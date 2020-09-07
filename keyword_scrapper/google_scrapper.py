from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import time


def crawling(query):
    PATH = 'chromedriver.exe'
    wd = webdriver.Chrome(executable_path=PATH)
    google_search = "https://www.google.com/search?q={q}&tbm=isch"
    wd.get(google_search.format(q=query))
    time.sleep(2)
    for i in range(2000):
        wd.execute_script('window.scrollBy(0, 10000)')
    image_sizes = wd.find_elements_by_css_selector('div.isv-r')

    count = 0
    imgUrls = []

    for image_size in image_sizes:
        try:
            if int(image_size.get_attribute('data-ow')) > 500 and int(image_size.get_attribute('data-oh')) > 500:
                image_size.click()
                time.sleep(1)
                actual = wd.find_element_by_xpath(
                    '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img')

                pic = actual.get_attribute('src')
                time.sleep(1)
                imgUrls.append(pic)

                count += 1
        except Exception:
            continue
    wd.close()
    print(f"Google: {len(imgUrls)} images scrapped. ")
    return imgUrls
