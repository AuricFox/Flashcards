from flask import render_template, url_for, redirect, request, flash

from app.main import bp
from app.utils import LOGGER
from app.database import view_allcategories, view_allcards

# ==============================================================================================================
@bp.route("/")
@bp.route("/home")
def index():
    '''
    Builds and returns an html page that displays the categories and the number of questions in 
    each category.

    Parameter(s): None

    Output(s):
        a built html page that displays the categories and their count
    '''
    # Query database for all categories and their counts
    categories = view_allcategories()

    return render_template('home.html', nav_id="home-page", categories=categories)

# ==============================================================================================================
@bp.route("/flashcards/<category>")
def flashcard(category):
    '''
    Builds and returns an html page based on the specified question category.

    Parameter(s):
        category (str): the type of questions being queried from the database

    Output(s):
        a built html page that displays the flashcards
    '''
    # Query database for questions related to specified category
    data = view_allcards(category=category)
    length = len(data['questions'])

    categories = view_allcategories()

    return render_template('flashcards.html', nav_id="flashcard-page", data=data, length=length, categories=categories)