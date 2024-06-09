from flask_testing import TestCase

from app import init_app

from app.utils import remove_image
from app.extensions import db
from app.models.flashcard_model import FlashcardModel, FigureModel


class BaseTestCase(TestCase):
    '''
    Creates a base test class for test cases
    '''
    def create_app(self):
        # Create and configure the app for testing
        app = init_app('config.TestingConfig')
        return app

    def setUp(self):
        # Set up the database
        self.client = self.app.test_client()
        db.create_all()  

    def tearDown(self):
        # Tear down the database
        db.session.remove()
        db.drop_all()

