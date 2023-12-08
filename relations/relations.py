import csv
import os

from ..utils import 

def update_relations_table(t_path='./data/relations/relations_to_id.csv', data):
    create_directory(t_path)
    

    return


RELATIONS= [
    "isPartOf",
    "hasPart",
    "attendees",
    "movedBy",
    "secondedBy",
    "vote",
    "yeas",
    "nays",
    "subjectOf"
]