import requests as req
from bs4 import BeautifulSoup
import cv2
from PIL import Image
import numpy as np
import os
import glob

# 여백
margin = 50
# 길이 * 너비
min_size = 5000


def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None


def imwrite(filename, img, params=None):
    # cv2.imread 가 한글 경로 저장이 안되므로 우회
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)
        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def make_dirs(dir):
    if (os.path.isdir(dir) == False):
        os.mkdir(dir)


def cropFace(images):
    face_cascade = cv2.CascadeClassifier(
        '../haarcascades/haarcascade_frontalface_default.xml')
    eye_casecade = cv2.CascadeClassifier('../haarcascades/haarcascade_eye.xml')

    for image in images:
        try:
            ff = np.fromfile(image, np.uint8)
            img = cv2.imdecode(ff, cv2.IMREAD_UNCHANGED)
            print(np.shape(img))
            # img = imread(image)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            if (faces is None):
                print('Failed to detect face')
                continue

            for (x, y, w, h) in faces:
                cropped = img[y - margin: y + h +
                              margin, x - margin: x + w + margin]
                cropped_gray = gray[y - margin: y + h +
                                    margin, x - margin: x + w + margin]
                eyes = eye_casecade.detectMultiScale(cropped_gray)

                # 눈 두개가 확인된 경우
                if(len(eyes) == 2 and w * h >= min_size):
                    # 이미지를 저장
                    imwrite(f"{margin}/{image}", cropped)
                    print(f"[{image}]: Cropped!")
                    imgNum += 1
        except Exception as e:
            print(e)
            continue


def init():
    images = []
    images.extend(glob.glob("./*.png"))
    images.extend(glob.glob("./*.jpg"))
    images.extend(glob.glob("./*.jpeg"))

    print(images)
    make_dirs(f"{margin}")
    cropFace(images)


init()
