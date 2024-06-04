from flask import render_template, url_for, redirect, request, flash, jsonify

from app.manage import bp
from app.extensions import db
from app.utils import LOGGER, process_figure, sanitize
from app.database import view_allcategories, view_allcards, view_card, add_card, update_card, delete_card

from app.forms.flashcard_form import FlashcardForm
from app.models.flashcard_model import FlashcardModel

# ==============================================================================================================
@bp.route("/", methods=['GET', 'POST'])
def index():
    '''
    Builds and returns an html page where all the flashcard data can be viewed and edited.

    Parameter(s): None

    Output(s):
        a built html page that displays the flashcard data
    '''
    try:
        if request.method == 'POST':
            category = request.form.get('search', type=str)
            data = view_allcards(category=category)

        else:
            # Query database for all questions
            data = view_allcards(category=None)

        categories = view_allcategories()
        return render_template('./manage/manage_flashcards.html', nav_id="manage-page", data=data, categories=categories)
    
    except Exception as e:
        LOGGER.error(f"Failed to load manage flashcard page: {e}")
        return render_template('404.html'), 404

# ==============================================================================================================
@bp.route('/autocomplete', methods=['GET'])
def autocomplete():
    '''
    Gets all the categories in the database and returns them for search options.

    Parameter(s): None

    Ouput(s):
        a json object with all the listed categories 
    '''

    term = request.args.get('search')

    # Get categories from the database
    available_options = view_allcategories()
    categories = [key for key in available_options]

    # Filter options based on the term
    matching_options = [option for option in categories if term.lower() in option.lower()]

    return jsonify(options=matching_options)

# ==============================================================================================================
@bp.route("/add_flashcard")
def add_flashcard():
    '''
    Builds and returns an html page for adding flashcards to database. 
    NOTE: flashcard is added to the database in create_flashcard_route.

    Parameter(s): None

    Output(s):
        a built html page that enables users to add flashcards to the database
    '''
    try:
        form = FlashcardForm(request.form)

        if form.validate_on_submit():

            new_flashcard = FlashcardModel(
                category=form.category.data,
                question=form.question.data,
                answer=form.answer.data,
                question_code_type=form.question_code_type.data,
                question_code_example=form.question_code_example.data,
                question_image_example=form.question_image_example,
                answer_code_type=form.answer_code_type.data,
                answer_code_example=form.answer_code_example.data,
                answer_image_example=form.answer_image_example
            )

            db.session.add(new_flashcard)
            db.session.commit()

            return redirect(url_for('manage.index'))
        
        return render_template('./manage/add_flashcard.html', nav_id="add-page", categories=view_allcategories(), form=form)

    except Exception as e:
        db.session.rollback()
        LOGGER.error(f"An error occurred when adding flashcard: {e}")
        flash("Failed to add flashcard!", "error")
        return redirect(url_for('manage.index'))   

# ==============================================================================================================
@bp.route("/create_flashcard", methods=['GET', 'POST'])
def create_flashcard():
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
            data['category'] = sanitize(request.form.get('category', type=str))
            data['question'] = request.form.get('question', type=str)
            data['answer'] = request.form.get('answer', type=str)

            data['q_code_block'], data['q_code_type'], data['q_image_file'] = process_figure(request, 'q')
            data['a_code_block'], data['a_code_type'], data['a_image_file'] = process_figure(request, 'a')

            LOGGER.info(f"Adding flashcard data:\n"
                        f"Category: {data['category']}\n"
                        f"Question: {data['question']}\n"
                        f"Answer: {data['answer']}\n"
                        f"Question Code Block: {data['q_code_block']}\n"
                        f"Question Code Type: {data['q_code_type']}\n"
                        f"Question Image File: {data['q_image_file']}\n"
                        f"Answer Code Block: {data['a_code_block']}\n"
                        f"Answer Code Type: {data['a_code_type']}\n"
                        f"Answer Image File: {data['a_image_file']}")

            # Update old question data with new data
            success = add_card(data=data)

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
        return redirect(url_for('create_flashcard'))
    
# ==============================================================================================================
@bp.route("/view_flashcard/<key>")
def view_flashcard(key):
    '''
    Builds and returns an html page based on the specified question.

    Parameter(s):
        key (int): the primary key of the question being queried

    Output(s):
        a built html page that displays the flashcard data
    '''
    # Query database for question
    data = view_card(key=key)
    categories = view_allcategories()
    
    return render_template('./manage/view_flashcard.html', nav_id="manage-page", data=data, categories=categories)

# ==============================================================================================================
@bp.route("/edit_flashcard/<key>")
def edit_flashcard(key):
    '''
    Builds and returns an html page based on the specified question category

    Parameter(s):
        key (int): the primary key of the question being edited

    Output(s):
        a built html page that displays the flashcard data for editing
    '''
    # Query database for question being edited
    data = view_card(key=key)
    categories = view_allcategories()
    
    return render_template('./manage/edit_flashcard.html', nav_id="manage-page", data=data, categories=categories)

# ==============================================================================================================
@bp.route("/update_flashcard/<key>", methods=['GET', 'POST'])
def update_flashcard(key):
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
            data['category'] = sanitize(request.form.get('category', type=str))
            data['question'] = request.form.get('question', type=str)
            data['answer'] = request.form.get('answer', type=str)

            data['q_code_block'], data['q_code_type'], data['q_image_file'] = process_figure(request, 'q')
            data['a_code_block'], data['a_code_type'], data['a_image_file'] = process_figure(request, 'a')

            LOGGER.info(f"Editing: {data['key']}\n"
                        f"Category: {data['category']}\n"
                        f"Question: {data['question']}\n"
                        f"Answer: {data['answer']}\n"
                        f"Question Code Block: {data['q_code_block']}\n"
                        f"Question Code Type: {data['q_code_type']}\n"
                        f"Question Image File: {data['q_image_file']}\n"
                        f"Answer Code Block: {data['a_code_block']}\n"
                        f"Answer Code Type: {data['a_code_type']}\n"
                        f"Answer Image File: {data['a_image_file']}")

            # Update old question data with new data
            success = update_card(data=data)

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
        return redirect(url_for('manage_flashcards'))

# ==============================================================================================================
@bp.route("/delete_flashcard/<key>")
def delete_flashcard(key):
    '''
    Deletes the queried flashcard from the database and redirects to manage page

    Parameter(s):
        key (int): the primary key of the question being deleted from the database

    Output(s):
        None, redirects to the manage page
    '''
    try:
        # Query database for question and delete it
        success = delete_card(key=key)

        if success:
            LOGGER.info(f"Flashcard question key {key} was successfully deleted!")
            flash("Flashcard was successfully deleted!", "success")
        else:
            LOGGER.info(f"Failed to delete flashcard question key {key}!")
            flash("Failed to delete flashcard", "error")
    
    except Exception as e:
        LOGGER.error(f'An Error occured when deleting the flashcard: {str(e)}')
        flash("Failed to delete flashcard!", 'error')
    
    return redirect(url_for('manage_flashcards'))