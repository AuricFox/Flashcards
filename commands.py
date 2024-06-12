import unittest, click
from flask.cli import FlaskGroup

import app
from app.utils import LOGGER, from_json
from app.extensions import db
from app.models.flashcard_model import FlashcardModel, FigureModel

cli = FlaskGroup(app)

@cli.command("clear_database")
def clear_database():
    """Initializes database and cleans up old tables"""
    try:
        print("Clearing Database ...")
        db.drop_all()

        print("Creating Tables ...")
        db.create_all()

        print("Successfully re-initialized the database!")
        LOGGER.info(f"Successfully re-initialized the database!")
        return 0
    
    except Exception as e:
        LOGGER.error(f"An error occurred when initializing database: {e}")
        return 1
# ============================================================================================================== 
@cli.command("create_database")
def init_database():
    """Initializes database by creating tables"""
    try:
        print("Creating Tables ...")
        db.create_all()

        print("Successfully initialized the database!")
        LOGGER.info(f"Successfully initialized the database!")
        return 0
    
    except Exception as e:
        LOGGER.error(f"An error occurred when initializing database: {e}")
        return 1
# ============================================================================================================== 
@cli.command("test")
def test():
    '''
    Runs all the unit tests
    '''
    tests = unittest.TestLoader().discover("tests")
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    if result.wasSuccessful():
        return 0
    else:
        return 1
# ============================================================================================================== 
@cli.command("test_routes")
@click.argument('route_name', required=False)
def test_routes(route_name):
    '''
    Runs the unit tests for routes: Main, Manage
    '''
    if not route_name:
        tests = unittest.TestLoader().discover("tests/test_routes")
    elif route_name == 'main':
        tests = unittest.TestLoader().discover("tests/test_routes", pattern="test_main_routes.py")
    elif route_name == 'manage':
        tests = unittest.TestLoader().discover("tests/test_routes", pattern="test_manage_routes.py")
    else:
        print(f"Invalid argument: {route_name}!")
        return 1
    
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    if result.wasSuccessful():
        return 0
    else:
        return 1
# ============================================================================================================== 
@cli.command("test_forms")
@click.argument('form_name', required=False)
def test_forms(form_name):
    '''
    Runs the unit tests for forms: FlashcardForm, SearchForm
    '''
    if not form_name:
        tests = unittest.TestLoader().discover("tests/test_forms")
    elif form_name == 'flashcard':
        tests = unittest.TestLoader().discover("tests/test_forms", pattern="test_flashcard_form.py")
    elif form_name == 'search':
        tests = unittest.TestLoader().discover("tests/test_forms", pattern="test_search_form.py")
    else:
        print(f"Invalid argument: {form_name}!")
        return 1
    
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    if result.wasSuccessful():
        return 0
    else:
        return 1
# ============================================================================================================== 
@cli.command("test_models")
@click.argument('model_name', required=False)
def test_models(model_name):
    '''
    Runs the unit tests for models: FlashcardModel, FigureModel
    '''
    if not model_name:
        tests = unittest.TestLoader().discover("tests/test_models")
    elif model_name == 'flashcard':
        tests = unittest.TestLoader().discover("tests/test_models", pattern="test_flashcard_model.py")
    elif model_name == 'figure':
        tests = unittest.TestLoader().discover("tests/test_models", pattern="test_figure_model.py")
    else:
        print(f"Invalid argument: {model_name}!")
        return 1
    
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    if result.wasSuccessful():
        return 0
    else:
        return 1
# ============================================================================================================== 
@cli.command("import_json")
@click.argument('filename', required=False)
def import_json(filename):
    '''
    Runs the unit tests for models: FlashcardModel, FigureModel
    '''
    try:
        if not filename:
            # NOTE: file must be in the data directory and named data.json
            print("Importing JSON File: data.json ...")
            LOGGER.info("Importing JSON File: data.json ...")
            data = from_json()
        else:
            print(f"Importing JSON File: {filename} ...")
            LOGGER.info(f"Importing JSON File: {filename} ...")
            data = from_json(filename=filename)

        for card in data:
            FlashcardModel(
                category=card['category'],
                question=card['question'],
                answer=card['answer'],
                q_code_type=card['q_code_type'],
                q_code_example=card['q_code_block'],
                a_code_type=card['a_code_type'],
                a_code_example=card['a_code_block'],
            )

        print(f"Successfully imported JSON file.")
        LOGGER.info(f"Successfully imported JSON file.")
        return 0
    
    except Exception as e:
        print(f"Failed to import JSON file: {e}")
        LOGGER.error(f"Failed to import JSON file: {e}")
        return 1



if __name__ == "__main__":
    cli()