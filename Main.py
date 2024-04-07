import cv2
import os

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



while True:
    success, img = cap.read()
    slikaPozadine[150:150 + 480, 44:44 + 640] = img
    slikaPozadine[50:50 + 600, 790:790 + 400] = slikeModovaLista[0]

    #cv2.imshow("Webkamera", img)
    cv2.imshow("Sistem evidencije", slikaPozadine)


    cv2.waitKey(1)



