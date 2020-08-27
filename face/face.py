from PIL import Image
import os, glob, numpy as np
from keras.models import load_model
import time, os.path


def animalmodel(image_path):
    categories = ['고양이상', '공룡상', '토끼상']
    nb_classes = len(categories)
    # model-3
    # image_w = 128
    # image_h = 128

    # model-7
    image_w = 64
    image_h = 64

    X = []
    filenames = []

    toyear = str(time.strftime('%Y'))                                                   # 현제 년도
    tomonth = str(time.strftime('%m'))                                                  # 현제 월
    file_dir = os.path.join('../_media/media/{}/{}/'.format(toyear, tomonth))
    # print('file_dir : ',file_dir)
    # files = '../_media/media/{}/{}/'.format(toyear, tomonth)+image_path
    fileName = 'C:/workspace/animal-face-django/_media/media/{}/{}/'.format(toyear, tomonth) + image_path
    files = file_dir + image_path
    print('files : ',files)

    img = Image.open(fileName)
    img = img.convert("RGB")
    img = img.resize((image_w, image_h))
    data = np.asarray(img)
    filenames.append(files)
    X.append(data)

    X = np.array(X)
    # model = load_model('C:/workspace/animal-face-django/face/static/face/animalmodel/animal-3.model')
    model = load_model('C:/workspace/animal-face-django/face/static/face/animalmodel/animal-7.model')

    prediction = model.predict(X)
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

    for i in prediction:
        pre_ans = i.argmax()  # 예측 레이블
        print(i)
        print(pre_ans)
        pre_ans_str = categories[pre_ans]
        print("해당 " + "이미지는 " + pre_ans_str + "로 추정됩니다.")

    argmax_face = prediction.argmax()
    face = categories[argmax_face]
    pre = []
    for i in prediction[0]:
        pre.append(round(i,2)*100)
    return face, pre

# files = '../_media/media/2020/08/김동현.jpg'
# # face, predic = animalmodel(files)
# #
# # print('face : ', face)
# # print('prediction : ', predic)