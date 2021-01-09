# -*- coding:utf-8 -*-
from urllib.request import urlopen
import argparse
import requests as req
from bs4 import BeautifulSoup
import cv2
from PIL import Image
import numpy as np
import os


def make_dirs(dir):
    if (os.path.isdir(dir) == False):
        os.mkdir(dir)


def make_all_dirs(name):
    # 3개의 폴더 생성
    make_dirs(name)
    make_dirs(f"{name}/흑백")
    make_dirs(f"{name}/컬러")
    make_dirs(f"{name}/원본")


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


def save_original_image(name, url, filetype, i):
    t = urlopen(url).read()
    filename = f"{name}/원본/{name}" + str(i) + f".{filetype}"

    with open(filename, "wb") as f:
        f.write(t)


def cropFace(name, imgUrls):
    face_cascade = cv2.CascadeClassifier(
        '../haarcascades/haarcascade_frontalface_default.xml')
    eye_casecade = cv2.CascadeClassifier('../haarcascades/haarcascade_eye.xml')
    imgNum = 0

    for imgUrl in imgUrls:
        try:
            # 파일 확장자 저장
            filetype = imgUrl.split(".")[-1]

            # url로부터 cv2에 이미지 읽어오기
            req = urlopen(imgUrl)
            arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
            img = cv2.imdecode(arr, -1)  # 'Load it as it is'

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            if (faces is None):
                print('Failed to detect face')
                continue

            for (x, y, w, h) in faces:
                cropped = img[y:y + h, x:x + w]
                cropped_gray = gray[y:y + h, x:x + w]
                eyes = eye_casecade.detectMultiScale(cropped_gray)

                # 눈 두개가 확인된 경우
                if(len(eyes) == 2 and w * h >= 500):
                    # 원본 사진 저장
                    save_original_image(name, imgUrl, filetype, imgNum)
                    # 이미지를 저장
                    imwrite(f"{name}/컬러/{name}" +
                            str(imgNum) + f".{filetype}", cropped)
                    imwrite(f"{name}/흑백/{name}" +
                            str(imgNum) + f".{filetype}", cropped_gray)
                    print(f"[{name}{str(imgNum)}]: Cropped!")
                    imgNum += 1
        except Exception:
            continue


def save_images(name, imgUrls):
    people = name
    # 폴더 생성
    make_all_dirs(name)
    # 원본, 얼굴, 흑백 저장
    cropFace(name, imgUrls)
