import os
import pickle
import firebase_admin
from firebase_admin import credentials

from firebase_admin import storage
import cv2
import face_recognition


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://evidencijaprepoznavanjemlica-default-rtdb.europe-west1.firebasedatabase.app/",
    'storageBucket':"evidencijaprepoznavanjemlica.appspot.com"
})

#importiranje slika iz foldera
folderPath = 'Slike'
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
imgIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    imgIds.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

    # print(path)
    # print(os.path.splitext(path)[0])
print(imgIds)

def findEncodings(imagesList):
    encodeList=[]
    for img in imagesList:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

print("Enkodiranje započeto...")
encodeListKnown=findEncodings(imgList)
encodeListKnownWithIds=[encodeListKnown, imgIds]
print(encodeListKnown)
print("Enkodiranje gotovo")

file=open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("Datoteka kreirana i spremljena")

