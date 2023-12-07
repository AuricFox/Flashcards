from flask import Flask, request, redirect, render_template, url_for, flash, jsonify

import os, sys, json
sys.path.append('./src/')
import utils

LOGGER = utils.LOGGER
app = Flask(__name__, static_folder='static')
app.secret_key = 'my_super_secret_totaly_unbreakable_key'

@app.route("/")
@app.route("/home")
def home():
    data = [('categories', 2), ('test', 3), ('test2', 1)]

    return render_template('home.html', nav_id="home-page", data=data)

#TODO: Manage Main Page, CRUD Pages

@app.route("/flashcards/<path:category>")
def flashcard_route(category):
    # Get all questions related to specified category
    data = {"questions": [{"question": "question1", "code": "code1", "image": "image1", "answer": "answer1"},
                          {"question": "question2", "code": "code2", "image": "image2", "answer": "answer2"}]}

    return render_template('flashcards.html', nav_id="home-page", data=data)


if __name__ == "__main__":
    app.run()