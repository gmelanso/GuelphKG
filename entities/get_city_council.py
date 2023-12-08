
import json
import uuid
import pandas as pd

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

if __name__=="__main__":

    f_paths= [
        "./data/csv/guelph-mayor-and-councillors-contact-information-2018-2022.csv",
        "./data/csv/guelph-mayor-and-councillors-contact-information-2022-2026.csv"
    ]

    df1= pd.read_csv(f_paths[1])
    df2= pd.read_csv(f_paths[0])
    rows_to_add = df2[~df2[['First name', 'Last name']].isin(df1[['First name', 'Last name']]).all(axis=1)]

    dfs= pd.concat([df1, rows_to_add], ignore_index=True)
    dfs.fillna('', inplace=True)

    entities= [create_councillor_entity(row) for _, row in dfs.iterrows()]
    
    with open('./entities/json/CityCouncil.json', 'w') as file:
        json.dump(entities, file, indent=4)
