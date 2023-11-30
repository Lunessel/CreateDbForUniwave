from selenium import webdriver
import json
from bs4 import BeautifulSoup
from lxml import html


def create_data(speciality, form_of_education):
    name_of_spec = "Null"
    specialisation = "Null"
    faculty = "Null"
    educational_program = "Null"

    tree = html.fromstring(str(speciality))
    educational_degree = tree.xpath("//div/div[1]/div[2]/b[1]/text()")[0]
    educational_degree += tree.xpath("//div/div[1]/div[2]/text()[2]")[0]
    major_branch = None
    tech = ["Аграрні науки та продовольство",
            "Архітектура та будівництво",
            "Біологія",
            "Виробництво та технології",
            "Електрична інженерія",
            "Електроніка, автоматизація та електронні комунікації",
            "Інформаційні технології",
            "Математика та статистика",
            "Механічна інженерія",
            "Природничі науки",
            "Транспорт",
            "Хімічна інженерія та біоінженерія"]
    social = ["Богослов’я",
              "Гуманітарні науки",
              "Журналістика",
              "Культура і мистецтво",
              "Міжнародні відносини",
              "Освіта/Педагогіка",
              "Право",
              "Публічне управління та адміністрування",
              "Соціальна робота",
              "Соціальні та поведінкові науки",
              "Управління та адміністрування"]
    health = ["Ветеринарія",
              "Охорона здоров’я",
              "Цивільна безпека",
              "Сфера обслуговування",
              "Воєнні науки, національна безпека, безпека державного кордону"]
    branch = tree.xpath("//div/div[1]/div[2]/span/text()[2]")[0][1::]
    if branch in tech:
        major_branch = "Природничі та технічні науки"
    elif branch in social:
        major_branch = "Соціальні науки та гуманітарні дисципліни"
    elif branch in health:
        major_branch = "Здоров’я та безпека"
    else:
        print("Pizda" + branch)
    number_of_spec = tree.xpath("//div/div[1]/div[2]/span/a[1]/text()")[0].split(' ')[0]
    education_list = tree.xpath('//span[@class="search"]/text()')

    education_list = list(filter(lambda x: (x not in ['\n', ' ', '\xa0']), education_list))
    if len(education_list) == 2:
        name_of_spec, educational_program = education_list
    elif len(education_list) == 3:
        name_of_spec, faculty, educational_program = education_list
    elif len(education_list) == 4:
        name_of_spec, specialisation, faculty, educational_program = education_list
    else:
        print("Error")

    offer_type = tree.xpath("//div/div[1]/div[2]/text()[5]")[0]
    offer_type += tree.xpath("//div/div[1]/div[2]/text()[6]")[0]
    term_of_study = tree.xpath("//div/div[1]/div[2]/text()[7]")[0]
    if term_of_study == "Скорочений курс":
        term_of_study = " 00.00.0000 - 00.00.0000"
    start_time_of_study = term_of_study[1:11]
    end_time_of_study = term_of_study[14:24]

    try:
        license_scope = tree.xpath("//div/div[1]/div[2]/text()[9]")[0]
    except:
        license_scope = 0

    try:
        contract = tree.xpath("//div/div[1]/div[2]/text()[10]")[0]
    except:
        contract = 0
    try:
        budget = tree.xpath("//div/div[1]/div[2]/text()[14]")[0].split(' ')[1]
    except:
        budget = 0

    try:
        avg_budget = tree.xpath("//div/div[1]/div[2]/div[1]/b/text()")[0]
    except:
        avg_budget = 0

    try:
        avg_contract = tree.xpath("//div/div[1]/div[2]/div[2]/b/text()")[0]
    except:
        avg_contract = 0

    name_of_subjects = tree.xpath("//b[@class='nmt']/text()")
    koef_of_subjects = tree.xpath("//span[@class='coef']/text()")

    specialitydic = {}
    for i in range(len(name_of_subjects)):
        specialitydic[name_of_subjects[i]] = koef_of_subjects[i]

    try:
        motivation_letter_koef = tree.xpath("//div[@class='sub_105 nocoef']/div/span/text()")[0]
        specialitydic['Мотиваційний лист'] = motivation_letter_koef
    except:
        pass

    try:
        creative_competition = tree.xpath("//div[@class='sub_0']/div/span[@class='coef']/text()")[0]
        specialitydic['Творчий конкурс'] = creative_competition
    except:
        pass

    data = {
        "form_of_education": form_of_education,
        "educational_degree": educational_degree,
        "branch": branch,
        "major_branch": major_branch,
        "number_of_spec": number_of_spec,
        "name_of_spec": name_of_spec,
        "specialisation": specialisation,
        "faculty": faculty,
        "educational_program": educational_program,
        "offer_type": offer_type,
        "start_time_of_study": start_time_of_study,
        "end_time_of_study": end_time_of_study,
        "License_scope": license_scope,
        "contract": contract,
        "budget": budget,
        "avgcontract": avg_contract,
        "avgbudget": avg_budget,
        "specialitydic": specialitydic,
    }
    return data


def parse_university(url, name_of_university, name_of_region):
    if len(name_of_university) > 180:
        name_of_university = name_of_university[0:160] + " ... "
    name_of_university = name_of_university.replace('\"', '\'')

    driver = webdriver.Firefox()
    driver.get(url)

    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")

    if content == '<html><head></head><body></body></html>':
        print(name_of_university)
        driver.close()
        return

    name_of_den_spec = ["row no-gutters table-of-specs-item-row qual1 base40",
                        "row no-gutters table-of-specs-item-row qual1 base520 hidden",
                        "row no-gutters table-of-specs-item-row qual1 base620 hidden",
                        "row no-gutters table-of-specs-item-row qual2 base40 hidden",
                        "row no-gutters table-of-specs-item-row qual2 base620 hidden"]

    name_of_zaoch_spec = ["row no-gutters table-of-specs-item-row qual1 base40 hidden",
                          "row no-gutters table-of-specs-item-row qual1 base520 hidden",
                          "row no-gutters table-of-specs-item-row qual1 base620 hidden",
                          "row no-gutters table-of-specs-item-row qual2 base40 hidden",
                          "row no-gutters table-of-specs-item-row qual2 base620 hidden"]

    name_of_distance_spec = ["row no-gutters table-of-specs-item-row qual1 base40 hidden",
                             "row no-gutters table-of-specs-item-row qual1 base520 hidden",
                             "row no-gutters table-of-specs-item-row qual1 base620 hidden",
                             "row no-gutters table-of-specs-item-row qual2 base40 hidden",
                             "row no-gutters table-of-specs-item-row qual2 base620 hidden"]

    specialities_den = []
    specialities_zaoch = []
    specialities_distance = []
    try:
        for den_spec in name_of_den_spec:
            specialities_den += soup.find("div", {"class": "panel den"}) \
                .find("div", {"class": "table-of-specs"}) \
                .find_all("div", class_=den_spec)
    except:
        pass

    try:
        for zaoch_spec in name_of_zaoch_spec:
            specialities_zaoch += soup.find("div", {"class": "panel den"}) \
                .find("div", {"class": "table-of-specs"}) \
                .find_all("div", class_=zaoch_spec)
    except:
        pass

    try:
        for distance_spec in name_of_distance_spec:
            specialities_distance += soup.find("div", {"class": "panel den"}) \
                .find("div", {"class": "table-of-specs"}) \
                .find_all("div", class_=distance_spec)
    except:
        pass

    res = []
    # Денна форма навчання
    for speciality in specialities_den:
        data = create_data(speciality, "Денна")
        res.append(data)

    # Заочна форма навчання

    for speciality in specialities_zaoch:
        data = create_data(speciality, "Заочна")
        res.append(data)

    for speciality in specialities_distance:
        data = create_data(speciality, "Дистанційна")
        res.append(data)

    with open(f"./{name_of_region}/{name_of_university}.json", "w", encoding='utf-8') as write_file:
        json.dump(res, write_file, ensure_ascii=False)  # , ensure_ascii=False is optional

    driver.close()
