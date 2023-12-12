from flask import Flask, request, redirect, render_template, url_for, flash

import os, sys
sys.path.append('./src/')
import utils #,database

LOGGER = utils.LOGGER
app = Flask(__name__, static_folder='static')
app.secret_key = 'my_super_secret_totaly_unbreakable_key'

# ==============================================================================================================
TEST_DATA = {"questions": [{"key": 1, "category": "<script>alert`1`</script>", "question": "<script>alert`1`</script>", "code": "<script>alert`1`</script>", "image": "NULL", "answer": "<script>alert`1`</script>"},
                           {"key": 2, "category": "category2", "question": "question2", "code": "NULL", "image": "NULL", "answer": "answer2"},
                           {"key": 3, "category": "category3", "question": "question3", "code": "NULL", "image": "NULL", "answer": "answer3"},
                           {"key": 4, "category": "category4", "question": "question4", "code": "NULL", "image": "NULL", "answer": "answer4"},
                           {"key": 5, "category": "category5", "question": "question5", "code": "NULL", "image": "NULL", "answer": "answer5"},
                           {"key": 6, "category": "category6", "question": "question6", "code": "NULL", "image": "NULL", "answer": "answer6"},
                           {"key": 7, "category": "category7", "question": "question7", "code": "NULL", "image": "NULL", "answer": "answer7"},
                           {"key": 8, "category": "category8", "question": "question8", "code": "NULL", "image": "NULL", "answer": "answer8"},
                           {"key": 9, "category": "category9", "question": "question9", "code": "NULL", "image": "NULL", "answer": "answer9"},
                           {"key": 10, "category": "category10", "question": "question10", "code": "NULL", "image": "NULL", "answer": "answer10"}]}

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
    # TODO: Query database for all categories and their counts
    # data = database.view_allcategories()

    data = {'categories': 2, 'test': 3, 'test2': 1}

    return render_template('home.html', nav_id="home-page", data=data)

# ==============================================================================================================
@app.route("/flashcards/<category>")
def flashcard_route(category):
    '''
    Builds and returns an html page based on the specified question category.

    Parameters:
        category (str): the type of questions being queried from the database

    Returns:
        a built html page that displays the flashcards
    '''
    # TODO: Query database for questions related to specified category
    # data = database.view_allcards(category=category)
    data=TEST_DATA

    return render_template('flashcards.html', nav_id="home-page", data=data, length=len(data['questions']))

# ==============================================================================================================
@app.route("/manage_flashcards")
def manage_flashcards_route():
    '''
    Builds and returns an html page where all the flashcard data can be viewed and edited.

    Parameters: None

    Returns:
        a built html page that displays the flashcard data
    '''
    # TODO: Query database for all questions
    # data = database.view_allcards(category=None)

    return render_template('manage_flashcards.html', nav_id="manage-page", data=TEST_DATA)

# ==============================================================================================================
@app.route("/add_flashcard")
def add_flashcard_route():
    '''
    Builds and returns an html page for adding flashcards to database. 
    NOTE: flashcard is added to the database in create_flashcard_route.

    Parameters: None

    Returns:
        a built html page that enables users to add flashcards to the database
    '''
    
    return render_template('add_flashcard.html', nav_id="add-page")

# ==============================================================================================================
@app.route("/create_flashcard", methods=['GET', 'POST'])
def create_flashcard_route():
    '''
    Builds and returns an html page based on the specified question category.

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
@app.route("/view_flashcard/<key>")
def view_flashcard_route(key):
    '''
    Builds and returns an html page based on the specified question.

    Parameters:
        key (int): the primary key of the question being queried

    Returns:
        a built html page that displays the flashcard data
    '''
    # TODO: Query database for question
    # data = database.view_card(key=key)
    
    return render_template('view_flashcard.html', nav_id="manage-page", data=TEST_DATA["questions"][0])

# ==============================================================================================================
@app.route("/edit_flashcard/<key>")
def edit_flashcard_route(key):
    '''
    Builds and returns an html page based on the specified question category

    Parameters:
        key (int): the primary key of the question being edited

    Returns:
        a built html page that displays the flashcard data for editing
    '''
    # TODO: Query database for question being edited
    # data = database.view_card(key=key)
    
    return render_template('edit_flashcard.html', nav_id="manage-page", data=TEST_DATA["questions"][0])

# ==============================================================================================================
@app.route("/update_flashcard/<key>", methods=['GET', 'POST'])
def update_flashcard_route(key):
    '''
    Builds and returns an html page based on the specified question category

    Parameters:
        key (int): the primary key of the question being edited

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
            LOGGER.info(f"Editing: {key}\n"
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
            # success = database.update_card(key=key, new_data=updated_data)
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
@app.route("/delete_flashcard/<key>")
def delete_flashcard_route(key):
    '''
    Deletes the queried flashcard from the database and redirects to manage page

    Parameters:
        key (int): the primary key of the question being deleted from the database

    Returns:
        None, redirects to the manage page
    '''
    try:
        # TODO: Query database for question and delete it
        # success = database.delete_card(key=key)
        success = True

        if success:
            LOGGER.info(f"Flashcard was successfully deleted!\nDeleted Question Key: {key}")
            flash("Flashcard was successfully deleted!", "success")
        else:
            LOGGER.info(f"Failed to delete flashcard!\nDeleted Question Key: {key}")
            flash("Failed to delete flashcard", "error")
    
    except Exception as e:
        LOGGER.error(f'An Error occured when deleting the flashcard: {str(e)}')
        flash("Failed to delete flashcard!", 'error')
    
    return redirect(url_for('manage_flashcards_route'))

# ==============================================================================================================
if __name__ == "__main__":
    app.run()