from selenium import webdriver
from bs4 import BeautifulSoup
from lxml import html
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')


def create_data(speciality, form_of_education, name_of_university, region):
    specialisation = "Null"
    faculty = "Null"
    educational_program = "Null"
    tree = html.fromstring(str(speciality))

    educational_degree = tree.xpath("//div/div[1]/div[2]/b[1]/text()")[0]
    educational_degree += tree.xpath("//div/div[1]/div[2]/text()[2]")[0]
    educational_degree = educational_degree.replace("\n", "")

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
    branch = branch.replace("\n", "")
    if branch in tech:
        major_branch = "Природничі та технічні науки"
    elif branch in social:
        major_branch = "Соціальні науки та гуманітарні дисципліни"
    elif branch in health:
        major_branch = "Здоров’я та безпека"
    else:
        print("Exception" + branch)
    number_of_spec = tree.xpath("//div/div[1]/div[2]/span/a[1]/text()")[0].split(' ')[0]
    number_of_spec = number_of_spec.replace("\n", "")
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
    educational_program = educational_program.replace("\'", "`")
    educational_program = educational_program.replace('\"', '').strip()
    educational_degree = educational_degree.replace("\n", "")

    faculty = faculty.replace("\'", "`")
    faculty = faculty.replace('\"', '').strip()
    faculty = faculty.replace("\n", "")

    specialisation = specialisation.replace("\'", "`")
    specialisation = specialisation.replace('\"', '').strip()
    specialisation = specialisation.replace("\n", "")

    name_of_spec = tree.xpath("//div/div[1]/div[2]/span/a[1]/text()")[0][4::]
    name_of_spec = name_of_spec.replace("\'", "`")
    name_of_spec = name_of_spec.replace('\"', '')
    name_of_spec = name_of_spec.replace("\n", "")

    offer_type = tree.xpath("//div/div[1]/div[2]/text()[5]")[0]
    offer_type += tree.xpath("//div/div[1]/div[2]/text()[6]")[0].strip()
    offer_type = offer_type.replace("\'", "`")
    offer_type = offer_type.replace('\"', '')
    offer_type = offer_type.replace("\n", "")

    term_of_study = tree.xpath("//div/div[1]/div[2]/text()[7]")[0]
    term_of_study = term_of_study.replace("\n", "")
    if term_of_study == "Скорочений курс":
        term_of_study = " 00.00.0000 - 00.00.0000"
    start_time_of_study = term_of_study[1:11]
    end_time_of_study = term_of_study[14:24]
    try:
        license_scope = tree.xpath("//div/div[1]/div[2]/text()[9]")[0]
        license_scope = license_scope.replace("\n", "")
    except:
        license_scope = 0

    try:
        contract = tree.xpath("//div/div[1]/div[2]/text()[10]")[0]
        contract = contract.replace("\n", "")
        if contract == "":
            contract = 0
    except:
        contract = 0

    try:
        budget = tree.xpath("//div/div[1]/div[2]/text()[14]")[0]
        budget = budget.replace(":", "").strip()
        budget = budget.replace("\n", "")
        if budget == "":
            budget = 0
    except:
        budget = 0

    try:
        avg_budget = tree.xpath("//div/div[1]/div[2]/div[1]/b/text()")[0]
        avg_budget = avg_budget.replace("\n", "")
    except:
        avg_budget = 0

    try:
        avg_contract = tree.xpath("//div/div[1]/div[2]/div[2]/b/text()")[0]
        avg_contract = avg_contract.replace("\n", "")
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

    temp = ""

    for i in specialitydic:
        temp += f"{i}:{specialitydic[i]} "

    data = {
        "name_of_university": name_of_university,
        "region": region,
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
        "license_scope": license_scope,
        "contract": contract,
        "budget": budget,
        "avg_contract": avg_contract,
        "avg_budget": avg_budget,
        "specialitydic": temp
    }

    return data


def parse_university(url, name_of_university, i, db_decoder, mcursor, UniWave, region):

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")

    if content == '<html><head></head><body></body></html>':
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
    name_of_university = name_of_university.replace("\'", "")
    name_of_university = name_of_university.replace('\"', "")
    region = region.replace("\'", "")
    region = region.replace('\"', "")

    table_name = f"id{i}"
    mcursor.execute(f"CREATE TABLE {table_name} (id int, name_of_university VARCHAR(1000), region VARCHAR(1000),"
                     f" form_of_education VARCHAR(1000), educational_degree VARCHAR(1000),"
                     f"branch VARCHAR(1000),major_branch VARCHAR(1000), number_of_spec VARCHAR(1000) ,"
                     f"name_of_spec VARCHAR(1000),"
                     f"specialisation VARCHAR(1000),"
                     f"faculty VARCHAR(1000), educational_program VARCHAR(1000), offer_type VARCHAR(1000),"
                     f" start_time_of_study VARCHAR(1000), end_time_of_study VARCHAR(1000),"
                     f" License_scope VARCHAR(1000),"
                     f" contract VARCHAR(1000), budget VARCHAR(1000),avg_contract NUMERIC(5, 2),"
                     f"avg_budget NUMERIC(5, 2),"
                     f"specialitydic VARCHAR(1000),"
                     f"bardresponse TEXT)")
    # Денна форма навчання
    id = 0
    for speciality in specialities_den:
        data = create_data(speciality, "Денна", name_of_university, region)
        res.append(data)
        sql_table_insert(data, mcursor, table_name, UniWave, id)
        id += 1
    # Заочна форма навчання

    for speciality in specialities_zaoch:
        data = create_data(speciality, "Заочна", name_of_university, region)
        res.append(data)
        sql_table_insert(data, mcursor, table_name, UniWave, id)
        id += 1

    for speciality in specialities_distance:
        data = create_data(speciality, "Дистанційна", name_of_university, region)
        res.append(data)
        sql_table_insert(data, mcursor, table_name, UniWave, id)
        id += 1

    driver.close()
    db_decoder[table_name] = name_of_university
    mcursor.execute(f"INSERT INTO decoder (ID, NAME, REGION) VALUES ('{table_name}', '{name_of_university}', '{region}');")
    UniWave.commit()


def sql_table_insert(data, mcursor, table_name, UniWave, id):
    mcursor.execute(f"INSERT INTO {table_name} (id, name_of_university, region, form_of_education, educational_degree, branch, major_branch,"
                     f" number_of_spec, name_of_spec, specialisation, faculty, educational_program, offer_type,"
                     f" start_time_of_study, end_time_of_study, license_scope, contract, budget, avg_contract,"
                     f" avg_budget, specialitydic) VALUES ({id}, '{data['name_of_university']}','{data['region']}','{data['form_of_education']}', '{data['educational_degree']}', '{data['branch']}', '{data['major_branch']}',"
                     f" '{data['number_of_spec']}', '{data['name_of_spec']}', '{data['specialisation']}', '{data['faculty']}', '{data['educational_program']}', '{data['offer_type']}',"
                     f" '{data['start_time_of_study']}', '{data['end_time_of_study']}', '{data['license_scope']}', '{data['contract']}', '{data['budget']}', '{data['avg_contract']}',"
                     f" '{data['avg_budget']}', '{data['specialitydic']}');")

    UniWave.commit()
