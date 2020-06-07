import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'postgres:postgres@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": "What is the acceleration of gravity?",
            "answer": "9.81 m/s2",
            "difficulty": 3,
            "category": 1
        }

        self.invalid_new_question = {
            "question": "Who discovered gravity?",
            "answer": "Newton",
            "difficulty": "Three",
            "category": 1
        }

        self.quiz_with_valid_category = {
            "quiz_category": {"id": 1, "type": "Science"},
            "previous_questions": [20]
        }

        self.quiz_with_not_valid_category = {
            "quiz_category": {"id": 1000, "type": "Marvel"},
            "previous_questions": []
        }

        self.quiz_without_category = {
            "quiz_category": {"id": 0, "type": "ALL"},
            "previous_questions": []
        }

        self.search_term = {
            "searchTerm": "title"
        }

        self.empty_search_term = {
            "searchTerm": ""
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_retrieve_categories(self):
        res = self.client().get("/api/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    def test_retrieve_questions(self):
        res = self.client().get("/api/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertEqual(data["total_questions"], 19)
        self.assertTrue(data["categories"])
        self.assertEqual(data["current_category"], {})

    def test_create_new_question(self):
        count_before = Question.query.count()
        res = self.client().post("/api/questions", json=self.new_question)
        data = json.loads(res.data)
        count_after = Question.query.count()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(count_before + 1, count_after)

    def test_422_if_create_new_question_with_invalid_input(self):
        count_before = Question.query.count()
        res = self.client().post("/api/questions", json=self.invalid_new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable")

    def test_search_questions(self):
        res = self.client().post("/api/questions", json=self.search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertEqual(data["total_questions"], 2)
        self.assertEqual(data["current_category"], {})

    def test_400_if_search_term_is_empty(self):
        res = self.client().post("/api/questions", json=self.empty_search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad Request")

    def test_get_questions_by_category(self):
        res = self.client().get("/api/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertEqual(data["current_category"], {
                         "id": 1, "type": "Science"})

    def test_404_if_category_not_found(self):
        res = self.client().get("/api/categories/1000/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not Found")

    def test_delete_question(self):
        res = self.client().delete("/api/questions/2")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["question_id"], 2)

    def test_422_delete_question_not_exist(self):
        res = self.client().delete("/api/questions/10000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable")

    def test_get_quiz_with_valid_category(self):
        res = self.client().post("/api/quizzes", json=self.quiz_with_valid_category)
        data = json.loads(res.data)
        previous_questions = self.quiz_with_valid_category["previous_questions"]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])
        self.assertNotIn(data["question"]["id"], previous_questions)

    def test_get_quiz_without_category(self):
        res = self.client().post("/api/quizzes", json=self.quiz_without_category)
        data = json.loads(res.data)
        previous_questions = self.quiz_without_category["previous_questions"]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])
        self.assertNotIn(data["question"]["id"], previous_questions)

    def test_400_get_quiz_with_not_existing_category(self):
        res = self.client().post("/api/quizzes", json=self.quiz_with_not_valid_category)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad Request")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
