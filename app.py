from flask import Flask, request, redirect, render_template, url_for, flash

import os, sys
sys.path.append('./src/')
import utils

LOGGER = utils.LOGGER
app = Flask(__name__, static_folder='static')
app.secret_key = 'my_super_secret_totaly_unbreakable_key'

# ==============================================================================================================
TEST_DATA = {"questions": [{"question": "question1", "code": "code1", "image": "image1", "answer": "answer1"},
                        {"question": "question2", "code": "code2", "image": "image2", "answer": "answer2"},
                        {"question": "question3", "code": "code3", "image": "image3", "answer": "answer3"},
                        {"question": "question4", "code": "code4", "image": "image4", "answer": "answer4"},
                        {"question": "question5", "code": "code5", "image": "image5", "answer": "answer5"},
                        {"question": "question6", "code": "code6", "image": "image6", "answer": "answer6"},
                        {"question": "question7", "code": "code7", "image": "image7", "answer": "answer7"},
                        {"question": "question8", "code": "code8", "image": "image8", "answer": "answer8"},
                        {"question": "question9", "code": "code9", "image": "image9", "answer": "answer9"},
                        {"question": "question10", "code": "code10", "image": "image10", "answer": "answer10"}]}

# ==============================================================================================================
@app.route("/")
@app.route("/home")
def home():
    data = [('categories', 2), ('test', 3), ('test2', 1)]

    return render_template('home.html', nav_id="home-page", data=data)

# ==============================================================================================================
@app.route("/flashcards/<path:category>")
def flashcard_route(category):
    # Get all questions related to specified category
    
    return render_template('flashcards.html', nav_id="home-page", data=TEST_DATA)

# ==============================================================================================================
@app.route("/manage_flashcards")
def manage_flashcards_route():

    return render_template('flashcards.html', nav_id="home-page", data=TEST_DATA)

#TODO: Manage Main Page, CRUD Pages

if __name__ == "__main__":
    app.run()