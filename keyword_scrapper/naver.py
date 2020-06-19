# -*- coding:utf-8 -*-

from urllib.request import urlopen
import argparse
import requests as req
from bs4 import BeautifulSoup
import cv2
from PIL import Image
import numpy as np
import os


parser = argparse.ArgumentParser()

parser.add_argument("-name", "--people", required=True)
args = parser.parse_args()
people = args.people


def make_dirs(dir):
    if (os.path.isdir(dir) == False):
        os.mkdir(dir)


def make_all_dirs():
    # 3개의 폴더 생성
    make_dirs("흑백")
    make_dirs("컬러")
    make_dirs("원본")


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


def bigImageUrl(url):
    # thumbnail 이미지가 아닌 원본 사이즈 이미지의 URL로 변환
    return url.split("&type")[0]


def save_original_image(url, filetype, i):
    t = urlopen(url).read()
    filename = f"원본/{people}" + str(i) + f".{filetype}"

    with open(filename, "wb") as f:
        f.write(t)


def cropFace(imgUrls):
    face_cascade = cv2.CascadeClassifier(
        '../haarcascades/haarcascade_frontalface_default.xml')
    eye_casecade = cv2.CascadeClassifier('../haarcascades/haarcascade_eye.xml')
    imgNum = 0

    for imgUrl in imgUrls:
        # 파일 확장자 저장
        filetype = imgUrl.split(".")[-1]
        # 원본 사진 저장
        save_original_image(imgUrl, filetype, imgNum)
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
            if(len(eyes) == 2):
                # 이미지를 저장
                imwrite(f"컬러/crop_{people}" +
                        str(imgNum) + f".{filetype}", cropped)
                imwrite(f"흑백/gray_{people}" +
                        str(imgNum) + f".{filetype}", cropped_gray)
                print(f"[{people}{str(imgNum)}]: Cropped!")
                imgNum += 1


def getImages(pageNumber):
    # 네이버 url https://search.naver.com/search.naver?where=image&sm=tab_jum&query=%EC%97%AC%EC%9A%B0%EC%83%81
    url_info = "https://search.naver.com/search.naver?"
    params = {
        "query": people,
        "where": "image",
        "face": 1,
        "start": pageNumber*50
    }
    html_object = req.get(url_info, params)
    img_data = []

    # BeautifulSoup로 파싱
    if html_object.status_code == 200:
        bs_object = BeautifulSoup(html_object.text, "html.parser")
        img_data = bs_object.find_all("img", {"class": "_img"})

    return img_data


def main():
    # 폴더 생성
    make_all_dirs()

    # 이미지 태그 50 * 20 = 1000개 받아오기
    img_datas = []
    for i in range(20):
        img_datas = img_datas + getImages(i)

    # 이미지 태그로부터 URL 받아오기
    imgUrls = []
    for i, img in enumerate(img_datas):
        # 원본 사이즈 URL로 변환
        url = bigImageUrl(img['data-source'])
        filetype = url.split(".")[-1]
        # cv2 지원 포맷인 경우 append
        if filetype != "jpg" and filetype != "png":
            continue
        imgUrls.append(url)

    # 원본, 얼굴, 흑백 저장
    cropFace(imgUrls)


if __name__ == "__main__":
    main()
