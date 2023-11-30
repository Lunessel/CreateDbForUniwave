from selenium import webdriver
from bs4 import BeautifulSoup
import os
import shutil
from university import parse_university

baseUrl = "https://vstup.osvita.ua/"


def get_university_by_region(region_name, url):
    driver = webdriver.Firefox()
    driver.get(url)

    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")

    list_of_li = soup.find("ul", {"class": "section-search-result-list"}).find_all("li")

    for li in list_of_li:
        a = li.find("a")
        university_name = a.text
        university_name = university_name.replace('\"', '\'')
        university_url = baseUrl + a['href'][1:]

        parse_university(university_url, university_name, region_name)

    driver.close()


def main():
    driver = webdriver.Firefox()
    driver.get(baseUrl)

    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")

    trs = soup.find("tbody").find_all("tr")

    regions = {}
    for tr in trs:
        a = tr.find("td").find("a")
        if a.text in {"Львівська область"}:
            regions[a.text] = baseUrl + a['href'][1:]

    try:
        shutil.rmtree('Україна')
    except:
        pass
    os.mkdir("Україна")
    os.chdir("./Україна")

    for region in regions:
        os.mkdir(region)

    for region in regions:
        get_university_by_region(region, regions[region])

    driver.close()


main()
