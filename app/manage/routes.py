from flask import render_template, url_for, redirect, request, flash, jsonify, send_from_directory
from os import path

from app.manage import bp
from app.extensions import db
from app.utils import LOGGER

from app.forms.flashcard_form import FlashcardForm
from app.forms.search_form import SearchForm
from app.models.flashcard_model import FlashcardModel, view_all_cards, view_all_categories

PATH = path.dirname(path.abspath(__file__))
IMAGE_FOLDER = path.join(PATH, "../uploads/images")

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
        form = SearchForm(request.form)
        if form.validate_on_submit(): 
            flashcards = view_all_cards(category=form.search.data)
        else:
            # Query database for all questions
            flashcards = view_all_cards(category=None)

        categories = view_all_categories()
        form = SearchForm(request.form)
        return render_template('./manage/manage_flashcards.html', nav_id="manage-page", flashcards=flashcards, categories=categories, form=form)
    
    except Exception as e:
        LOGGER.error(f"Failed to load manage flashcard page: {e}")
        categories = view_all_categories()
        return render_template('404.html', nav_id="home-page", categories=categories), 404

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
    available_options = view_all_categories()
    categories = [key for key in available_options]

    # Filter options based on the term
    matching_options = [option for option in categories if term.lower() in option.lower()]

    return jsonify(options=matching_options)

# ==============================================================================================================
@bp.route("/add_flashcard", methods=['GET', 'POST'])
def add_flashcard():
    '''
    Builds and returns an html page for adding flashcards to database. 
    NOTE: flashcard is added to the database in create_flashcard_route.

    Parameter(s): None

    Output(s):
        a built html page that enables users to add flashcards to the database
    '''
    try:
        form = FlashcardForm()
        if form.validate_on_submit():

            FlashcardModel(
                category=form.category.data,
                question=form.question.data,
                answer=form.answer.data,
                q_code_type=form.q_code_type.data,
                q_code_example=form.q_code_example.data,
                q_image_example=request.files.get('q_image_example'),
                a_code_type=form.a_code_type.data,
                a_code_example=form.a_code_example.data,
                a_image_example=request.files.get('a_image_example')
            )

            return redirect(url_for('manage.index'))
        
        categories = view_all_categories()
        return render_template('./manage/add_flashcard.html', nav_id="add-page", categories=categories, form=form)

    except Exception as e:
        LOGGER.error(f"An error occurred when adding flashcard: {e}")
        flash("Failed to add flashcard!", "error")
        return redirect(url_for('manage.index'))   

# ==============================================================================================================
@bp.route("/view_flashcard/<id>")
def view_flashcard(id):
    '''
    Builds and returns an html page based on the specified question.

    Parameter(s):
        id (int): the primary key of the question being queried

    Output(s):
        a built html page that displays the flashcard data
    '''
    try:
        # Query database for flashcard data
        flashcard = FlashcardModel.query.get(id)

        if not flashcard:
            LOGGER.error(f"Flashcard {id} not found!")
            categories = view_all_categories()
            return render_template('404.html', nav_id="home-page", categories=categories), 404

        categories = view_all_categories()

        return render_template('./manage/view_flashcard.html', nav_id="manage-page", flashcard=flashcard.view(), categories=categories)
    
    except Exception as e:
        LOGGER.error(f"An error occurred when trying to view flashcard {id}: {e}")
        return redirect(url_for('manage.index'))

# ==============================================================================================================
@bp.route("/edit_flashcard/<id>", methods=['GET', 'POST'])
def edit_flashcard(id):
    '''
    Builds and returns an html page based on the specified question category

    Parameter(s):
        key (int): the primary key of the question being edited

    Output(s):
        a built html page that displays the flashcard data for editing
    '''
    try:
        flashcard = FlashcardModel.query.get(id)

        if not flashcard:
            LOGGER.error(f"Flashcard {id} not found!")
            categories = view_all_categories()
            return render_template('404.html', nav_id="home-page", categories=categories), 404
        
        form = FlashcardForm()
        if form.validate_on_submit():

            # Get image input for question, set it to the old image if there is none
            q_image = request.files.get('q_image_example')
            if form.q_figure_type.data == 'image' and not q_image:
                q_image = form.q_old_image.data

            # Get image input for answer, set it to the old image if there is none
            a_image = request.files.get('a_image_example')
            if form.a_figure_type.data == 'image' and not a_image:
                a_image = form.a_old_image.data

            # Update flashcard data
            flashcard.update(
                category=form.category.data, 
                question=form.question.data, 
                answer=form.answer.data, 
                q_code_type=form.q_code_type.data,
                q_code_example=form.q_code_example.data,
                q_image_example=q_image, 
                a_code_type=form.a_code_type.data,
                a_code_example=form.a_code_example.data,
                a_image_example=a_image
            )

            LOGGER.info(f"Successfully edited flashcard: {id}")
            return redirect(url_for('manage.index'))

        categories = view_all_categories()
        return render_template('./manage/edit_flashcard.html', nav_id="manage-page", flashcard=flashcard.view(), categories=categories, form=form)
                    
    except Exception as e:
        db.session.rollback()
        LOGGER.error(f"An error occurred when editing flashcard: {e}")
        flash("Failed to edit flashcard!", "error")
        return redirect(url_for('manage.index'))          

# ==============================================================================================================
@bp.route("/delete_flashcard/<id>")
def delete_flashcard(id):
    '''
    Deletes the queried flashcard from the database and redirects to manage page

    Parameter(s):
        key (int): the primary key of the question being deleted from the database

    Output(s):
        None, redirects to the manage page
    '''
    try:
        # Query database for flashcard
        flashcard = FlashcardModel.query.get(id)

        if not flashcard:
            raise Exception(f"Flashcard {id} not found!")
        
        flashcard.delete()

        LOGGER.info(f"Flashcard question key {id} was successfully deleted!")
        flash("Flashcard was successfully deleted!", "success")
    
    except Exception as e:
        LOGGER.error(f'An Error occured when deleting the flashcard: {str(e)}')
        flash("Failed to delete flashcard!", 'error')
    
    return redirect(url_for('manage.index'))

# ==============================================================================================================
@bp.route('/get_image/<filename>')
def get_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)