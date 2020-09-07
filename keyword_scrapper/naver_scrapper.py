# -*- coding:utf-8 -*-

from urllib.request import urlopen
import argparse
import requests as req
from bs4 import BeautifulSoup
import cv2
from PIL import Image
import numpy as np
import os


def getImages(pageNumber, query):
    # 네이버 url https://search.naver.com/search.naver?where=image&sm=tab_jum&query=%EC%97%AC%EC%9A%B0%EC%83%81
    url_info = "https://search.naver.com/search.naver?"
    params = {
        "query": query,
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


def bigImageUrl(url):
    # thumbnail 이미지가 아닌 원본 사이즈 이미지의 URL로 변환
    return url.split("&type")[0]


def crawling(query):

    # 이미지 태그 50 * 20 = 1000개 받아오기
    img_datas = []
    for i in range(20):
        img_datas = img_datas + getImages(i, query)

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
    print(f"Naver: {len(imgUrls)} images scrapped. ")
    # 원본, 얼굴, 흑백 저장
    return imgUrls
