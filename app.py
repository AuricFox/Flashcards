from flask import Flask, request, redirect, render_template, url_for, send_file, flash

import os, sys
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
    return render_template('home.html', nav_id="home-page")


if __name__ == "__main__":
    app.run()