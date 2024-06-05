from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class SearchForm(FlaskForm):
    '''
    Form used to validate submitted flashcard data
    '''
    search = StringField(
        "Search", validators=[DataRequired(), Length(max=100)]
    )

    # ==============================================================================================================
    def validate(self, extra_validators=None):
        '''
        Validates the submitted form data
        '''
        initial_validation = super(SearchForm, self).validate(extra_validators)
        if not initial_validation:
            return False
       
        return True