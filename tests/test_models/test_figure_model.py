import unittest

from tests.base_test import BaseTestCase

from app.models.flashcard_model import FigureModel as fm

class Test_Figure_Model(BaseTestCase):
    '''Test the constructor method within the figure model'''

    def test_1_figure_model(self):
        '''
        Tests the figure model with no inputs
        '''
        with self.assertRaises(Exception) as context:
            figure = fm()

        self.assertTrue("Missing figure inputs!" in str(context.exception))
    #-----------------------------------------------------------------------------------------------------------
    def test_2_figure_model(self):
        '''
        Tests the figure model with missing inputs (code_example)
        '''
        with self.assertRaises(Exception) as context:
            figure = fm(
                code_type='python'
            )

        self.assertTrue("Missing figure inputs!" in str(context.exception))
    #-----------------------------------------------------------------------------------------------------------
    def test_3_figure_model(self):
        '''
        Tests the figure model with code inputs
        '''
        figure = fm(
            code_type='python',
            code_example="print('This is a code example!')"
        )

        self.assertTrue(figure.code_type == 'python')
        self.assertTrue(figure.code_example == "print('This is a code example!')")
    #-----------------------------------------------------------------------------------------------------------
    def test_4_figure_model(self):
        '''
        Tests the figure model with invalid image file
        '''
        with self.assertRaises(Exception) as context:
            figure = fm(
                image_example='example_image.jpg'
            )

        self.assertTrue("'str' object has no attribute 'filename'" in str(context.exception))


class Test_Figure_Update(BaseTestCase):
    '''Test the update method within the figure model'''

    def test_1_figure_update(self):
        '''
        Tests update method with no inputs
        '''
        with self.assertRaises(Exception) as context:
            figure = fm(
                code_type='python',
                code_example="print('This is an old code example!')"
            )

            figure.update()

        self.assertTrue("Missing figure inputs!" in str(context.exception))
    #-----------------------------------------------------------------------------------------------------------
    def test_2_figure_update(self):
        '''
        Tests update method with missing inputs (code_example)
        '''
        with self.assertRaises(Exception) as context:
            figure = fm(
                code_type='python',
                code_example="print('This is an old code example!')"
            )

            figure.update(
                code_type='python'
            )

        self.assertTrue("Missing figure inputs!" in str(context.exception))
    #-----------------------------------------------------------------------------------------------------------
    def test_3_figure_update(self):
        '''
        Tests update method with code inputs
        '''
        figure = fm(
            code_type='python',
            code_example="print('This is an old code example!')"
        )

        figure.update(
            code_type='python',
            code_example="print('This is a new code example!')"
        )

        self.assertTrue(figure.code_type == 'python')
        self.assertTrue(figure.code_example == "print('This is a new code example!')")
#-----------------------------------------------------------------------------------------------------------
    def test_3_figure_update(self):
        '''
        Tests update method with invalid image file
        '''
        with self.assertRaises(Exception) as context:
            figure = fm(
                code_type='python',
                code_example="print('This is an old code example!')"
            )

            figure.update(
                image_example='example_image.jpg'
            )

        self.assertTrue('Invalid image filename!' in str(context.exception))
        self.assertTrue(figure.code_type == 'python')
        self.assertTrue(figure.code_example == "print('This is an old code example!')")


class Test_Figure_Delete(BaseTestCase):
    '''Tests the delete method within the figure model'''

    def test_1_figure_delete(self):
        '''Tests the delete method'''
        figure = fm(
            code_type='python',
            code_example="print('This is an old code example!')"
        )

        db_figure = fm.query.get(figure.id)
        self.assertTrue(db_figure != None)

        figure.delete()

        db_figure = fm.query.get(figure.id)
        self.assertTrue(db_figure == None)