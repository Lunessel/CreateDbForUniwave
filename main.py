import json
from bardapi import Bard
import time

BARD_TOKEN = 'dAiEI_ezActkfW4d7bI7NrvSLw66HJF0e_NRACi1h-JhCDGRyZbYJMDOrEUGhAIOKrSXIQ.'


def write_prompt(university, faculty, speciality):
    prompt = (f"Зайди на сайт {university} ,"
              f"перейди до розділу {faculty} та розпиши спеціальність"
              f"{speciality}"
              "за цими критеріями:"
              "1. Напиши короткий опис спеціальності ,вкажи чим конкретно займається спеціаліст даної професії."
              "Подай це у розгорнутому, всебічному форматі"
              "2. Опишіть освітню програму спеціальності,"
              " які предмети вона включає та що загалом зможе вивчити студент."
              "3. Яка є перспектива для кар'єри в Україні та світі?"
              "4. Напиши додаткову інформацію яка може бути цікава вступникам"
              "Не виходь за рамки пунктів , не пиши висновок. Подай інформацію у нейтральному форматі,"
              " з висоти пташиного польоту, не рекламуючи університет, також зроби її цікавою ,"
              "орієнтованою на вступників та їхніх батьків")
    response = bard.get_answer(prompt)
    return response['content']


bard = Bard(token=BARD_TOKEN)
with open('politeh.json', 'r+', encoding='utf-8') as file:
    data = json.loads(file.read())
    for specialty in data:
        if "short_description" not in specialty or "Response Error" in specialty["short_description"]:
            faculty_name = specialty['faculty']
            specialty_name = specialty['number_of_spec'] + specialty['name_of_spec']
            text = write_prompt(university="Lviv.ua", faculty=faculty_name, speciality=specialty_name)
            print(text)
            specialty["short_description"] = text

            file.seek(0)
            file.write(json.dumps(data, ensure_ascii=False, indent=4))
            file.truncate()
            time.sleep(1)
    file.close()
