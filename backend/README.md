# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

* [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

* [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

* [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
createdb trivia
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Reference
### Getting Started
The backend app is hosted at the default URL `http://127.0.0.1:5000`

### Error Handling
Errors are returned as JSON object in the following format
```
{
    "success": False,
    "error": 400,
    "message": "Bad Request"
}
```
The API will return three error types when the requests fail
* 400 Bad Request
* 404 Not Found
* 422 Unprocessable

### GET `"/api/categories"`
* Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
* Request Arguments: None
* Returns: 
    
    success: Boolean value indicating the request was successful
    
    categories: An object with a single key, categories, that contains a object of id: category_string key:value pairs
```
{
    "success": True,
    "categories": {
        "1" : "Science",
        "2" : "Art",
        "3" : "Geography",
        "4" : "History",
        "5" : "Entertainment",
        "6" : "Sports"
    }
}
```

### GET `"/api/questions"`
* Fetches all questions, including pagination (every 10 questions)
* Request Arguments:
    
    page: Integer indicating the range of questions to get
* Returns: 
    
    success: Boolean value indicating the request was successful
    
    questions: A collection of questions (max 10)
    
    total_questions: An Integer indication total number of questions
    
    categories: An object with a single key, categories, that contains a object of id: category_string key:value pairs
    
    current_category: An empty object indicating that current category is not specified
```
{
    "success": True,
    "questions": [{
        "id": 2, 
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
        "answer": "Apollo 13", 
        "category": 5, 
        "difficulty": 4        
    }, 
    {
        "id": 4, 
        "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
        "answer": "Tom Cruise", 
        "category": 5, 
        "difficulty": 4        
    },
    {
        "id": 20, 
        "question": "What is the heaviest organ in the human body?",
        "answer": "The Liver", 
        "category": 1, 
        "difficulty": 4        
    }],
    "total_questions": 3,
    "categories": {
        "1" : "Science",
        "2" : "Art",
        "3" : "Geography",
        "4" : "History",
        "5" : "Entertainment",
        "6" : "Sports"
    },
    "current_category": {}
}
```

### POST `"/api/questions"`
##### Create a new question
* Request Arguments: None
* Request Body:
    
    question: String value of the question
    
    answer: String value of the answer
    
    difficulty: String value inidicating the question's difficulty
    
    category: String value indidcating the category this question belongs to
```
{
    "question": "Who discovered gravity?",
    "answer": "Newton",
    "difficulty": "3",
    "category": "1",
}
```
- Returns: 
    
    success: Boolean value indicating the request was successful
```
{
    "success": True
}
```

#####  Get questions based on a search term (case insensitive)
* Request Arguments: None
* Request Body:
    
    searchTerm: Case insensitive string value to search for
```
{
    "searchTerm": "title"
}
```
* Returns: 
    
    success: Boolean value indicating the request was successful
    
    current_category: An empty object indicating that it's searching across all categories
    
    questions: A collection of questions
    
    total_questions: An Integer indication total number of questions
```
{
    "success": True,
    "current_category": {}, 
    "questions": [{
        "id": 5, 
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
        "answer": "Maya Angelou", 
        "category": 4, 
        "difficulty": 2
    }, 
    {
        "id": 6, 
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?",
        "answer": "Edward Scissorhands", 
        "category": 5, 
        "difficulty": 3
    }], 
    "total_questions": 2
}
```

### GET `"/api/categories/<int:category_id>/questions"`
* Fetches all questions in the given category, including pagination (every 10 questions)
* Request Arguments:
    page: Integer indicating the range of questions to get
* Request variable: Integer value indicating the category ID
* Returns: 
    
    success: Boolean value indicating the request was successful
    
    questions: A collection of questions (max 10)
    
    total_questions: An Integer indication total number of questions
    
    current_category: A Category object indicating the current category
```
{
    "success": True,
    "questions": [{
        "id": 20, 
        "question": "What is the heaviest organ in the human body?",
        "answer": "The Liver", 
        "category": 1, 
        "difficulty": 4, 
    }],
    "total_questions": 1,
    "current_category": {
        "id": 1, 
        "type": "Science"
    }
}
```

### DELETE `"/api/questions/<int:question_id>"`
* Removes the given question from the database
* Request Arguments: None
* Request variable: Integer value indicating the question ID
* Returns: 

    success: Boolean value indicating the request was successful

    question_id: ID of the question deleted
```
{
    "success": True,
    "question_id": 10
}
```

### POST `"/api/quizzes"`
* Fetch questions in a category to play the quiz
* Request Arguments: None
* Request Body:

    previous_questions: A collection of question IDs that have been answered
    
    quiz_category: A Category object indicating the current category
```
{
    "previous_questions": [22],
    "quiz_category": {
        "id": "1",
        "type": "Science"
    }
}
```

* Returns:

    success: Boolean value indicating the request was successful
    
    question: A question to be answered
```
{
    "success": true,
    "question": {
        "id": 26, 
        "question": "What's the acceleration of gravity? (m/s^2)",
        "answer": "9.81", 
        "category": 1, 
        "difficulty": 3        
    }
}
```
