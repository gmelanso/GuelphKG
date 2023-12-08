from datetime import datetime
from ..utils import *

def create_councillor_entity(row):
    return {
        "id": str(uuid.uuid4()),
        "type": "Person",
        "address": {
            "type": "PostalAddress",
            "addressCountry": "Canada",
            "addressRegion": "Ontario",
            "addressLocality": row['Locality'],
            "postalCode": row['Postal code'],
            "streetAddress": f"{row['Address line 1']} {row['Address line 2']}" if row['Address line 1'] != 'nan' and row['Address line 2'] != 'nan' else '',
            "email": row['Email'],
            "fax": row['Fax'],
            "telephone": row['Phone']              
        },
        "cellNumber": {
            "type": "Property",
            "value": row['Cell']
        },
        "familyName": {
            "type": "Property",
            "value": row['Last name']
        },
        "gender": {
            "type": "Property",
            "value": row['Gender']
        },
        "givenName": {
            "type": "Property",
            "value": row['First name']
        },
        "image": {
            "type": "Property",
            "value": row['Photo URL']
        },
        "representsWard": {
            "type": "Relationship",
            "object": 0 if row['District name'] == "Guelph" else row['District name'][-1]
        }
    }


def create_item_entity(abstract, has_parts, id, meeting_id, moved_by, seconded_by, title):
    return {
        "type": "AgendaItem",
        "id": id,
        "abstract": {
            "type": "Property",
            "value": abstract
        },
        "hasPart": {
            "type": "Relationship",
            "object": has_parts
        },
        "isPartOf": {
            "type": "Relationship",
            "object": [
                meeting_id
            ]
        },
        "movedBy": {
            "type": "Relationship",
            "object": [
                moved_by
            ]
        },
        "title": {
            "type": "Property",
            "value": title
        },
        "secondedBy": {
            "type": "Relationship",
            "object": [
                seconded_by
            ]            
        },
        "@context": [
            "https://schema.org/",
            "https://schema.org/CreativeWork",
            {
            "movedBy": "https://schema.org/contributor",
            "secondedBy": "https://schema.org/contributor"
            }
        ]
    }


def create_meeting_entity(attendees, date, id, items):
    return {  
        "type": "MeetingMinutes",
        "id": id,
        "attendees": {
            "type": "Relationship",
            "object": [
                attendee for attendee in attendees
            ]
        },
        "dateCreated": {
            "type": "Property",
            "value": convert_to_iso_format(date)
        },
        "hasPart": {
            "type": "Relationship",
            "object": [item for item in items]
        },
        "@context": [
            "https://schema.org/",
            "https://schema.org/CreativeWork"
        ]
    }


def create_motion_entity(about, abstract, id, item, moved_by, seconded_by, sequence, vote_id):
    return {
        "type": "Motion",
        "id":  id,
        "about": {
            "type": "Property",
            "value": about           
        },
        "abstract": {
            "type": "Property",
            "value": abstract
        },
        "isPartOf": {
            "type": "Relationship",
            "object": [
                item
            ]
        },
        "movedBy": {
            "type": "Relationship",
            "object": [
                moved_by
            ]
        },
        "secondedBy": {
            "type": "Relationship",
            "object": [
                seconded_by
            ]            
        },
        "sequence": {
            "type": "Property",
            "value": sequence        
        },
        "vote": {
            "type": "Relationship",
            "object": [
                vote_id
            ]
        },
        "@context": [
            "https://schema.org/",
            "https://schema.org/CreativeWork",
            {
            "vote": "https://schema.org/workPerformed",
            "movedBy": "https://schema.org/contributor",
            "secondedBy": "https://schema.org/contributor"
            }
        ]
    }

def create_vote_entity(id, motion_id, nays, yeas):
    return {
        "type": "VoteAction",
        "id":  id,
        "yeas": {
            "type": "Relationship",
            "object": yeas
        },
        "nays": {
            "type": "Relationship",
            "object": nays
        },
        "subjectOf": {
            "type": "Relationship",
            "object": [
                motion_id
            ]
        },
        "@context": [
            "https://schema.org/",
            "https://schema.org/CreativeWork",
            {
            "yeas": "https://schema.org/contributor",
            "nays": "https://schema.org/contributor"
            }
        ] 
    }
