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

class RouteTestCase(BaseTestCase):
    '''
    Creates a base test class for routes
    '''
    def create_app(self):
        # Create and configure the app for testing
        app = init_app('config.TestingConfig')
        return app

    def setUp(self):
        # Set up the database
        super().setUp()
        self.create_test_users()

    def create_test_users(self):
        # Populates the database with test date
        self.flashcard1 = FlashcardModel(
            category='Test Category',
            question='Is this a test question?',
            answer='This is a test answer.',
            q_code_type='python',
            q_code_example="print('Test Question Example')",
            a_code_type='python',
            a_code_example="print('Test Answer Example')"
        )

        db.session.flush()
        db.session.commit()
        