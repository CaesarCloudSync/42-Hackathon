import json
import requests
import unittest
import sys

uri = "http://127.0.0.1:8080" #"https://blacktechdivisionreward-hrjw5cc7pa-uc.a.run.app"

class AnthropicTestCase(unittest.TestCase):
    def test_message(self):
        response = requests.get(f"{uri}/sendmessage",params={"message":"how can I learn python flask programming?"})
        print(response.json())
        self.assertEqual(response.json().get("error"),None)
        self.assertNotEqual(response.json().get("error"),"you have already done this action can't gain tokens.")
    def test_store_question(self):
        response = requests.get(f"{uri}/storequestion",params={"username":"Amari","question_set_title":"Maths Test for 8-9 Year Olds","question":"What is the result of 5 + 7?","useranswered":"14","answer":"12","numofattempts":3,"hintsused":1})
        print(response.json())
        response = requests.get(f"{uri}/storequestion",params={"username":"Amari","question_set_title":"Maths Test for 8-9 Year Olds","question":"If you have 8 apples and eat 2, how many apples do you have left?","useranswered":"7","answer":"6","numofattempts":3,"hintsused":0})
        print(response.json())
        response = requests.get(f"{uri}/storequestion",params={"username":"Amari","question_set_title":"Maths Test for 8-9 Year Olds","question":"If you have 9 cars and 2 were destroyed, how many cars do you have left?","useranswered":"7","answer":"6","numofattempts":3,"hintsused":3})
        print(response.json())
        response = requests.get(f"{uri}/storequestion",params={"username":"Amari","question_set_title":"Maths Test for 8-9 Year Olds","question":"Multiply 3 by 6","useranswered":"18","answer":"18","numofattempts":5,"hintsused":0})
        print(response.json())
        response = requests.get(f"{uri}/storequestion",params={"username":"Amari","question_set_title":"Maths Test for 8-9 Year Olds","question":"Multiply 8 by 6","useranswered":"48","answer":"48","numofattempts":5,"hintsused":0})
        print(response.json())
        response = requests.get(f"{uri}/storequestion",params={"username":"Amari","question_set_title":"Maths Test for 8-9 Year Olds","question":"Multiply 5 by 3","useranswered":"15","answer":"15","numofattempts":5,"hintsused":0})
        print(response.json())
        response = requests.get(f"{uri}/storequestion",params={"username":"Amari","question_set_title":"Maths Test for 8-9 Year Olds","question":"Divide 20 by 4.","useranswered":"5","answer":"5","numofattempts":5,"hintsused":0})
        print(response.json())
        response = requests.get(f"{uri}/storequestion",params={"username":"Amari","question_set_title":"Maths Test for 8-9 Year Olds","question":"What is 10 minus 3?","useranswered":"9","answer":"7","numofattempts":3,"hintsused":0})
        print(response.json())
    def test_count_result(self):
        response = requests.get(f"{uri}/count_result",params={"username":"Amari","question_set_title":"Maths Test for 8-9 Year Olds"})
        print(response.json())
    def test_create_profile_for_teacher(self):
        response = requests.get(f"{uri}/create_profile_for_teacher")
        print(response.json())
    def test_create_profile_for_parent(self):
        response = requests.get(f"{uri}/create_profile_for_parent",params={"username":"Amari","question_set_title":"Maths Test for 8-9 Year Olds"})
        print(response.json())
    def test_get_profile_for_teacher(self):
        response = requests.get(f"{uri}/get_profile_for_teacher")
        print(response.json())
    def test_gen_parent(self):
        response = requests.get(f"{uri}/create_profile_for_parent",params={"username":"Amari","question_set_title":"Maths Test for 8-9 Year Olds","question":"What is 10 minus 3?","useranswered":"9","answer":"7","numofattempts":3,"hintsused":0})
        print(response.json())


if __name__ == "__main__":
    unittest.main()