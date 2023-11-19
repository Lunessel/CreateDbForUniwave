"""CopyRight"""
from bardapi import Bard
import time


BARD_TOKEN = 'dQiEI3IIK-D9C9Prql1I9wZLPO84M6yqK3J3F4dsfD5M-DC2B6VWRJSF6MYGx9zB_bTtSQ.'

class PromptWriter(Bard):
    """Here are all methods to write prompts"""
    def __init__(self) -> None:
        super().__init__(token=BARD_TOKEN)

    def write_first_prompt(self, university, faculty, speciality) -> str:
        first_prompt = (f"Go to the website {university}, go to the section {faculty} and describe the specialty" 
                        f"{speciality}"
                        "according to these criteria:"
                        "1. Find and write a description of the specialty, indicate what a specialist in this profession does."
                          "Submit it in a detailed, comprehensive format, make it simple"
                        "2. Describe the educational program of the specialty, what subjects it includes"
                          "and what the student will be able to study in general."
                        "3. What is the perspective for the career of this specialist in Ukraine and the world?"
                        "Do not go beyond the criterias, do not write a conclusion.  Provide information in a neutral format,"
                        "'from a bird's eye view', without advertising the university, also make it interesting,"
                          "oriented to applicants and their parents. Response in Ukrainian")
        response = self.get_answer(first_prompt)
        time.sleep(3)
        return response['content']
    
    def write_second_prompt(self, specility, university) -> str:
        second_prompt = (f"Can you add some additional information about speciality - {specility}"
                          f"in university - {university}, that was not included above , which might be"
                            "interesting for entrances or their parents. Response in Ukrainian")
        response = self.get_answer(second_prompt)
        time.sleep(3)
        return response['content']
