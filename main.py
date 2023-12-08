from selenium import webdriver
from bs4 import BeautifulSoup
from university import parse_university
from selenium.webdriver.chrome.options import Options
import os
import psycopg2
from dotenv import load_dotenv


options = Options()
options.add_argument('--headless')


baseUrl = "https://vstup.osvita.ua/"

#UniWave = mysql.connector.connect(
#  host="localhost",
#  user="root",
#  password="22060810D"
#)
#
#mcursor = UniWave.cursor()
#mcursor.execute("DROP DATABASE UniWave")
#mcursor.execute("CREATE DATABASE UniWave")

def get_university_by_region(url, region):
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    i = 0
    db_decoder = {}
    list_of_li = soup.find("ul", {"class": "section-search-result-list"}).find_all("li")
    UniWave = psycopg2.connect(os.getenv('DATABASE_URL'))
    mcursor = UniWave.cursor()
    mcursor.execute(f"CREATE TABLE decoder(ID VARCHAR(100), NAME VARCHAR(1000), REGION VARCHAR(1000))")
    UniWave.commit()

    for li in list_of_li:
        a = li.find("a")
        university_name = a.text
        university_name = university_name.replace('\"', '\'')
        university_url = baseUrl + a['href'][1:]
        i += 1

        parse_university(university_url, university_name, i, db_decoder, mcursor, UniWave, region)

    mcursor.close()
    UniWave.close()
    driver.close()


def main():
    driver = webdriver.Chrome(options=options)
    driver.get(baseUrl)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")

    trs = soup.find("tbody").find_all("tr")

    regions = {}
    for tr in trs:
        a = tr.find("td").find("a")
        if a.text in {"Львівська область"}:
            regions[a.text] = baseUrl + a['href'][1:]

    for region in regions:
        get_university_by_region(regions[region], region)

    driver.close()


main()