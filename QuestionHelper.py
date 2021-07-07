import requests

from Question import Question


class QuestionHelper:

    def __init__(self):
        self.base_url = "https://opentdb.com/"
        self.category = ""
        self.session_token = ""
        self.question_queue = list()

    def set_category(self, category: str) -> None:
        self.category = category

    def get_session_token(self) -> bool:
        # Get a new session token
        url = self.base_url + "api_token.php"
        params = {
            "command": "request"
        }
        res = requests.get(url, params).json()
        self.session_token = res["token"]
        return True

    def list_categories(self) -> list:
        url = self.base_url + "api_category.php"
        res = requests.get(url).json()
        return res["trivia_categories"]
    
    def is_category(self, category) -> bool:
        is_category = False
        categories = self.list_categories()
        for c in categories:
            if str(c["id"]) == category:
                is_category = True
        return is_category

    def load_questions(self, num_questions: int = 50) -> int:
        """
        Load questions from the API. Must be called after set_category and get_session_token
        :param num_questions: Number of questions to load. Will stop loading if less questions exist in the catagory
        :return: Number of questions actually loaded. If the number is less than num_questions, the API has exhausted
        all questions for the category.
        """
        assert num_questions <= 50
        "https://opentdb.com/api.php?amount=10&token=YOURTOKENHERE"
        url = self.base_url + "api.php"
        params = {
            "amount": num_questions,
            "token": self.session_token
        }
        res = requests.get(url, params).json()
        json_questions = res["results"]

        # TODO : Use https://github.com/lidatong/dataclasses-json
        for q in json_questions:
            question = Question(
                question=q["question"],
                correct_answer=q["correct_answer"],
                type=q["type"],
                category=q["category"],
                difficulty=q["difficulty"],
                incorrect_answers=q["incorrect_answers"]
            )
            self.question_queue.append(question)

        return len(json_questions)

    def get_next_question(self) -> Question:
        return self.question_queue.pop()

    def reset(self) -> None:
        self.category = ""
        self.session_token = ""
