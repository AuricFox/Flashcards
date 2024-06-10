import unittest

from tests.base_test import BaseTestCase

from app.forms.search_form import SearchForm

class Test_Search_Form(BaseTestCase):

    def test_1_search_form(self):
        '''
        Tests the search form with no inputs
        '''
        form = SearchForm(data={})
        self.assertFalse(form.validate())
    #-----------------------------------------------------------------------------------------------------------
    def test_2_search_form(self):
        '''
        Tests the search form with inputs
        '''
        form = SearchForm(data={
            'search': 'Search test'
        })
        self.assertTrue(form.validate())
    #-----------------------------------------------------------------------------------------------------------
    def test_3_search_form(self):
        '''
        Tests the search form with invalid inputs
        '''
        form = SearchForm(data={
            'search': 'Search test' * 10
        })
        self.assertFalse(form.validate())