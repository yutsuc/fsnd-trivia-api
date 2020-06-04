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
        self.database_path = "postgres://{}/{}".format('postgres:postgres@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_retrieve_all_categories(self):
        res = self.client().get("/api/categories")
        data = json.loads(res.data)

        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
    
    def test_retrieve_all_questions(self):
        res = self.client().get("/api/questions")
        data = json.loads(res.data)

        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertEqual(data["total_questions"], 19)
        self.assertTrue(data["categories"])
        self.assertEqual(data["current_category"], "ALL")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()