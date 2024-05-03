import pickle
import numpy as np
import cv2
import os
import cvzone
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import db

import face_recognition


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://evidencijaprepoznavanjemlica-default-rtdb.europe-west1.firebasedatabase.app/",
    'storageBucket':"evidencijaprepoznavanjemlica.appspot.com"
})
bucket = storage.bucket()

# Otvaranje kamere
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Učitavanje pozadine
slikaPozadine = cv2.imread("Resursi/pozadina.png")
if slikaPozadine is None:
    raise Exception("Pozadinska slika nije učitana.")

# Učitavanje modova
datotekaModovaPutanja = 'Resursi/Modovi'
modoviPutanjaLista = os.listdir(datotekaModovaPutanja)
slikeModovaLista = [cv2.imread(os.path.join(datotekaModovaPutanja, path)) for path in modoviPutanjaLista]

# Učitavanje enkodirane datoteke
print("Učitavanje enkodirane datoteke započeto...")
file = open("EncodeFile.p", "rb")
encodeListWithIds = pickle.load(file)
file.close()
encodeListKnown, imgIds = encodeListWithIds
print("Enkodirana datoteka uspješno učitana.")

modeType= 0
counter = 0
id = -1
imgS = []


# Glavna petlja
while True:
    success, img = cap.read()
    if not success:
        print("Nije uspjelo čitanje slike s kamere.")
        continue

    # Priprema za detekciju
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Detekcija lica
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    # Stavljanje slike s kamere na pozadinu
    slikaPozadine[150:150 + 480, 44:44 + 640] = img

    # Ako imamo modove, postavite ih na pozadinu



    # Obrada detekcije lica
    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)


        # Najbolji match
        matchIndex = np.argmin(faceDis)
        #print("Match Index:", matchIndex)

        if matches[matchIndex]:
           # print("Poznato lice detektirano:", imgIds[matchIndex])

            # Uzimanje koordinata i pretvaranje u originalnu veličinu
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

            # Postavljanje okvira
            bbox = (55 + x1, 162 + y1, x2 - x1, y2 - y1)
            #print("Koordinate bbox-a:", bbox)

            # Provjera da su koordinate unutar granica slike
            if (x1 >= 0 and y1 >= 0 and x2 <= slikaPozadine.shape[1] and y2 <= slikaPozadine.shape[0]):
                slikaPozadine = cvzone.cornerRect(slikaPozadine, bbox, rt=0)
            id = imgIds[matchIndex]
            if counter == 0:
                counter = 1
                modeType = 1

        if counter != 0:

            if counter == 1:

                #Povlacenje podataka iz baze
                studentInfo = db.reference(f'Studenti/{id}').get()
                print(studentInfo)
                #Dohvat slike iz storagea

                blob = bucket.get_blob(f'Slike/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgS = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                #Azuriranje podataka o evidenciji
                ref = db.reference(''f'Studenti/{id}')
                studentInfo['ukupno_dolazaka'] += 1
                ref.child('ukupno_dolazaka').set(studentInfo['ukupno_dolazaka'])

    if 10 < counter < 20:
        modeType = 2
        slikaPozadine[50:50 + 600, 790:790 + 400] = slikeModovaLista[modeType]

    if counter <= 10:

        cv2.putText(slikaPozadine,str(studentInfo['ukupno_dolazaka']),(835,125),
                    cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
        cv2.putText(slikaPozadine, str(studentInfo['titula']), (950, 530),
                    cv2.FONT_HERSHEY_COMPLEX, 0.4, (255, 255, 255),1)
        cv2.putText(slikaPozadine, str(id), (970, 483),
                    cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 1)
        cv2.putText(slikaPozadine, str(studentInfo['godina']), (1005, 605),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100,100,100), 1)
        cv2.putText(slikaPozadine, str(studentInfo['godina_upisa']), (1095, 605),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100,100,100), 1)

        (w,h), _= cv2.getTextSize(studentInfo['name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
        offset = (414-w)//2
        cv2.putText(slikaPozadine, str(studentInfo['name']), (808+offset, 445),
                    cv2.FONT_HERSHEY_COMPLEX, 0.8, (50, 50, 50), 1)


        #slikaPozadine[175:175 + 216, 885:885 + 216] = imgS #
        counter+=1

    # Prikazivanje rezultata
    cv2.imshow("Sistem evidencije", slikaPozadine)

    # Uvjet za izlaz iz petlje
    if cv2.waitKey(1) & 0xFF == ord('q'):
             break

cap.release()  # Oslobađanje resursa
cv2.destroyAllWindows()  # Zatvaranje svih prozora