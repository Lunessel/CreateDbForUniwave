"""CopyRight"""
import json
import os
from prompts import PromptWriter


def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            update_json(file_path, file_name)



def update_json(file_path, file_name):
    print(file_name.replace(".json", ""))
    with open(file_path, 'r+', encoding='utf-8') as file:
        data = json.loads(file.read())
        user = PromptWriter()

        for specialty in data:
            faculty_name = specialty['faculty']
            specialty_name = specialty['number_of_spec'] + specialty['name_of_spec']
            
            if ("short_description" not in specialty or "Response Error" in specialty["short_description"] or 
                "У мене недостатньо інформації" in specialty["short_description"]):
                text_response_1 = user.write_first_prompt(university=file_name.replace(".json", ""), faculty=faculty_name, speciality=specialty_name)
                specialty["short_description"] = text_response_1

            if ("aditional_information" not in specialty or "Response Error" in specialty["aditional_information"] or 
               "У мене недостатньо інформації" in specialty["aditional_information"]):
                text_response_2 = user.write_second_prompt(university=file_name.replace(".json", ""), specility=specialty_name)
                specialty["aditional_information"] = text_response_2

            file.seek(0)
            file.write(json.dumps(data, ensure_ascii=False, indent=4))
            file.truncate()
        file.close
        print("Done, next -")

if __name__ == "__main__":
    folder_path = 'Ukraine_without_college' 
    process_folder(folder_path)
