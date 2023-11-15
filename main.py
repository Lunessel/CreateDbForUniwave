import json
from prompts import WritePrompt


with open('politeh.json', 'r+', encoding='utf-8') as file:
    data = json.loads(file.read())
    user = WritePrompt()
    sequence_number = 0
    for specialty in data:
        if "short_description" not in specialty or "Response Error" in specialty["short_description"]:
            faculty_name = specialty['faculty']
            specialty_name = specialty['number_of_spec'] + specialty['name_of_spec']
            text_response_1 = user.write_first_prompt(university="Lviv.ua", faculty=faculty_name, speciality=specialty_name)
            specialty["short_description"] = text_response_1
        if "aditional_information" not in specialty or "Response Error" in specialty["aditional_information"]:
            text_response_2 = user.write_second_prompt(university="Lviv Politechnic National University(Lpnu.ua)", specility=specialty_name)
            specialty["aditional_information"] = text_response_2
        sequence_number += 1
        print(sequence_number)
        file.seek(0)
        file.write(json.dumps(data, ensure_ascii=False, indent=4))
        file.truncate()


    file.close()
