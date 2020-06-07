import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # Set up CORS. Allow '*' for origins
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers",
                             "Content-Type, Authorization, true")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        response.headers.add("Access-Control-Allow-Methods",
                             "GET, PATCH, POST, DELETE, OPTIONS")
        return response

    def get_categories_as_dictionary():
        categories = {}
        for category in Category.query.all():
            categories[category.id] = category.type

        return categories

    def get_paginated_results(results, request):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        return results[start:end]

    '''
    GET requests for all available categories
    '''
    @app.route("/api/categories")
    def retrieve_categories():
        categories = get_categories_as_dictionary()

        return jsonify({
            "success": True,
            "categories": categories
        })

    '''
    GET requests for questions, including pagination (every 10 questions)
    '''
    @app.route("/api/questions")
    def retrieve_questions():
        questions = Question.query.order_by("id").all()
        formatted_questions = [
            question.format() for question in get_paginated_results(questions, request)]
        categories = get_categories_as_dictionary()

        return jsonify({
            "success": True,
            "questions": formatted_questions,
            "total_questions": len(questions),
            "categories": categories,
            "current_category": {}
        })

    '''
    POST request to create a new question or get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.
    '''
    @app.route("/api/questions", methods=["POST"])
    def create_new_question():
        req = request.get_json()
        search_term = req.get("searchTerm", None)

        if search_term is None:
            try:
                question = req.get("question")
                answer = req.get("answer")
                difficulty = int(req.get("difficulty"))
                category = req.get("category")
                new_question = Question(question, answer, category, difficulty)
                new_question.insert()

                return jsonify({
                    "success": True
                })

            except:
                abort(422)
        else:
            if search_term == "":
                abort(400)

            questions = Question.query.filter(
                Question.question.ilike(f"%{search_term}%")).all()
            formatted_questions = [
                question.format() for question in get_paginated_results(questions, request)]
            return jsonify({
                "success": True,
                "questions": formatted_questions,
                "total_questions": len(questions),
                "current_category": {}
            })

    '''
    GET requests to get questions based on category.
    '''
    @app.route("/api/categories/<int:category_id>/questions")
    def get_questions_by_category(category_id):
        category = Category.query.get(category_id)

        if category is None:
            abort(404)

        questions = Question.query.filter(
            Question.category == category_id).order_by("id").all()
        formatted_questions = [
            question.format() for question in get_paginated_results(questions, request)]

        return jsonify({
            "success": True,
            "questions": formatted_questions,
            "total_questions": len(questions),
            "current_category": category.format()
        })

    '''
    DELETE requests to remove a question
    '''
    @app.route("/api/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            question.delete()
            return jsonify({
                "success": True,
                "question_id": question_id,
            })
        except:
            abort(422)

    '''
    POST requests to get questions to play the quiz.
    '''
    @app.route("/api/quizzes", methods=["POST"])
    def retrieve_quiz():
        req = request.get_json()
        category_id = req["quiz_category"]["id"]
        previous_questions = req["previous_questions"]

        if category_id == 0:
            questions = Question.query.filter(
                ~Question.id.in_(previous_questions)).all()
        else:
            category = Category.query.get(category_id)
            if category is None:
                abort(400)
            questions = Question.query.filter(
                Question.category == category_id, ~Question.id.in_(previous_questions)).all()

        if len(questions) == 0:
            return jsonify({
                "success": True
            })
        else:
            question_index = random.randrange(len(questions))
            return jsonify({
                "success": True,
                "question": questions[question_index].format()
            })

    '''
    Error handlers
    '''
    @app.errorhandler(400)
    def error_not_found(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def error_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not Found"
        }), 404

    @app.errorhandler(422)
    def error_not_found(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(500)
    def error_not_found(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    return app
