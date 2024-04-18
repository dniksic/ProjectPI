import os
import pickle

import cv2
import face_recognition

#importiranje slika iz foldera
folderPath = 'Slike'
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
imgIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    imgIds.append(os.path.splitext(path)[0])
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

