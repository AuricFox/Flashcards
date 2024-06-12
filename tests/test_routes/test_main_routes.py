import unittest

from flask import url_for

from tests.base_test import BaseTestCase

class Test_Main_Pages(BaseTestCase):

    def test_home_page(self):
        '''
        Tests the home page
        '''
        response = self.client.get(url_for('main.index'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<title>Home</title>", response.data)
    #-----------------------------------------------------------------------------------------------------------
    def test_flashcard_page(self):
        '''
        Tests the flashcard page
        '''
        response = self.client.get(url_for('main.flashcard', category='Test Cagegory'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<title>Flashcards</title>", response.data)
    #-----------------------------------------------------------------------------------------------------------
    def test_404_page(self):
        '''
        Tests the 404 page
        '''
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'<title>Page Not Found</title>', response.data)
        

if __name__ == "__main__":
    unittest.main()