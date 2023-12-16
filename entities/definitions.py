import uuid
from datetime import datetime
from utils import *

PERSON= {
    "relationships": {
        "attendees": "Attendees of an Event.",
        "yeas": "Support a legislative CreativeWork",
        "nays": "Opposes a legislative CreativeWork",
        "movedBy": "",
        "secondedBy": ""
    }
}

def ByLaw(**kwargs):
    return {
        "id": kwargs['id'] if 'id' in kwargs else str(uuid.uuid4()),
        "type": "Legislation",
        "bylawId": {
            "type": "Property",
            "value": kwargs['bylawId'] if 'bylawId' in kwargs else []
        },
        "dateCreated": { 
            "type": "Property",
            "value": kwargs['dateCreated'] if 'dateCreated' in kwargs else []
        },
        "isPartOf": { 
            "type": "Relationship",
            "object": kwargs['isPartOf'] if 'isPartOf' in kwargs else []
        },
        "legislationApplies": {
            "type": "Relationship",
            "object": kwargs['legislationApplies'] if 'legislationApplies' in kwargs else []
        },
        "legislationConsolidates": {
            "type": "Relationship",
            "object": kwargs['legislationConsolidates'] if 'legislationConsolidates' in kwargs else []
        },
        "legislationDate": {
            "type": "Property",
            "value": kwargs['legislationDate'] if 'legislationDate' in kwargs else []
        },
        "legislationRepeals": {
            "type": "Relationship",
            "object": kwargs['legislationRepeals'] if 'legislationRepeals' in kwargs else []
        },
        "legislationType": {
            "type": "Property",
            "value": "By-law"
        },
        "name": {
            "type": "Property",
            "value": kwargs['name'] if 'name' in kwargs else (kwargs['bylawId'] if 'bylawId' in kwargs else [])
        },
        "recordedAt": { 
            "type": "Relationship",
            "object": kwargs['recordedAt'] if 'recordedAt' in kwargs else []
        }
    }

def Person(row):
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


def AgendaItem(**kwargs):
    return {
        "type": "AgendaItem",
        "id": kwargs['id'] if 'id' in kwargs else [],
        "abstract": {
            "type": "Property",
            "value": kwargs['abstract'] if 'abstract' in kwargs else []
        },
        "dateCreated": {
            "type": "Property",
            "value": kwargs['dateCreated'] if 'dateCreated' in kwargs else []
        },
        "hasPart": {
            "type": "Relationship",
            "object": kwargs['hasPart'] if 'hasPart' in kwargs else []
        },
        "isPartOf": {
            "type": "Relationship",
            "object": kwargs['isPartOf'] if 'isPartOf' in kwargs else []
        },
        "movedBy": {
            "type": "Relationship",
            "object": kwargs['movedBy'] if 'movedBy' in kwargs else []
        },
        "title": {
            "type": "Property",
            "value": kwargs['title'] if 'title' in kwargs else []
        },
        "secondedBy": {
            "type": "Relationship",
            "object": kwargs['secondedBy'] if 'secondedBy' in kwargs else []           
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


def MeetingMinutes(**kwargs):
    return {  
        "type": "MeetingMinutes",
        "id": kwargs['id'] if 'id' in kwargs else [],
        "attendees": {
            "type": "Relationship",
            "object": kwargs['attendees'] if 'attendees' in kwargs else []
        },
        "dateCreated": {
            "type": "Property",
            "value": kwargs['dateCreated'] if 'dateCreated' in kwargs else []
        },
        "hasPart": {
            "type": "Relationship",
            "object": kwargs['hasPart'] if 'hasPart' in kwargs else []
        },
        "@context": [
            "https://schema.org/",
            "https://schema.org/CreativeWork"
        ]
    }


def Motion(**kwargs):
    return {
        "type": "Motion",
        "id":  kwargs['id'] if 'id' in kwargs else [],
        "about": {
            "type": "Property",
            "value": kwargs['about'] if 'about' in kwargs else []          
        },
        "abstract": {
            "type": "Property",
            "value": kwargs['abstract'] if 'abstract' in kwargs else []
        },
        "dateCreated": {
            "type": "Property",
            "value": kwargs['dateCreated'] if 'dateCreated' in kwargs else []
        },
        "isPartOf": {
            "type": "Relationship",
            "object": kwargs['isPartOf'] if 'isPartOf' in kwargs else []
        },
        "movedBy": {
            "type": "Relationship",
            "object": kwargs['movedBy'] if 'movedBy' in kwargs else []
        },
        "nays": {
            "type": "Relationship",
            "object": kwargs['nays'] if 'nays' in kwargs else []
        },
        "secondedBy": {
            "type": "Relationship",
            "object": kwargs['secondedBy'] if 'secondedBy' in kwargs else []            
        },
        "sequence": {
            "type": "Property",
            "value": kwargs['sequence'] if 'sequence' in kwargs else []        
        },
        "yeas": {
            "type": "Relationship",
            "object": kwargs['yeas'] if 'yeas' in kwargs else []
        },
        "@context": [
            "https://schema.org/",
            "https://schema.org/CreativeWork",
            {
            "vote": "https://schema.org/workPerformed",
            "movedBy": "https://schema.org/contributor",
            "secondedBy": "https://schema.org/contributor",
            "yeas": "https://schema.org/contributor",
            "nays": "https://schema.org/contributor"
            }
        ]
    }


def newProperty(obj=None):
    return {
        "type": "Property",
        "value": obj if obj else []
    }


def newRelation(obj=None):
    return {
        "type": "Relationship",
        "object": obj if obj else []
    }