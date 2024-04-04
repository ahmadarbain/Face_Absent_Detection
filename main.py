import cv2 as cv
import os
import pickle
import face_recognition
import numpy as np
import cvzone
from firebase_admin import credentials, db
import firebase_admin
from time import sleep
from datetime import datetime

def capture_video():
    # Fungsi untuk memulai deteksi objek hanya saat tombol ditekan

    cred = credentials.Certificate("serviceAccountKey.json")
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred,{
            'databaseURL': 'https://faceemployeeattandance-default-rtdb.firebaseio.com/',
            'storageBucket': 'faceemployeeattandance.appspot.com'
        })

    cap = cv.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    print("Loading encode file")
    file = open('EncodeFile.p', 'rb')
    encodeListWithName = pickle.load(file)
    file.close()
    encodeListKnown, employeeName = encodeListWithName

    while True:
        success, img = cap.read()

        imgs = cv.resize(img, (0, 0), None, 1, 1)
        imgs = cv.cvtColor(imgs, cv.COLOR_BGR2RGB)

        faceCurrentFrame = face_recognition.face_locations(imgs)
        encodeCurrentFrame = face_recognition.face_encodings(imgs, faceCurrentFrame)
        
        for encodeFace, faceLoc in zip(encodeCurrentFrame, faceCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            distances = face_recognition.face_distance(encodeListKnown, encodeFace)
            
            matchIndex = np.argmin(distances)
            id = employeeName[matchIndex] 

            if matches[matchIndex]:    
                employeeInfo = db.reference(f'Employee/{id}').get()
                if not employeeInfo.get('attendance_marked', False):
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 1, x2 * 1, y2 * 1, x1 * 1
                    bbox = (x1, y1, x2 - x1, y2 - y1)
                    img = cvzone.cornerRect(imgs, bbox, rt=0)
                    img = cv.cvtColor(img, cv.COLOR_RGB2BGR)

                    text_present = "Present"
                    text_name = str(employeeInfo['nick_name'])
                    text_present_size = cv.getTextSize(text_present, cv.FONT_HERSHEY_COMPLEX, 1, 1)[0]
                    text_name_size = cv.getTextSize(text_name, cv.FONT_HERSHEY_COMPLEX, 1, 1)[0]
                    cv.putText(img, text_name, (x1 + 15, y2 + text_present_size[1] + 5), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
                    cv.putText(img, text_present, (x1 + 15, y2 + 2 * text_present_size[1] + 10 + text_name_size[1]), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
                    
                    db.reference(f'Employee/{id}').update({'attendance_marked': True})
                    attendTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    attendance_ref = db.reference('Attendance').push()
                    attendance_ref.set({
                        'employee_id': id,
                        'attendance_time': attendTime,
                        'name':text_name,
                        'status': 'Present'
                    })
                    print(f"{employeeInfo['nick_name']} attendance present at {attendTime}.")

                    sleep(5)

                else:
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 1, x2 * 1, y2 * 1, x1 * 1
                    bbox = (x1, y1, x2 - x1, y2 - y1)
                    img = cvzone.cornerRect(imgs, bbox, rt=0)
                    img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
                    text_present = "Marked"
                    text_name = str(employeeInfo['nick_name'])
                    text_present_size = cv.getTextSize(text_present, cv.FONT_HERSHEY_COMPLEX, 1, 1)[0]
                    text_name_size = cv.getTextSize(text_name, cv.FONT_HERSHEY_COMPLEX, 1, 1)[0]
                    cv.putText(img, text_name, (x1 + 15, y2 + text_present_size[1] + 5), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
                    cv.putText(img, text_present, (x1 + 15, y2 + 2 * text_present_size[1] + 10 + text_name_size[1]), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
                    print(f"{employeeInfo['nick_name']} attendance Marked.")
                
            else:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 1, x2 * 1, y2 * 1, x1 * 1
                bbox = (x1, y1, x2 - x1, y2 - y1)
                img = cvzone.cornerRect(imgs, bbox, rt=0)
                img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
                cv.putText(img,"People Unknown",(x1+15, y2-25),cv.FONT_HERSHEY_COMPLEX,1,(0,255,0),1)
            
        cv.imshow("Webcam", img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()
