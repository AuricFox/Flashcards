from flask import Flask, request, redirect, render_template, url_for, send_file, flash

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
    data = json.dumps([("category1", "question1", "code1", "image1", "answer1"),
            ("category2", "question2", "code2", "image2", "answer2")])

    return render_template('flashcards.html', nav_id="home-page", data=data)


if __name__ == "__main__":
    app.run()