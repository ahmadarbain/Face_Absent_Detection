import cv2 as cv
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://faceemployeeattandance-default-rtdb.firebaseio.com/',
    'storageBucket': 'faceemployeeattandance.appspot.com'
})

# Importing Resources Images
folderModelPath = 'Images'
pathList = os.listdir(folderModelPath)
print(pathList)
imgList = []
employeeName = []
for path in pathList:
    imgList.append(cv.imread(os.path.join(folderModelPath, path)))
    employeeName.append(os.path.splitext(path)[0])

    fileName = f'{folderModelPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
    
print(employeeName)


def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)


    return encodeList

print("Encoding Started")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithName = [encodeListKnown,employeeName]
# print(encodeListKnownWithName)
print("Encoding Complate") 

file = open("EncodeFile.p","wb")
pickle.dump(encodeListKnownWithName, file)
file.close()
print("File Save")
   