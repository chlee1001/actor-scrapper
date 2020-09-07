# -*- coding:utf-8 -*-
from naver_scrapper import crawling as crawl_naver
from google_scrapper import crawling as crawl_google
from save import save_images
import argparse


parser = argparse.ArgumentParser()

parser.add_argument("-name", "--people", required=True)
args = parser.parse_args()
people = args.people


def crawl_images(name):
    naver_urls = crawl_naver(name)
    google_urls = crawl_google(name)
    imgUrls = naver_urls + google_urls
    print(f"Total: {len(imgUrls)} images scrapped. ")
    # 원본, 얼굴, 흑백 저장
    save_images(name, imgUrls)


def main():
    names = people.split(',')
    for name in names:
        crawl_images(name)


if __name__ == "__main__":
    main()
