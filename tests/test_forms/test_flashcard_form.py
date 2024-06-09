import unittest

from tests.base_test import BaseTestCase

from app.forms.flashcard_form import FlashcardForm

class Test_Default_Form(BaseTestCase):

    def test_1_flashcard_form(self):
        '''
        Tests the flashcard form with no inputs
        '''
        form = FlashcardForm(data={})
        self.assertFalse(form.validate())
        self.assertIn('This field is required.', form.category.errors)
    #-----------------------------------------------------------------------------------------------------------
    def test_2_flashcard_form(self):
        '''
        Tests the flashcard form with only category field
        '''
        form = FlashcardForm(data={
            'category': 'Test Category'
        })
        self.assertFalse(form.validate())
        self.assertIn('At least one question input is required!', form.question.errors)
    #-----------------------------------------------------------------------------------------------------------
    def test_3_flashcard_form(self):
        '''
        Tests the flashcard form with only category and question fields
        '''
        form = FlashcardForm(data={
            'category': 'Test Category',
            'question': 'Is this a test question?'
        })
        self.assertFalse(form.validate())
        self.assertIn('At least one answer input is required!', form.answer.errors)
    #-----------------------------------------------------------------------------------------------------------
    def test_4_flashcard_form(self):
        '''
        Tests the flashcard form with missing figure type fields
        '''
        form = FlashcardForm(data={
            'category': 'Test Category',
            'question': 'Is this a test question?',
            'answer': 'This is a test answer.'
        })
        self.assertTrue(form.validate())
    #-----------------------------------------------------------------------------------------------------------
    def test_5_flashcard_form(self):
        '''
        Tests the flashcard form with missing answer figure type field
        '''
        form = FlashcardForm(data={
            'category': 'Test Category',
            'question': 'Is this a test question?',
            'answer': 'This is a test answer.',
            'q_figure_type': 'none'
        })
        self.assertTrue(form.validate())
    #-----------------------------------------------------------------------------------------------------------
    def test_6_flashcard_form(self):
            '''
            Tests the flashcard form with no figures
            '''
            form = FlashcardForm(data={
                'category': 'Test Category',
                'question': 'Is this a test question?',
                'answer': 'This is a test answer.',
                'q_figure_type': 'none',
                'a_figure_type': 'none'
            })
            self.assertTrue(form.validate())
    #-----------------------------------------------------------------------------------------------------------
    def test_7_flashcard_form(self):
            '''
            Tests the flashcard form with missing question code figure
            '''
            form = FlashcardForm(data={
                'category': 'Test Category',
                'question': 'Is this a test question?',
                'answer': 'This is a test answer.',
                'q_figure_type': 'code',
                'a_figure_type': 'none'
            })
            self.assertFalse(form.validate())
            self.assertIn('Code example is required!', form.q_code_example.errors)
    #-----------------------------------------------------------------------------------------------------------
    def test_8_flashcard_form(self):
            '''
            Tests the flashcard form with missing answer code figure
            '''
            form = FlashcardForm(data={
                'category': 'Test Category',
                'question': 'Is this a test question?',
                'answer': 'This is a test answer.',
                'q_figure_type': 'none',
                'a_figure_type': 'code'
            })
            self.assertFalse(form.validate())
            self.assertIn('Code example is required!', form.a_code_example.errors)
    #-----------------------------------------------------------------------------------------------------------
    def test_9_flashcard_form(self):
            '''
            Tests the flashcard form with missing question code type
            '''
            form = FlashcardForm(data={
                'category': 'Test Category',
                'question': 'Is this a test question?',
                'answer': 'This is a test answer.',
                'q_figure_type': 'code',
                'a_figure_type': 'none',
                'q_code_example': "print('Code Example')"
            })
            self.assertFalse(form.validate())
            self.assertIn('Code type is required!', form.q_code_type.errors)
    #-----------------------------------------------------------------------------------------------------------
    def test_10_flashcard_form(self):
            '''
            Tests the flashcard form with missing answer code type
            '''
            form = FlashcardForm(data={
                'category': 'Test Category',
                'question': 'Is this a test question?',
                'answer': 'This is a test answer.',
                'q_figure_type': 'none',
                'a_figure_type': 'code',
                'a_code_example': "print('Code Example')"
            })
            self.assertFalse(form.validate())
            self.assertIn('Code type is required!', form.a_code_type.errors)
    #-----------------------------------------------------------------------------------------------------------
    def test_11_flashcard_form(self):
            '''
            Tests the flashcard form with question figure fields
            '''
            form = FlashcardForm(data={
                'category': 'Test Category',
                'question': 'Is this a test question?',
                'answer': 'This is a test answer.',
                'q_figure_type': 'code',
                'a_figure_type': 'none',
                'q_code_type': 'python',
                'q_code_example': "print('Code Example')"
            })
            self.assertTrue(form.validate())
    #-----------------------------------------------------------------------------------------------------------
    def test_12_flashcard_form(self):
            '''
            Tests the flashcard form with answer figure fields
            '''
            form = FlashcardForm(data={
                'category': 'Test Category',
                'question': 'Is this a test question?',
                'answer': 'This is a test answer.',
                'q_figure_type': 'none',
                'a_figure_type': 'code',
                'a_code_type': 'python',
                'a_code_example': "print('Code Example')"
            })
            self.assertTrue(form.validate())
    #-----------------------------------------------------------------------------------------------------------
    def test_13_flashcard_form(self):
            '''
            Tests the flashcard form with question and answer figure fields
            '''
            form = FlashcardForm(data={
                'category': 'Test Category',
                'question': 'Is this a test question?',
                'answer': 'This is a test answer.',
                'q_figure_type': 'code',
                'a_figure_type': 'code',
                'q_code_type': 'python',
                'q_code_example': "print('Code example for question')",
                'a_code_type': 'python',
                'a_code_example': "print('Code example for answer')"
            })
            self.assertTrue(form.validate())
    #-----------------------------------------------------------------------------------------------------------
    def test_14_flashcard_form(self):
            '''
            Tests the flashcard form with none selected for question figure field
            '''
            form = FlashcardForm(data={
                'category': 'Test Category',
                'question': 'Is this a test question?',
                'answer': 'This is a test answer.',
                'q_figure_type': 'none',
                'a_figure_type': 'code',
                'q_code_type': 'python',
                'q_code_example': "print('Code example for question')",
                'a_code_type': 'python',
                'a_code_example': "print('Code example for answer')"
            })
            self.assertFalse(form.validate())
            self.assertIn('Cannot submit code if none is selected!', form.q_code_example.errors)
    #-----------------------------------------------------------------------------------------------------------
    def test_15_flashcard_form(self):
            '''
            Tests the flashcard form with none selected for answer figure field
            '''
            form = FlashcardForm(data={
                'category': 'Test Category',
                'question': 'Is this a test question?',
                'answer': 'This is a test answer.',
                'q_figure_type': 'code',
                'a_figure_type': 'none',
                'q_code_type': 'python',
                'q_code_example': "print('Code example for question')",
                'a_code_type': 'python',
                'a_code_example': "print('Code example for answer')"
            })
            self.assertFalse(form.validate())
            self.assertIn('Cannot submit code if none is selected!', form.a_code_example.errors)
    #-----------------------------------------------------------------------------------------------------------
    def test_16_flashcard_form(self):
            '''
            Tests the flashcard form with image selected for question figure field
            '''
            form = FlashcardForm(data={
                'category': 'Test Category',
                'question': 'Is this a test question?',
                'answer': 'This is a test answer.',
                'q_figure_type': 'image',
                'a_figure_type': 'code',
                'q_code_type': 'python',
                'q_code_example': "print('Code example for question')",
                'a_code_type': 'python',
                'a_code_example': "print('Code example for answer')"
            })
            self.assertFalse(form.validate())
            self.assertIn('Cannot submit code if image is selected!', form.q_code_example.errors)
    #-----------------------------------------------------------------------------------------------------------
    def test_17_flashcard_form(self):
            '''
            Tests the flashcard form with image selected for answer figure field
            '''
            form = FlashcardForm(data={
                'category': 'Test Category',
                'question': 'Is this a test question?',
                'answer': 'This is a test answer.',
                'q_figure_type': 'code',
                'a_figure_type': 'image',
                'q_code_type': 'python',
                'q_code_example': "print('Code example for question')",
                'a_code_type': 'python',
                'a_code_example': "print('Code example for answer')"
            })
            self.assertFalse(form.validate())
            self.assertIn('Cannot submit code if image is selected!', form.a_code_example.errors)
    #-----------------------------------------------------------------------------------------------------------
    def test_18_flashcard_form(self):
            '''
            Tests the flashcard form with question image example missing
            '''
            form = FlashcardForm(data={
                'category': 'Test Category',
                'question': 'Is this a test question?',
                'answer': 'This is a test answer.',
                'q_figure_type': 'image',
                'a_figure_type': 'none',
            })
            self.assertFalse(form.validate())
            self.assertIn('Image is required if selected!', form.q_image_example.errors)
    #-----------------------------------------------------------------------------------------------------------
    def test_19_flashcard_form(self):
            '''
            Tests the flashcard form with answer image example missing
            '''
            form = FlashcardForm(data={
                'category': 'Test Category',
                'question': 'Is this a test question?',
                'answer': 'This is a test answer.',
                'q_figure_type': 'none',
                'a_figure_type': 'image'
            })
            self.assertFalse(form.validate())
            self.assertIn('Image is required if selected!', form.a_image_example.errors)
    #-----------------------------------------------------------------------------------------------------------
    def test_20_flashcard_form(self):
            '''
            Tests the flashcard form with question image figure
            '''
            form = FlashcardForm(data={
                'category': 'Test Category',
                'question': 'Is this a test question?',
                'answer': 'This is a test answer.',
                'q_figure_type': 'image',
                'a_figure_type': 'none',
                'q_image_example': 'question_example.jpg'
            })
            self.assertTrue(form.validate())
    #-----------------------------------------------------------------------------------------------------------
    def test_21_flashcard_form(self):
            '''
            Tests the flashcard form with answer image figure
            '''
            form = FlashcardForm(data={
                'category': 'Test Category',
                'question': 'Is this a test question?',
                'answer': 'This is a test answer.',
                'q_figure_type': 'none',
                'a_figure_type': 'image',
                'a_image_example': 'answer_example.jpg'
            })
            self.assertTrue(form.validate())
    #-----------------------------------------------------------------------------------------------------------
    def test_22_flashcard_form(self):
            '''
            Tests the flashcard form with question image when none is selected
            '''
            form = FlashcardForm(data={
                'category': 'Test Category',
                'question': 'Is this a test question?',
                'answer': 'This is a test answer.',
                'q_figure_type': 'none',
                'a_figure_type': 'none',
                'q_image_example': 'question_example.jpg'
            })
            self.assertFalse(form.validate())
            self.assertIn('Cannot submit an image if none is selected!', form.q_image_example.errors)
    #-----------------------------------------------------------------------------------------------------------
    def test_23_flashcard_form(self):
            '''
            Tests the flashcard form with answer image when none is selected
            '''
            form = FlashcardForm(data={
                'category': 'Test Category',
                'question': 'Is this a test question?',
                'answer': 'This is a test answer.',
                'q_figure_type': 'none',
                'a_figure_type': 'none',
                'a_image_example': 'answer_example.jpg'
            })
            self.assertFalse(form.validate())
            self.assertIn('Cannot submit an image if none is selected!', form.a_image_example.errors)
    #-----------------------------------------------------------------------------------------------------------
    def test_24_flashcard_form(self):
            '''
            Tests the flashcard form with question image when code is selected
            '''
            form = FlashcardForm(data={
                'category': 'Test Category',
                'question': 'Is this a test question?',
                'answer': 'This is a test answer.',
                'q_figure_type': 'code',
                'q_image_example': 'question_example.jpg'
            })
            self.assertFalse(form.validate())
            self.assertIn('Cannot submit an image if code is selected!', form.q_image_example.errors)
    #-----------------------------------------------------------------------------------------------------------
    def test_25_flashcard_form(self):
            '''
            Tests the flashcard form with answer image when code is selected
            '''
            form = FlashcardForm(data={
                'category': 'Test Category',
                'question': 'Is this a test question?',
                'answer': 'This is a test answer.',
                'a_figure_type': 'code',
                'a_image_example': 'answer_example.jpg'
            })
            self.assertFalse(form.validate())
            self.assertIn('Cannot submit an image if code is selected!', form.a_image_example.errors)
    #-----------------------------------------------------------------------------------------------------------
    def test_26_flashcard_form(self):
            '''
            Tests the flashcard form with old question image figure
            '''
            form = FlashcardForm(data={
                'category': 'Test Category',
                'question': 'Is this a test question?',
                'answer': 'This is a test answer.',
                'q_figure_type': 'image',
                'q_old_image': 'old_question_example.jpg'
            })
            self.assertTrue(form.validate())
    #-----------------------------------------------------------------------------------------------------------
    def test_27_flashcard_form(self):
            '''
            Tests the flashcard form with old answer image figure
            '''
            form = FlashcardForm(data={
                'category': 'Test Category',
                'question': 'Is this a test question?',
                'answer': 'This is a test answer.',
                'a_figure_type': 'image',
                'a_old_image': 'old_answer_example.jpg'
            })
            self.assertTrue(form.validate())
    #-----------------------------------------------------------------------------------------------------------
    def test_28_flashcard_form(self):
            '''
            Tests the flashcard form with image figures and missing question
            '''
            form = FlashcardForm(data={
                'category': 'Test Category',
                'answer': 'This is a test answer.',
                'q_figure_type': 'image',
                'q_image_example': 'question_example.jpg',
                'a_figure_type': 'image',
                'a_image_example': 'answer_example.jpg'
            })
            self.assertTrue(form.validate())
    #-----------------------------------------------------------------------------------------------------------
    def test_29_flashcard_form(self):
            '''
            Tests the flashcard form with image figures and missing answer
            '''
            form = FlashcardForm(data={
                'category': 'Test Category',
                'question': 'Is this a test question?',
                'q_figure_type': 'image',
                'q_image_example': 'question_example.jpg',
                'a_figure_type': 'image',
                'a_image_example': 'answer_example.jpg'
            })
            self.assertTrue(form.validate())
    #-----------------------------------------------------------------------------------------------------------
    def test_30_flashcard_form(self):
            '''
            Tests the flashcard form with image figures and missing question and answer
            '''
            form = FlashcardForm(data={
                'category': 'Test Category',
                'q_figure_type': 'image',
                'q_image_example': 'question_example.jpg',
                'a_figure_type': 'image',
                'a_image_example': 'answer_example.jpg'
            })
            self.assertTrue(form.validate())
    #-----------------------------------------------------------------------------------------------------------
    def test_31_flashcard_form(self):
            '''
            Tests the flashcard form with code figures and missing question and answer
            '''
            form = FlashcardForm(data={
                'category': 'Test Category',
                'q_figure_type': 'code',
                'q_code_type': 'python',
                'q_code_example': "print('Code example for question')",
                'a_figure_type': 'code',
                'a_code_type': 'python',
                'a_code_example': "print('Code example for answer')"
            })
            self.assertTrue(form.validate())