from selenium import webdriver
from bs4 import BeautifulSoup
import os
import shutil
import threading
import itertools

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
        if len(university_name) > 200:
            university_name = university_name[0:190] + " ... "
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
        regions[a.text] = baseUrl + a['href'][1:]

    try:
        shutil.rmtree('Україна')
    except:
        pass
    os.mkdir("Україна")
    os.chdir("./Україна")


    for region in regions:
        os.mkdir(region)

    number_of_threads = 4
    items = list(regions.items())

    for group in itertools.zip_longest(*[iter(items)] * number_of_threads):
        print("group")
        threads = []
        for region, url in group:
            thread = threading.Thread(target=get_university_by_region, args=(region, url))
            threads.append(thread)
            thread.start()
        
        for t in threads:
            t.join()

    for region in regions:
        get_university_by_region(region, regions[region])

    driver.close()


main()
