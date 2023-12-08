
import json
import os
import re
import uuid

from itertools import chain
from datetime import datetime

from definitions import create_vote_entity, create_motion_entity, 
from definitions import create_item_entity, create_meeting_entity

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait


def get_meeting_minutes_urls():

    hrefs= {}

    driver = webdriver.Chrome()
    driver.get('https://guelph.ca/city-hall/mayor-and-council/city-council/agendas-and-minutes/')

    driver.switch_to.frame('MeetingsFrame')
    WebDriverWait(
        driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH, '//*[@id="calendar"]/div[1]/div[3]/button[4]'
                )
            )
        ).click()
    
    Select(
        WebDriverWait(
            driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.CLASS_NAME, 'YearFilterOption'
                    )
                )
            )
        ).select_by_index(0)

    WebDriverWait(
        driver, 10).until(
            EC.element_to_be_clickable(
                (By.ID, 'ctl00_MainContent_lvPastMeetingTypes_ctrl0_ExpandCollapseLink')
            )
        ).click()
    
    link_elements= WebDriverWait(
        driver,10).until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH, "//a[contains(@aria-label, 'Minutes') and contains(@aria-label, 'HTML')]"
                )
            )
        )
    
    for link_element in link_elements:
        pattern= r'(\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2}:\d{2} [APMapm]{2})'
        key= link_element.get_attribute('aria-label')
        key= re.search(pattern, key)
        key= key.group(1)
        hrefs[key] = link_element.get_attribute("href")
        
    driver.quit()
    
    return hrefs


def parse_minutes_to_json(url, date):

    items= []
    motions= []
    votes= []

    meeting_has_part= []

    response = requests.get(url)

    if response.status_code == 200:

        soup= BeautifulSoup(response.text, 'html.parser')

        # Below code will get the attendees of the meeting as a list of strings
        attendees_table = soup.find('table', class_='AgendaHeaderAttendanceTable')
        attendees_div = soup.find('div', class_='AgendaHeaderAttendanceTable')

        all_attendees = []

        if attendees_table:
            for value_element in attendees_table.find_all('td', class_='Value'):
                attendees_list = value_element.find('ul').find_all('li', recursive=False)
                all_attendees.extend([attendee.get_text(strip=True) for attendee in attendees_list])

        if attendees_div:
            for value_element in attendees_div.find_all('div', class_='Value'):
                attendees_list = value_element.find('ul').find_all('li', recursive=False)
                all_attendees.extend([attendee.get_text(strip=True) for attendee in attendees_list])

        agenda_items= soup.find_all('div', class_='AgendaItemContainer')
        for item in agenda_items:
            item_id= str(uuid.uuid4())
            counter= item.find('div', class_='AgendaItemCounter').get_text(strip=True) if item.find('div', class_='AgendaItemCounter') else None
            title= item.find('div', class_='AgendaItemTitle').find('a').get_text(strip=True) if item.find('div', class_='AgendaItemTitle') and item.find('div', class_='AgendaItemTitle').find('a') else None
            title = f"{counter} {title}"
            meeting_has_part.append(item_id)

            # extract information for the agenda item
            item_abstract= item.find('div', class_='AgendaItemMinutes RichText').get_text(strip=True) if item.find('div', class_='AgendaItemMinutes RichText') else None
            item_moved_by= item.find('div', class_='MovedBy').find('span', class_='Value').get_text(strip=True) if item.find('div', class_='MovedBy') else None
            item_seconded_by= item.find('div', class_='SecondedBy').find('span', class_='Value').get_text(strip=True) if item.find('div', class_='SecondedBy') else None
            motion_text= item.find('div', class_='MotionText RichText').get_text(strip=True) if item.find('div', class_='MotionText RichText') else None
            item_result= item.find('div', class_='MotionResult').get_text(strip=True) if item.find('div', class_='MotionResult') else None
            item_title= f"{counter} {title}"

            item_vote_id= str(uuid.uuid4())
            item_voters= item.find('table', class_='MotionVoters').get_text(strip=True) if item.find('table', class_='MotionVoters') else None
            item_yeas, item_nays= vote_record(item_voters)

            if item_yeas:
                votes.append(
                    create_vote_action(id=item_vote_id, motion_id=item_id, nays=item_nays, yeas=item_yeas)
                )

            # Check if AgendaItemMotions exist within the item
            agenda_item_motions = item.find('ul', class_='AgendaItemMotions')
            item_has_part= []

            if agenda_item_motions:
                # Iterate over each AgendaItemMotion
                for index, motion in enumerate(agenda_item_motions.find_all('li', class_='AgendaItemMotion'), 1):

                    motion_about= " ".join(
                        [
                            motion.find('div', class_='PreMotionText RichText').get_text(strip=True) if motion.find('div', class_='PreMotionText RichText') else None,
                            motion.find('div', class_='PostMotionText RichText').get_text(strip=True) if motion.find('div', class_='PostMotionText RichText') else None,
                            motion.find('div', class_='MotionResult').get_text(strip=True) if motion.find('div', class_='MotionResult') else None
                        ]
                    )
                    motion_abstract= motion.find('div', class_='MotionText RichText').get_text(strip=True) if motion.find('div', class_='MotionText RichText') else None
                    motion_moved_by= motion.find('div', class_='MovedBy').find('span', class_='Value').get_text(strip=True) if motion.find('div', class_='MovedBy') else None
                    motion_seconded_by= motion.find('div', class_='SecondedBy').find('span', class_='Value').get_text(strip=True) if motion.find('div', class_='SecondedBy') else None
                    motion_id= str(uuid.uuid4())
                    motion_sequence= index
                    item_has_part.append(motion_id)

                    vote_id= str(uuid.uuid4())
                    motion_vote= motion.find('table', class_='MotionVoters').get_text(strip=True) if motion.find('table', class_='MotionVoters') else None
                    motion_yeas, motion_nays= vote_record(motion_vote)

                    motions.append(
                        create_motion_entity(
                            about=motion_about, 
                            abstract=motion_abstract, 
                            id=motion_id, 
                            item=item_id, 
                            moved_by=motion_moved_by, 
                            seconded_by=motion_seconded_by, 
                            sequence=motion_sequence, 
                            vote_id=vote_id
                            )
                        )

                    if motion_yeas:
                        votes.append(
                            create_vote_entity(
                                id=vote_id, 
                                motion_id=motion_id, 
                                nays=motion_nays, 
                                yeas=motion_yeas
                                )
                            )

            items.append(
                create_item_entity( 
                    abstract=item_abstract, 
                    has_parts=item_has_part, 
                    id=item_id, 
                    meeting_id=url, 
                    moved_by=item_moved_by, 
                    seconded_by=item_seconded_by, 
                    title=item_title)
            )

        meeting= create_meeting_entity(
            attendees=all_attendees, 
            date=date, 
            id=url, 
            items=meeting_has_part)

    return meeting, items, motions, votes


def vote_record(s):
    if s:
        fors= re.search(r'Voting in Favour: \(\d+\)(.*)Voting Against:', s)
        against= re.search(r'Voting Against: \(\d+\)(.*)', s)
    
        yeas = [name.strip() for name in re.split(r',\s*and|\s*,', fors.group(1))] if fors else None
        nays = [name.strip() for name in re.split(r',\s*and|\s*,', against.group(1))] if against else None
        return yeas, nays
    
    else:
        return None, None


if __name__=="__main__":

    meeting_objs= []

    with open('./data/minutes/minutes_url.json', 'r') as file:
        urls= json.load(file)
    
    for date, url in urls.items():
        meeting, items, motions, votes= parse_minutes_to_json(url, date)
        meeting_objs.append(meeting)
        for each in [items, motions, votes]:
            meeting_objs.extend(each)

    with open('./entities/json/MeetingMinutes.json', 'w') as file:
        json.dump(meeting_objs, file, indent=4)

    