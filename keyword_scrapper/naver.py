# -*- coding:utf-8 -*-

from urllib.request import urlopen
import argparse
import requests as req
from bs4 import BeautifulSoup
import cv2
from PIL import Image
import numpy as np


parser = argparse.ArgumentParser()

parser.add_argument("-name", "--people", required=True)
args = parser.parse_args()
people = args.people


def bigImageUrl(url):
    return url.split("&type")[0]


def cropFace(filenames):
    face_cascade = cv2.CascadeClassifier(
        '../haarcascades/haarcascade_frontalface_default.xml')
    eye_casecade = cv2.CascadeClassifier('../haarcascades/haarcascade_eye.xml')
    imgNum = 0
    for filename in filenames:
        img = cv2.imread(filename)
        img2 = Image.open(filename)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        if (faces is None):
            print('Failed to detect face')
            continue
        print(f"Face Detected: {faces}")
        for (x, y, w, h) in faces:
            cropped = gray[y:y + h, x:x + w]
            # 이미지를 저장
            cv2.imwrite("crop" + str(imgNum) + ".jpg", cropped)
            print(f"[crop{str(imgNum)}]: Cropped!")
            imgNum += 1


def main():
    # 네이버 url https://search.naver.com/search.naver?where=image&sm=tab_jum&query=%EC%97%AC%EC%9A%B0%EC%83%81
    url_info = "https://search.naver.com/search.naver?"
    params = {
        "query": people,
        "where": "image",
        "face": 1
    }
    html_object = req.get(url_info, params)

    if html_object.status_code == 200:

        bs_object = BeautifulSoup(html_object.text, "html.parser")
        img_data = bs_object.find_all("img", {"class": "_img"})

        imgNames = []

        for i, img in enumerate(img_data):
            url = bigImageUrl(img['data-source'])
            filetype = url.split(".")[-1]

            if filetype != "jpg":
                continue

            t = urlopen(url).read()
            filename = str(i+1) + "." + filetype

            with open(filename, "wb") as f:
                f.write(t)

            print(f"[{filename}]: Img Save Success")
            imgNames.append(filename)

        print(imgNames)
        cropFace(imgNames)


if __name__ == "__main__":
    main()
