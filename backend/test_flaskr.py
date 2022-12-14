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
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_path = "postgresql://postgres:AdeDoud$98@localhost:5432/trivia_test"
        setup_db(self.app, self.database_path)
        
        self.new_question = {
            "question": "c'est quoi Flask",
            "answer": "Framework python",
            "category": 3,
            "difficulty": 4
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

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
   
    #--- Tester la recuperation de toutes les categories ------
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    #--- Tester la recuperation de toutes les categories en cas d'echec ------

    
    #--- Tester la recuperation de toutes les questions ------
    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])

   
    #--- Tester la recuperation de toutes les categories en cas d'echec ------
    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "ressource not found")

    
    #--- Tester la suppression d'une question de part son id ------
    def test_delete_specific_question(self):
        res = self.client().delete("/questions/5")
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    
    #--- Tester la suppression d'une question qui n'existe pas ------
    def test_422_if_question_does_not_exist(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
        

   
    #--- Tester la creation d'une question ------
    def test_create_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

   
    #--- Tester la creation d'une question ------
    def test_405_if_question_create_not_allowed(self):
        res = self.client().post("/questions/5", json=self.new_question)
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")
    
    #--- Tester la recherche d'une question avec resultats ------
    def test_get_question_search_with_result(self):
        res = self.client().post("/questions", json={"search": "title"})
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)

    #--- Tester la recuperation des questions par categorie ------
    def test_get_questions_per_categories(self):
        res  = self.client().get("/categories/5/questions")
        data = json.loads(res.data)
        print(data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])

     #--- Tester la recuperation des questions pour une categorie ne contenant pas des questions ------
    def test_get_questions_from_unexist_category(self):
        res  = self.client().get("/categories/10/questions")
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "ressource not found")

    #--- Tester la recuperation des questions pour le quizzes ------
    def test_get_quizzes(self):
        res = self.client().post("quizzes", json={
            "previous_questions": [1, 4, 20, 15],"quiz_category": {"type" : "Science","id": 1}
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["question"])  
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()