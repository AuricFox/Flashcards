from flask import Flask, request, redirect, render_template, url_for, flash

import os, sys
sys.path.append('./src/')
import utils ,database

LOGGER = utils.LOGGER
app = Flask(__name__, static_folder='static')
app.secret_key = 'my_super_secret_totaly_unbreakable_key'

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
    # Query database for all categories and their counts
    categories = database.view_allcategories()

    return render_template('home.html', nav_id="home-page", categories=categories)

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
    # Query database for questions related to specified category
    data = database.view_allcards(category=category)
    length = len(data['questions'])

    categories = database.view_allcategories()

    return render_template('flashcards.html', nav_id="flashcard-page", data=data, length=length, categories=categories)

# ==============================================================================================================
@app.route("/manage_flashcards", methods=['GET', 'POST'])
def manage_flashcards_route():
    '''
    Builds and returns an html page where all the flashcard data can be viewed and edited.

    Parameters: None

    Returns:
        a built html page that displays the flashcard data
    '''
    if request.method == 'POST':
        category = request.form.get('search', type=str)
        data = database.view_allcards(category=category)

    else:
        # Query database for all questions
        data = database.view_allcards(category=None)
    
    categories = database.view_allcategories()

    return render_template('manage_flashcards.html', nav_id="manage-page", data=data, categories=categories)

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

    categories = database.view_allcategories()
    
    return render_template('add_flashcard.html', nav_id="add-page", categories=categories)

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

        if request.method == 'POST':
            # Retrieve main card elements from the form
            category = utils.sanitize(request.form.get('category', type=str))
            question = request.form.get('question', type=str)
            answer = request.form.get('answer', type=str)

            code_or_image = request.form.get('input-type', type=str)

            # Process image file
            if code_or_image == 'image':
                # Get file data from form and save it
                file = request.files['image-ex']
                image_file = utils.save_image_file(file)

                # Set code elements to none, user can only have an image or code not both
                code = None
                code_type = None

                # Incorrect file was submitted or file failed to save
                if image_file is None:
                    LOGGER.error(f'{file.filename} is an Invalid File or FileType')
                    flash(f'{file.filename} is an Invalid File or FileType', 'error')
                    return redirect(request.referrer)
            
            # Process code elements
            elif code_or_image == 'code':
                code = request.form.get('code-ex', str)
                code_type = request.form.get('code-type', str)
                image_file = None

            # No code or images used
            else:
                code = None
                code_type = None
                image_file = None
            
            LOGGER.info(f"Adding flashcard data:\n"
                        f"Category: {category}\n"
                        f"Question: {question}\n"
                        f"Answer: {answer}\n"
                        f"Code: {code}\n"
                        f"Code Type: {code_type}\n"
                        f"Image File: {image_file}")

            # Update old question data with new data
            success = database.add_card(
                category=category, 
                question=question, 
                answer=answer, 
                code=code,
                code_type=code_type,
                image_file=image_file
                )

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
    # Query database for question
    data = database.view_card(key=key)
    categories = database.view_allcategories()
    
    return render_template('view_flashcard.html', nav_id="manage-page", data=data, categories=categories)

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
    # Query database for question being edited
    data = database.view_card(key=key)
    categories = database.view_allcategories()
    
    return render_template('edit_flashcard.html', nav_id="manage-page", data=data, categories=categories)

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

        if request.method == 'POST':
            # Retrieve main card elements from the form
            category = utils.sanitize(request.form.get('category', type=str))
            question = request.form.get('question', type=str)
            answer = request.form.get('answer', type=str)

            code_or_image = request.form.get('input-type', type=str)

            # Process image file
            if code_or_image == 'image':
                # Get file data from form and save it
                file = request.files['image-ex']
                image_file = utils.save_image_file(file)

                # Set code elements to none, user can only have an image or code not both
                code = None
                code_type = None

                # Incorrect file was submitted or file failed to save
                if image_file is None:
                    LOGGER.error(f'{file.filename} is an Invalid File or FileType')
                    flash(f'{file.filename} is an Invalid File or FileType', 'error')
                    return redirect(request.referrer)
            
            # Process code elements
            elif code_or_image == 'code':
                code = request.form.get('code-ex', str)
                code_type = request.form.get('code-type', str)
                image_file = None

            # No code or images used
            else:
                code = None
                code_type = None
                image_file = None
            
            LOGGER.info(f"Editing: {key}\n"
                        f"Category: {category}\n"
                        f"Question: {question}\n"
                        f"Answer: {answer}\n"
                        f"Code: {code}\n"
                        f"Code Type: {code_type}\n"
                        f"Image File: {image_file}")

            # Update old question data with new data
            success = database.update_card(
                key=key, 
                category=category,
                question=question,
                answer=answer,
                code=code,
                code_type=code_type,
                image_file=image_file
                )

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
        # Query database for question and delete it
        success = database.delete_card(key=key)

        if success:
            LOGGER.info(f"Flashcard question key {key} was successfully deleted!")
            flash("Flashcard was successfully deleted!", "success")
        else:
            LOGGER.info(f"Failed to delete flashcard question key {key}!")
            flash("Failed to delete flashcard", "error")
    
    except Exception as e:
        LOGGER.error(f'An Error occured when deleting the flashcard: {str(e)}')
        flash("Failed to delete flashcard!", 'error')
    
    return redirect(url_for('manage_flashcards_route'))

# ==============================================================================================================
if __name__ == "__main__":
    app.run()