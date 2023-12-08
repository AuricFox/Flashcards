from flask import Flask, request, redirect, render_template, url_for, flash

import os, sys
sys.path.append('./src/')
import utils

LOGGER = utils.LOGGER
app = Flask(__name__, static_folder='static')
app.secret_key = 'my_super_secret_totaly_unbreakable_key'

# ==============================================================================================================
TEST_DATA = {"questions": [{"category": "category1", "question": "question1", "code": "code1", "image": "image1", "answer": "answer1"},
                        {"category": "category2", "question": "question2", "code": "code2", "image": "image2", "answer": "answer2"},
                        {"category": "category3", "question": "question3", "code": "code3", "image": "image3", "answer": "answer3"},
                        {"category": "category4", "question": "question4", "code": "code4", "image": "image4", "answer": "answer4"},
                        {"category": "category5", "question": "question5", "code": "code5", "image": "image5", "answer": "answer5"},
                        {"category": "category6", "question": "question6", "code": "code6", "image": "image6", "answer": "answer6"},
                        {"category": "category7", "question": "question7", "code": "code7", "image": "image7", "answer": "answer7"},
                        {"category": "category8", "question": "question8", "code": "code8", "image": "image8", "answer": "answer8"},
                        {"category": "category9", "question": "question9", "code": "code9", "image": "image9", "answer": "answer9"},
                        {"category": "category10", "question": "question10", "code": "code10", "image": "image10", "answer": "answer10"}]}

# ==============================================================================================================
@app.route("/")
@app.route("/home")
def home():
    '''
    Builds and returns an html page that displays the categories and the number of questions in 
    each category.

    Parameters: None

    Returns:
        a built html page that displays the categories and their count
    '''
    # TODO: Query database for categories

    data = {'categories': 2, 'test': 3, 'test2': 1}

    return render_template('home.html', nav_id="home-page", data=data)

# ==============================================================================================================
@app.route("/flashcards/<path:category>")
def flashcard_route(category):
    '''
    Builds and returns an html page based on the specified question category

    Parameters:
        category (str): the type of questions being queried for the flashcards

    Returns:
        a built html page that displays the flashcards
    '''
    # TODO: Query database for questions related to specified category
    
    return render_template('flashcards.html', nav_id="home-page", data=TEST_DATA)

# ==============================================================================================================
@app.route("/manage_flashcards")
def manage_flashcards_route():
    '''
    Builds and returns an html page where all the flashcard data can be viewed and edited

    Parameters: None

    Returns:
        a built html page that displays the flashcard data
    '''
    # TODO: Query database for all questions

    return render_template('manage_flashcards.html', nav_id="manage-page", data=TEST_DATA)

# ==============================================================================================================
#TODO: Manage Main Page, CRUD Pages
# ==============================================================================================================
@app.route("/view_flashcard/<path:question>")
def view_flashcard_route(question):
    '''
    Builds and returns an html page based on the specified question

    Parameters:
        question (str): the question being queried

    Returns:
        a built html page that displays the flashcard data
    '''
    # TODO: Query database for question
    data = {"category": "category1", "question": "question1", "code": "code1", "image": "image1", "answer": "answer1"}
    
    return render_template('view_flashcard.html', nav_id="manage-page", data=data)

# ==============================================================================================================
@app.route("/edit_flashcard/<path:question>")
def edit_flashcard_route(question):
    '''
    Builds and returns an html page based on the specified question category

    Parameters:
        question (str): the question being edited

    Returns:
        a built html page that displays the flashcard data for editing
    '''
    # TODO: Query database for question and edit it
    data = {"category": "category1", "question": "question1", "code": "code1", "image": "image1", "answer": "answer1"}
    
    return render_template('edit_flashcard.html', nav_id="manage-page", data=data)

# ==============================================================================================================
@app.route("/update_flashcard/<question>", methods=['GET', 'POST'])
def update_flashcard_route(question):
    '''
    Builds and returns an html page based on the specified question category

    Parameters:
        question (str): the question being edited

    Returns:
        None, redirects to manage_flashcard page
    '''
    try:
        updated_data = {}

        if request.method == 'POST':
            # Retrieve updated data from the form
            updated_data['category'] = request.form['category']
            updated_data['question'] = request.form['question']
            updated_data['code'] = request.form['code']
            updated_data['answer'] = request.form['answer']
            # TODO: Process image file
            updated_data['image'] = request.form['image']

            # TODO:Update old question data with new data
            # success = database.update_card(old_question=question, new_data=updated_data)
            success = True

            if success:
                flash("Flashcard updated successfully", "success")
                return redirect(url_for('manage_flashcards_route'))
            else:
                flash("Failed to update flashcard", "error")

        return redirect(url_for('manage_flashcards_route'))
    
    except Exception as e:
        flash(f'An Error occured: {str(e)}', 'error')
        redirect(url_for('manage_flashcards_route'))

# ==============================================================================================================
@app.route("/delete_flashcard/<path:question>")
def delete_flashcard_route(question):
    '''
    Builds and returns an html page based on the specified question category

    Parameters:
        question (str): the question being deleted from the database

    Returns:
        None, redirects to the manage page
    '''
    # TODO: Query database for question and delete it
    
    return render_template('manage_flashcards.html', nav_id="manage-page", data=TEST_DATA)

if __name__ == "__main__":
    app.run()