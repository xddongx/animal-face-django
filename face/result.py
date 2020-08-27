import cv2 as cv
import sip
# import matplotlib.pyplot as plt
from glob import glob
from PIL import Image
import os, glob, numpy as np
from keras.models import load_model
# keras v = '2.2.4-tf'
face_cascade = cv.CascadeClassifier(
    'C:/Users/rlaeh/Anaconda3/envs/myvenv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')


print('----------',face_cascade)
# 이미지 넣기
img = cv.imread('C:/workspace/animal-face-django/_media/media/2020/08/003.jpg')
print('-----------',img)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3, 5)
for (x, y, w, h) in faces:
    cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    roi_gray = gray[y:y + h, x:x + w]
    roi_color = img[y:y + h, x:x + w]
    sub_face = img[y:y + h, x:x + w]
    # 저장
    face_file_name = "./003.jpg"
    cv.imwrite(face_file_name, sub_face)

categories = ['고양이상', '공룡상', '토끼상']
nb_classes = len(categories)
print(categories)
image_w = 64
image_h = 64

X = []
filenames = []
files = 'C:/workspace/animal-face-django/face/003.jpg'
img = Image.open(files)
img = img.convert("RGB")
img = img.resize((image_w, image_h))
data = np.asarray(img)
filenames.append(files)
X.append(data)

X = np.array(X)
model = load_model('./static/face/animalmodel/animal-7.model')

prediction = model.predict(X)
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

for i in prediction:
    pre_ans = i.argmax()  # 예측 레이블
    print(i)
    print(pre_ans)
    pre_ans_str = categories[pre_ans]
    print("해당 " + "이미지는 " + pre_ans_str + "로 추정됩니다.")
