import requests
import re
from bs4 import BeautifulSoup

LIMIT = 20
ROOT_URL = "http://megaphonekorea.com"
URL = "http://megaphonekorea.com/index.php/dataFunction/indexList"
KEYWORD = ["all", "14", "16", "17", "18", "20", "21", "22", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33",
           "34", "35", "36", "37", "38", "39", "41", "42",
           "43", "44", "45", "46", "47", "48", "49", "50", "51", "53", "55", "56", "57", "58", "59", "60"]
GENDER = ["all", "M", "F"]
AGE = ["all", "1~", "2~", "3~", "4~", "5~", "6~"]
BODY = "all"
CORPORALPUNISHMENT = "all"
SPECIALTY = "all"
TEXT = "none"
filter = ["/", "*", "(", ")", ".", ",", "'", "\"",
          "[", "]", "<", ">", " ", "_", "-"]


# http://megaphonekorea.com/index.php/dataFunction/indexList/q/keyword/all/gender/all/age/all/body/all/corporalpunishment/all/specialty/all/text/none/page/15280

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
        page_url = page * LIMIT
        if page_url is 0:
            page_url = 1
        result = requests.get(
            f"{URL}/q/keyword/{KEYWORD[0]}/gender/{GENDER[1]}/age/{AGE[0]}/body/{BODY}/corporalpunishment/{CORPORALPUNISHMENT}/specialty/{SPECIALTY}/text/{TEXT}/page/{page_url}")
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
