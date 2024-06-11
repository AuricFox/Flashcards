import unittest

from tests.base_test import BaseTestCase

from app.models.flashcard_model import FlashcardModel as fm

class Test_Flashcard_Model(BaseTestCase):
    '''Test the constructor method within the Flashcard model'''

    def test_1_flashcard_model(self):
        '''
        Tests the flashcard model with no inputs
        '''
        with self.assertRaises(Exception) as context:
            flashcard = fm()

        self.assertTrue("missing 1 required positional argument: 'category'" in str(context.exception))
    #-----------------------------------------------------------------------------------------------------------
    def test_2_flashcard_model(self):
        '''
        Tests the flashcard model with only category input
        '''
        with self.assertRaises(Exception) as context:
            flashcard = fm(
                category='Test Category'
            )

        self.assertTrue("No question inputs!" in str(context.exception))
    #-----------------------------------------------------------------------------------------------------------
    def test_3_flashcard_model(self):
        '''
        Tests the flashcard model with no answer inputs
        '''
        with self.assertRaises(Exception) as context:
            flashcard = fm(
                category='Test Category',
                question='Is this a test question?'
            )

        self.assertTrue("No answer inputs!" in str(context.exception))
    #-----------------------------------------------------------------------------------------------------------
    def test_4_flashcard_model(self):
        '''
        Tests the flashcard model with question and answer inputs
        '''
        flashcard = fm(
            category='Test Category',
            question='Is this a test question?',
            answer='This is an answer example.'
        )

        self.assertTrue(flashcard.category == 'Test Category')
        self.assertTrue(flashcard.question == 'Is this a test question?')
        self.assertTrue(flashcard.answer == 'This is an answer example.')
    #-----------------------------------------------------------------------------------------------------------
    def test_5_flashcard_model(self):
        '''
        Tests the flashcard model with missing question code example
        '''
        with self.assertRaises(Exception) as context:
            flashcard = fm(
                category='Test Category',
                question='Is this a test question?',
                answer='This is an answer example.',
                q_code_type='python'
            )

        self.assertTrue("Missing figure inputs!" in str(context.exception))
    #-----------------------------------------------------------------------------------------------------------
    def test_6_flashcard_model(self):
        '''
        Tests the flashcard model with missing answer code example
        '''
        with self.assertRaises(Exception) as context:
            flashcard = fm(
                category='Test Category',
                question='Is this a test question?',
                answer='This is an answer example.',
                q_code_type='python'
            )

        self.assertTrue("Missing figure inputs!" in str(context.exception))
    #-----------------------------------------------------------------------------------------------------------
    def test_7_flashcard_model(self):
        '''
        Tests the flashcard model with missing question code type
        '''
        with self.assertRaises(Exception) as context:
            flashcard = fm(
                category='Test Category',
                question='Is this a test question?',
                answer='This is an answer example.',
                q_code_example="print('This is a question example!')"
            )

        self.assertTrue("Missing figure inputs!" in str(context.exception))
    #-----------------------------------------------------------------------------------------------------------
    def test_8_flashcard_model(self):
        '''
        Tests the flashcard model with missing answer code type
        '''
        with self.assertRaises(Exception) as context:
            flashcard = fm(
                category='Test Category',
                question='Is this a test question?',
                answer='This is an answer example.',
                a_code_example="print('This is an answer example!')"
            )

        self.assertTrue("Missing figure inputs!" in str(context.exception))
    #-----------------------------------------------------------------------------------------------------------
    def test_9_flashcard_model(self):
        '''
        Tests the flashcard model question code figure
        '''
        flashcard = fm(
            category='Test Category',
            question='Is this a test question?',
            answer='This is an answer example.',
            q_code_type='python',
            q_code_example="print('This is a question example!')"
        )

        self.assertTrue(flashcard.category == 'Test Category')
        self.assertTrue(flashcard.q_figure == 1)
    #-----------------------------------------------------------------------------------------------------------
    def test_10_flashcard_model(self):
        '''
        Tests the flashcard model answer code figure
        '''
        flashcard = fm(
            category='Test Category',
            question='Is this a test question?',
            answer='This is an answer example.',
            a_code_type='python',
            a_code_example="print('This is an answer example!')"
        )

        self.assertTrue(flashcard.category == 'Test Category')
        self.assertTrue(flashcard.a_figure == 1)


class Test_Flascard_View(BaseTestCase):
    '''Test the view method within the Flashcard model'''

    def test_1_flashcard_view(self):
        '''Test the view method with minimum inputs'''
        flashcard = fm(
            category='Test Category',
            question='Is this a test question?',
            answer='This is an answer example.',
        )

        response = flashcard.view()
        self.assertTrue(response['category'] == 'Test Category')
        self.assertTrue(response['question'] == 'Is this a test question?')
        self.assertTrue(response['answer'] == 'This is an answer example.')
    #-----------------------------------------------------------------------------------------------------------
    def test_2_flashcard_view(self):
        '''Test the view method with inputs'''
        flashcard = fm(
            category='Test Category',
            question='Is this a test question?',
            answer='This is an answer example.',
            q_code_type='python',
            q_code_example="print('This is a question example!')",
            a_code_type='python',
            a_code_example="print('This is an answer example!')"
        )

        response = flashcard.view()
        self.assertTrue(response['category'] == 'Test Category')
        self.assertTrue(response['question'] == 'Is this a test question?')
        self.assertTrue(response['answer'] == 'This is an answer example.')
        self.assertTrue(response['q_code_type'] == 'python')
        self.assertTrue(response['q_code_example'] == "print('This is a question example!')")
        self.assertTrue(response['a_code_type'] == 'python')
        self.assertTrue(response['a_code_example'] == "print('This is an answer example!')")


class Test_Flashcard_Update(BaseTestCase):
    '''Tests Update method within the Flashcard model'''

    def test_1_flashcard_update(self):
        '''Test the update method with minimum inputs'''
        flashcard = fm(
            category='Old Test Category',
            question='Is this an old test question?',
            answer='This is an old answer example.'
        )

        flashcard.update(
            category='New Test Category',
            question='Is this a new test question?',
            answer='This is a new answer example.'
        )

        self.assertTrue(flashcard.category == 'New Test Category')
        self.assertTrue(flashcard.question == 'Is this a new test question?')
        self.assertTrue(flashcard.answer == 'This is a new answer example.')
    #-----------------------------------------------------------------------------------------------------------
    def test_2_flashcard_update(self):
        '''Test the update method with no new code figures'''
        flashcard = fm(
            category='Old Test Category',
            question='Is this an old test question?',
            answer='This is an old answer example.',
            q_code_type='python',
            q_code_example="print('This is a question example!')",
            a_code_type='python',
            a_code_example="print('This is an answer example!')"
        )

        flashcard.update(
            category='New Test Category',
            question='Is this a new test question?',
            answer='This is a new answer example.',
        )

        self.assertTrue(flashcard.category == 'New Test Category')
        self.assertTrue(flashcard.question == 'Is this a new test question?')
        self.assertTrue(flashcard.answer == 'This is a new answer example.')
        self.assertTrue(flashcard.q_figure == None)
        self.assertTrue(flashcard.a_figure == None)
    #-----------------------------------------------------------------------------------------------------------
    def test_3_flashcard_update(self):
        '''Test the update method with new code figures'''
        flashcard = fm(
            category='Old Test Category',
            question='Is this an old test question?',
            answer='This is an old answer example.',
            q_code_type='python',
            q_code_example="print('This is an old question example!')",
            a_code_type='python',
            a_code_example="print('This is an old answer example!')"
        )

        flashcard.update(
            category='New Test Category',
            question='Is this a new test question?',
            answer='This is a new answer example.',
            q_code_type='python',
            q_code_example="print('This is a new question example!')",
            a_code_type='python',
            a_code_example="print('This is a new answer example!')"
        )

        self.assertTrue(flashcard.category == 'New Test Category')
        self.assertTrue(flashcard.question == 'Is this a new test question?')
        self.assertTrue(flashcard.answer == 'This is a new answer example.')
        self.assertFalse(flashcard.q_figure == None)
        self.assertFalse(flashcard.a_figure == None)
    #-----------------------------------------------------------------------------------------------------------
    def test_4_flashcard_update(self):
        '''Test the update method adding code figures'''
        flashcard = fm(
            category='Old Test Category',
            question='Is this an old test question?',
            answer='This is an old answer example.'
        )

        flashcard.update(
            category='New Test Category',
            question='Is this a new test question?',
            answer='This is a new answer example.',
            q_code_type='python',
            q_code_example="print('This is a new question example!')",
            a_code_type='python',
            a_code_example="print('This is a new answer example!')"
        )

        self.assertTrue(flashcard.category == 'New Test Category')
        self.assertTrue(flashcard.question == 'Is this a new test question?')
        self.assertTrue(flashcard.answer == 'This is a new answer example.')
        self.assertFalse(flashcard.q_figure == None)
        self.assertFalse(flashcard.a_figure == None)


class Test_Flashcard_Delete(BaseTestCase):
    '''Tests delete method within the Flashcard model'''

    def test_1_flashcard_delete(self):
        '''Test the delete method with minimum inputs'''
        flashcard = fm(
            category='Test Category',
            question='Is this a test question?',
            answer='This is an answer example.'
        )

        status = flashcard.delete()
        self.assertTrue(status)
    #-----------------------------------------------------------------------------------------------------------
    def test_3_flashcard_update(self):
        '''Test the delete method with code figures'''
        flashcard = fm(
            category='Test Category',
            question='Is this a test question?',
            answer='This is an answer example.',
            q_code_type='python',
            q_code_example="print('This is a question example!')",
            a_code_type='python',
            a_code_example="print('This is an answer example!')"
        )

        status = flashcard.delete()
        self.assertTrue(status)