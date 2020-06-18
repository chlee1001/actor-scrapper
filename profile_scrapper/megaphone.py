import requests
import re
from bs4 import BeautifulSoup

LIMIT = 20
ROOT_URL = "http://megaphonekorea.com"
URL = "http://megaphonekorea.com/index.php/dataFunction/indexList"
filter = ["/", "*", "(", ")", ".", ",", "'", "\"",
          "[", "]", "<", ">", " ", "_", "-"]


def name_filter(name):
    for t in filter:
        name = name.replace(t, "")
    return name


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("ul", {"class": "pagination"})
    lists = pagination.find_all('li')
    last = lists[-1]
    max_page = int(last.find("a").get("data-ci-pagination-page")) / LIMIT
    return int(max_page)


def extract_profile(html):
    image_src = html.find("div", {"class": "img_box"}).find("img").get("src")
    if image_src:
        image_src = ROOT_URL + image_src
    else:
        return
    name = html.find("div", {"class": "img_box"}).find("p").text
    if name == "탈퇴":
        return
    else:
        name = name_filter(name)
    age = None
    return {"name": name, "age": age, "image_src": image_src}


def extract_profiles(last_page):
    profiles = []
    for page in range(last_page):
        print(f"Scrapping Megaphone Korea: Page {page}")
        page_url = page*LIMIT
        if page_url is 0:
            page_url = 1
        result = requests.get(f"{URL}/page/{page_url}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("li", {"class": "indexList"})
        for result in results:
            profile = extract_profile(result)
            if profile:
                profiles.append(profile)
    return profiles


def get_profiles():
    last_page = get_last_page()
    jobs = extract_profiles(last_page)
    return jobs
