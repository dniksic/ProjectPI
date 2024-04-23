import pickle
import numpy
import cv2
import os
import cvzone

import face_recognition

cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

slikaPozadine = cv2.imread('Resursi/pozadina.png')


#importanje modova u listu
datotekaModovaPutanja = 'Resursi/Modovi'
modoviPutanjaLista = os.listdir(datotekaModovaPutanja)
slikeModovaLista = []
for path in modoviPutanjaLista:
    slikeModovaLista.append(cv2.imread(os.path.join(datotekaModovaPutanja, path)))

#print(len(slikeModovaLista)) test

#učitavanje enkodiranog filea
print("Učitavanje enkodirane datoteke započeto...")
file = open('EncodeFile.p','rb')
encodeListWithIds = pickle.load(file)
file.close()
encodeListKnown, imgIds = encodeListWithIds
#print(imgIds)
print("Enkodirana datoteka uspješno učitana...")

while True:
    success, img = cap.read()

    imgS=cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    faceCurFrame=face_recognition.face_locations(imgS)
    encodeCurFrame=face_recognition.face_encodings(imgS, faceCurFrame)

    slikaPozadine[150:150 + 480, 44:44 + 640] = img
    slikaPozadine[50:50 + 600, 790:790 + 400] = slikeModovaLista[0]

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        mathces=face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        #print("matches", mathces)
        #print("faceDis", faceDis)

        mathcIndex=numpy.argmin(faceDis)
        #print("Match Index", mathcIndex)
        if mathces[mathcIndex]:
            #print("Poznato lice detektirano")
            #print(imgIds[mathcIndex])
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
       #     bbox = 790+x1, 50+y1, x2-x1, y2-y1
            cvzone.cornerRect(slikaPozadine, bbox, rt=0)


    #cv2.imshow("Webkamera", img)
    cv2.imshow("Sistem evidencije", slikaPozadine)


    cv2.waitKey(1)



