from selenium import webdriver
from bs4 import BeautifulSoup
import os
import shutil
from university import parse_university
import mysql.connector

baseUrl = "https://vstup.osvita.ua/"

UniWave = mysql.connector.connect(
  host="localhost",
  user="root",
  password="22060810D"
)

mycursor = UniWave.cursor()
mycursor.execute("DROP DATABASE UniWave")
mycursor.execute("CREATE DATABASE UniWave")

mycursor.execute("SHOW DATABASES")


def get_university_by_region(url):
    driver = webdriver.Firefox()
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    i = 0
    list_of_li = soup.find("ul", {"class": "section-search-result-list"}).find_all("li")
    for li in list_of_li:
        a = li.find("a")
        university_name = a.text
        university_name = university_name.replace('\"', '\'')
        university_url = baseUrl + a['href'][1:]
        i += 1

        parse_university(university_url, university_name, i)

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
        if a.text in {"Київ"}:
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
        get_university_by_region(regions[region])

    driver.close()


main()
