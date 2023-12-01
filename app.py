from flask import Flask, request, redirect, render_template, url_for, send_file, flash

import os, sys, logging

app = Flask(__name__, static_folder='static')
app.secret_key = 'my_super_secret_totaly_unbreakable_key'

PATH = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(
    filename=os.path.join(PATH, './output/app.log'),
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s'
)

LOGGER = logging.getLogger(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', active='')

#TODO: Manage Main Page, CRUD Pages

if __name__ == "__main__":
    app.run()