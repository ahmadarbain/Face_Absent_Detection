import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://faceemployeeattandance-default-rtdb.firebaseio.com/'
})

ref = db.reference('Employee')

data = {
    "FEA0001":
    {
        "name": "Dermot Kennedy",
        "nick_name": "Dermot",
        "departement":"Research & Development",
        'attendance_marked': False,
        "last_attand_ime": "2022-12-11 00:45:34"
    },  
    
    "FEA0002":
    {
        "name": "Edward Christopher Sheeran",
        "nick_name": "Ed Sheeran",
        "departement":"Software Engineer",
        'attendance_marked': False,
        "last_attand_ime": "2022-12-11 00:45:34"
    },
    
    "FEA0003":
    {
        "name": "George Ezra",
        "nick_name": "George",
        "departement":"Software Engineer",
        'attendance_marked': False,
        "last_attand_ime": "2022-12-11 00:45:34"
    },
    "FEA0004":
    {
        "name": "Ahmad Arbain",
        "nick_name": "Arbain",
        "departement":"Data Scientist",
        'attendance_marked': False,
        "last_attand_ime": ""
    }
}

for key,value in data.items():
    ref.child(key).set(value)