import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://evidencijaprepoznavanjemlica-default-rtdb.europe-west1.firebasedatabase.app/"
})

ref = db.reference('Studenti')

data = {
    "321654":
        {
            "name": "Davor Niksic",
            "titula": "Student informatike",
            "godina": "4",
            "ukupno_dolazaka": "6",
            "godina_upisa": "2020",
            "zadnja_evidencija_vrijeme": "2024-04-29 00:54:34"
        },
    "852741":
{
            "name": "Sanel Halacevic",
            "titula": "Student informatike",
            "godina": "4",
            "ukupno_dolazaka": "11",
            "godina_upisa": "2020",
            "zadnja_evidencija_vrijeme": "2024-04-29 03:54:34"
        },
}

for key,value in data.items():
    ref.child(key).set(value)