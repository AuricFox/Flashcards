from flask import Flask, request, redirect, render_template, url_for, flash

import os, sys
sys.path.append('./src/')
import utils

LOGGER = utils.LOGGER
app = Flask(__name__, static_folder='static')
app.secret_key = 'my_super_secret_totaly_unbreakable_key'

# ==============================================================================================================
TEST_DATA = {"questions": [{"category": "category1", "question": "question1", "code": "NULL", "image": "NULL", "answer": "answer1"},
                        {"category": "category2", "question": "question2", "code": "NULL", "image": "NULL", "answer": "answer2"},
                        {"category": "category3", "question": "question3", "code": "NULL", "image": "NULL", "answer": "answer3"},
                        {"category": "category4", "question": "question4", "code": "NULL", "image": "NULL", "answer": "answer4"},
                        {"category": "category5", "question": "question5", "code": "NULL", "image": "NULL", "answer": "answer5"},
                        {"category": "category6", "question": "question6", "code": "NULL", "image": "NULL", "answer": "answer6"},
                        {"category": "category7", "question": "question7", "code": "NULL", "image": "NULL", "answer": "answer7"},
                        {"category": "category8", "question": "question8", "code": "NULL", "image": "NULL", "answer": "answer8"},
                        {"category": "category9", "question": "question9", "code": "NULL", "image": "NULL", "answer": "answer9"},
                        {"category": "category10", "question": "question10", "code": "NULL", "image": "NULL", "answer": "answer10"}]}

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
@app.route("/flashcards/<category>")
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
@app.route("/add_flashcard")
def add_flashcard_route():
    '''
    Builds and returns an html page for adding flashcards to database

    Parameters: None

    Returns:
        a built html page that enables users to add flashcards to the database
    '''
    
    return render_template('add_flashcard.html', nav_id="add-page")

# ==============================================================================================================
@app.route("/create_flashcard", methods=['GET', 'POST'])
def create_flashcard_route():
    '''
    Builds and returns an html page based on the specified question category

    Parameters:
        question (str): the question being edited

    Returns:
        None, redirects to manage_flashcard page
    '''
    try:
        data = {}

        if request.method == 'POST':
            # Retrieve updated data from the form
            data['category'] = request.form.get('category', type=str)
            data['question'] = request.form.get('question', type=str)
            data['code'] = request.form.get('code', type=str)
            data['answer'] = request.form.get('answer', type=str)
            
            # Get file data from form
            file = request.files['image']
            # Save file and get filename
            data['image'] = 'NULL' if not file or file.filename == 'NULL' else 'NULL'
            LOGGER.info(f"Adding flashcard data:\n"
                        f"Category: {data['category']}\n"
                        f"Question: {data['question']}\n"
                        f"Code: {data['code']}\n"
                        f"Answer: {data['answer']}\n"
                        f"Image File: {data['image']}")

            # Incorrect file was submitted or file failed to save
            if data['image'] is None:
                LOGGER.error(f'{file.filename} is an Invalid File or FileType')
                flash(f'{file.filename} is an Invalid File or FileType', 'error')
                return redirect(request.referrer)

            # TODO:Update old question data with new data
            '''
            success = database.add_card(
                category=data['category'], 
                question=data['question'], 
                answer=data['answer'], 
                code=data['code'], 
                image=data['image'])
            '''
            success = True

            if success:
                LOGGER.info("Flashcard added successfully")
                flash("Flashcard added successfully", "success")
                return redirect(url_for('manage_flashcards_route'))
            else:
                LOGGER.error("Failed to add flashcard")
                flash("Failed to add flashcard", "error")

        return redirect(url_for('manage_flashcards_route'))
    
    except Exception as e:
        LOGGER.error(f'An Error occured when adding the flashcard: {str(e)}')
        flash("Failed to add flashcard", 'error')
        return redirect(url_for('manage_flashcards_route'))

# ==============================================================================================================
@app.route("/view_flashcard/<question>")
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
@app.route("/edit_flashcard/<question>")
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
            updated_data['category'] = request.form.get('category', type=str)
            updated_data['question'] = request.form.get('question', type=str)
            updated_data['code'] = request.form.get('code', type=str)
            updated_data['answer'] = request.form.get('answer', type=str)
            
            # Get file data from form
            file = request.files['image']
            # Save file and get filename
            updated_data['image'] = 'NULL' if not file or file.filename == 'NULL' else 'NULL'
            LOGGER.info(f"Editing: {question}\n"
                        f"Category: {updated_data['category']}\n"
                        f"Question: {updated_data['question']}\n"
                        f"Code: {updated_data['code']}\n"
                        f"Answer: {updated_data['answer']}\n"
                        f"Image File: {updated_data['image']}")

            # Incorrect file was submitted or file failed to save
            if updated_data['image'] is None:
                LOGGER.error(f'{file.filename} is an Invalid File or FileType')
                flash(f'{file.filename} is an Invalid File or FileType', 'error')
                return redirect(request.referrer)

            # TODO:Update old question data with new data
            # success = database.update_card(old_question=question, new_data=updated_data)
            success = True

            if success:
                LOGGER.info("Flashcard updated successfully")
                flash("Flashcard updated successfully", "success")
                return redirect(url_for('manage_flashcards_route'))
            else:
                LOGGER.error("Failed to update flashcard")
                flash("Failed to update flashcard", "error")

        return redirect(url_for('manage_flashcards_route'))
    
    except Exception as e:
        LOGGER.error(f'An Error occured when updating the flashcard: {str(e)}')
        flash("Failed to update flashcard", 'error')
        return redirect(url_for('manage_flashcards_route'))

# ==============================================================================================================
@app.route("/delete_flashcard/<question>")
def delete_flashcard_route(question):
    '''
    Deletes the queried flashcard from the database and redirects to manage page

    Parameters:
        question (str): the question being deleted from the database

    Returns:
        None, redirects to the manage page
    '''
    try:
        # TODO: Query database for question and delete it
        # success = database.delete_card(question=question)
        success = True

        if success:
            LOGGER.info("Flashcard was successfully deleted!")
            flash("Flashcard was successfully deleted!", "success")
        else:
            LOGGER.info("Failed to delete flashcard!")
            flash("Failed to delete flashcard", "error")
    
    except Exception as e:
        LOGGER.error(f'An Error occured when deleting the flashcard: {str(e)}')
        flash("Failed to delete flashcard!", 'error')
    
    return redirect(url_for('manage_flashcards_route'))

# ==============================================================================================================
if __name__ == "__main__":
    app.run()