from flask import Flask, request, redirect, render_template, url_for, flash, jsonify

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

    Parameter(s): None

    Output(s):
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

    Parameter(s):
        category (str): the type of questions being queried from the database

    Output(s):
        a built html page that displays the flashcards
    '''
    # Query database for questions related to specified category
    data = database.view_allcards(category=category)
    length = len(data['questions'])

    categories = database.view_allcategories()

    return render_template('flashcards.html', nav_id="flashcard-page", data=data, length=length, categories=categories)

# ==============================================================================================================
@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    '''
    Gets all the categories in the database and returns them for search options.

    Parameter(s): None

    Ouput(s):
        a json object with all the listed categories 
    '''

    term = request.args.get('search')

    # Get categories from the database
    available_options = database.view_allcategories()
    categories = [key for key in available_options]

    # Filter options based on the term
    matching_options = [option for option in categories if term.lower() in option.lower()]

    return jsonify(options=matching_options)

# ==============================================================================================================
@app.route("/manage_flashcards", methods=['GET', 'POST'])
def manage_flashcards_route():
    '''
    Builds and returns an html page where all the flashcard data can be viewed and edited.

    Parameter(s): None

    Output(s):
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

    Parameter(s): None

    Output(s):
        a built html page that enables users to add flashcards to the database
    '''

    categories = database.view_allcategories()
    
    return render_template('add_flashcard.html', nav_id="add-page", categories=categories)

# ==============================================================================================================
def process_figure_upload(request, f):
    try:
        figure_type = request.form.get(f'{f}-figure-type', type=str)

        # Process image figure
        if figure_type == 'image':
            # Get new image file
            file = request.files[f'{f}-image-figure']
            # Check for old image filename
            old_file = request.form.get(f'current-{f}-image', str)

            if file: image_file = utils.save_image_file(file)
            elif old_file: image_file = old_file
            else:
                LOGGER.error('Invalid File or FileType Entered!')
                flash('Invalid File or FileType Entered', 'error')
                return None
            
            return (None, None, image_file)
        
        # Process code figure
        elif figure_type == 'code':
            code_block = request.form.get(f'{f}-code-figure', str)
            code_type = request.form.get(f'{f}-code-type', str)

            return (code_block, code_type, None)
        
        # No figure to process
        else:
            return (None, None, None)
        
    except Exception as e:
        LOGGER.error(f"Error processing {figure_type} upload: {str(e)}")
        flash(f"Error processing {figure_type} upload", 'error')
        return None

# ==============================================================================================================
@app.route("/create_flashcard", methods=['GET', 'POST'])
def create_flashcard_route():
    '''
    Builds and returns an html page based on the specified question category.

    Parameter(s):
        question (str): the question being edited

    Output(s):
        None, redirects to manage_flashcard page
    '''
    try:

        if request.method == 'POST':
            data = {}
            # Retrieve main card elements from the form
            data['category'] = utils.sanitize(request.form.get('category', type=str))
            data['question'] = request.form.get('question', type=str)
            data['answer'] = request.form.get('answer', type=str)

            data['q_code_block'], data['q_code_type'], data['q_image_file'] = process_figure_upload(request, 'q')
            data['a_code_block'], data['a_code_type'], data['a_image_file'] = process_figure_upload(request, 'a')

            LOGGER.info(f"Adding flashcard data:\n"
                        f"Category: {data['category']}\n"
                        f"Question: {data['question']}\n"
                        f"Answer: {data['answer']}\n"
                        f"Question Code lock: {data['q_code_block']}\n"
                        f"Question Code Type: {data['q_code_type']}\n"
                        f"Question Image File: {data['q_image_file']}\n"
                        f"Answer Code lock: {data['a_code_block']}\n"
                        f"Answer Code Type: {data['a_code_type']}\n"
                        f"Answer Image File: {data['a_image_file']}")

            # Update old question data with new data
            success = database.add_card(data=data)

            if success:
                LOGGER.info("Flashcard added successfully")
                flash("Flashcard added successfully", "success")
                return redirect(url_for('manage_flashcards_route'))
            else:
                LOGGER.error("Failed to add flashcard")
                flash("Failed to add flashcard", "error")

        return redirect(url_for('create_flashcard_route'))
    
    except Exception as e:
        LOGGER.error(f'An Error occured when adding the flashcard: {str(e)}')
        flash("Failed to add flashcard", 'error')
        return redirect(url_for('create_flashcard_route'))

# ==============================================================================================================
@app.route("/view_flashcard/<key>")
def view_flashcard_route(key):
    '''
    Builds and returns an html page based on the specified question.

    Parameter(s):
        key (int): the primary key of the question being queried

    Output(s):
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

    Parameter(s):
        key (int): the primary key of the question being edited

    Output(s):
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

    Parameter(s):
        key (int): the primary key of the question being edited

    Output(s):
        None, redirects to manage_flashcard page
    '''
    try:

        if request.method == 'POST':
            data = {}
            # Retrieve main card elements from the form
            data['key'] = key
            data['category'] = utils.sanitize(request.form.get('category', type=str))
            data['question'] = request.form.get('question', type=str)
            data['answer'] = request.form.get('answer', type=str)

            data['q_code_block'], data['q_code_type'], data['q_image_file'] = process_figure_upload(request, 'q')
            data['a_code_block'], data['a_code_type'], data['a_image_file'] = process_figure_upload(request, 'a')


            LOGGER.info(f"Editing: {data['key']}\n"
                        f"Category: {data['category']}\n"
                        f"Question: {data['question']}\n"
                        f"Answer: {data['answer']}\n"
                        f"Question Code lock: {data['q_code_block']}\n"
                        f"Question Code Type: {data['q_code_type']}\n"
                        f"Question Image File: {data['q_image_file']}\n"
                        f"Answer Code lock: {data['a_code_block']}\n"
                        f"Answer Code Type: {data['a_code_type']}\n"
                        f"Answer Image File: {data['a_image_file']}")

            # Update old question data with new data
            success = database.update_card(data=data)

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

    Parameter(s):
        key (int): the primary key of the question being deleted from the database

    Output(s):
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