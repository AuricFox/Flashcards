import unittest
from flask.cli import FlaskGroup

import app
from app.utils import LOGGER
from app.extensions import db
from app.models.flashcard_model import FlashcardModel, FigureModel

cli = FlaskGroup(app)

@cli.command("init_database")
def init_database():
    """Initializes database and cleans up old tables"""
    try:
        print("Initializing Database ...")
        with app.app_context():
            db.drop_all()
            db.create_all()
            LOGGER.info(f"Successfully initialized the database!")
        return 0
    
    except Exception as e:
        LOGGER.error(f"An error occurred when initializing database: {e}")
        return 1
    
if __name__ == "__main__":
    cli()