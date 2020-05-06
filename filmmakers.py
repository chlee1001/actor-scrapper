import requests
import re
from bs4 import BeautifulSoup

URL = "https://www.filmmakers.co.kr/index.php?mid=actorsProfile"
max_page = 359
filter = ["/", "*", "(", ")", ".", ",", "'", "\"",
          "[", "]", "<", ">", " ", "_", "-"]


def name_filter(name):
    for t in filter:
        name = name.replace(t, "")
    return name


def extract_profile(html):
    image_src = html.find("a").find("img").get("src")
    name = html.find("div", {"class": "content"}).find(
        "div", {"class": "description"}).find("a").text
    name = name_filter(name)
    age_tag = html.find("div", {"class": "extra"}).find("p")
    if age_tag:
        age_text = age_tag.text.strip()
        age = re.findall("\d+", age_text)[0]
        age = 2021 - int(age)
    else:
        age = None
    return {"name": name, "age": age, "image_src": image_src}


def get_profiles():
    profiles = []
    for page in range(max_page):
        print(f"Scrapping Film Makers: Page {page}")
        result = requests.get(f"{URL}&page={page}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "card"})
        for result in results:
            profile = extract_profile(result)
            profiles.append(profile)
    return profiles
