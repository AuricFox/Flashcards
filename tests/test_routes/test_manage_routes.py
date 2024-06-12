import unittest

from flask import url_for

from tests.base_test import BaseTestCase, RouteTestCase


class Test_Manage_Page(BaseTestCase):

    def test_1_manage_page(self):
        '''
        Tests the manage page without search input
        '''
        response = self.client.get(url_for('manage.index'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<title>Manage Flashcards</title>", response.data)
    #-----------------------------------------------------------------------------------------------------------
    def test_1_manage_page(self):
        '''
        Tests the manage page with search input
        '''
        response = self.client.get(
            url_for('manage.index'), 
            data = {
                'search': 'Search Category'
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<title>Manage Flashcards</title>", response.data)


class Test_Add_Page(BaseTestCase):

    def test_1_add_page(self):
        '''
        Tests the add flashcard page without inputs
        '''
        response = self.client.get(url_for('manage.add_flashcard'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<title>Add Flashcard</title>", response.data)
    #-----------------------------------------------------------------------------------------------------------
    def test_2_add_page(self):
        '''
        Tests for a successful post for the add flashcard page
        '''
        response = self.client.post(
            url_for('manage.add_flashcard'), 
            data={
                'category': 'Test Category',
                'question': 'Is this a test question?',
                'answer': 'This is a test answer.'}, 
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Manage Flashcards</title>', response.data)
    #-----------------------------------------------------------------------------------------------------------
    def test_3_add_page(self):
        '''
        Tests for an invalid post to the add flashcard page
        '''
        response = self.client.post(
            url_for('manage.add_flashcard'), 
            data={
                'question': 'Is the category field missing?',
                'answer': 'Yes, the category field is missing'}, 
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Add Flashcard</title>', response.data)


class Test_View_Page(RouteTestCase):

    def test_1_view_page(self):
        '''
        Tests the view page
        '''
        response = self.client.get(url_for('manage.view_flashcard', id=1), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<title>View Flashcard</title>", response.data)
    #-----------------------------------------------------------------------------------------------------------
    def test_2_view_page(self):
        '''
        Tests the view page for invalid id
        '''
        response = self.client.get(url_for('manage.view_flashcard', id=100), follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"<title>Page Not Found</title>", response.data)


class Test_Edit_Page(RouteTestCase):

    def test_1_edit_page(self):
        '''
        Tests the edit page
        '''
        response = self.client.get(url_for('manage.edit_flashcard', id=1), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<title>Edit Flashcard</title>", response.data)
    #-----------------------------------------------------------------------------------------------------------
    def test_2_edit_page(self):
        '''
        Tests the edit page for invalid id
        '''
        response = self.client.get(url_for('manage.edit_flashcard', id=100), follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"<title>Page Not Found</title>", response.data)
    #-----------------------------------------------------------------------------------------------------------
    def test_3_edit_page(self):
        '''
        Tests the edit page for successful post
        '''
        response = self.client.post(
            url_for('manage.edit_flashcard', id=1), 
            data = {
                'category': 'New Test Category',
                'question': 'Is this a new test question?',
                'answer': 'This is a new test answer.',
                'q_code_type': 'python',
                'q_code_example': "print('New Test Question Example')",
                'a_code_type': 'python',
                'a_code_example': "print('New Test Answer Example')"
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<title>Manage Flashcards</title>", response.data)
    #-----------------------------------------------------------------------------------------------------------
    def test_3_edit_page(self):
        '''
        Tests the edit page for invalid post
        '''
        response = self.client.post(
            url_for('manage.edit_flashcard', id=1), 
            data = {
                'category': 'New Test Category',
                'question': 'Is this a new test question?',
                'answer': 'This is a new test answer.',
                'q_code_type': 'python',
                'q_code_example': "print('New Test Question Example')",
                'a_code_type': 'python',
                'a_code_example': "print('New Test Answer Example')"
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<title>Edit Flashcard</title>", response.data)


class Test_Delete_Route(RouteTestCase):

    def test_1_delete_route(self):
        '''
        Tests the delete route
        '''
        response = self.client.get(url_for('manage.delete_flashcard', id=1), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<title>Manage Flashcards</title>", response.data)
    #-----------------------------------------------------------------------------------------------------------
    def test_2_delete_route(self):
        '''
        Tests the delete route for invalid id
        '''
        response = self.client.get(url_for('manage.delete_flashcard', id=100), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<title>Manage Flashcards</title>", response.data)


if __name__ == "__main__":
    unittest.main()