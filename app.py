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
    return render_template('home.html', active='')

#TODO: Manage Main Page, CRUD Pages

if __name__ == "__main__":
    app.run()