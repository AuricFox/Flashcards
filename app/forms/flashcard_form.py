from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, HiddenField
from wtforms.validators import DataRequired, Optional, Length

class FlashcardForm(FlaskForm):
    '''
    Form used to validate submitted flashcard data
    '''
    category = StringField(
        "Category", validators=[DataRequired(), Length(max=100)]
    )
    question = TextAreaField(
        "Question", validators=[Optional()]
    )
    answer = TextAreaField(
        "Answer", validators=[Optional()]
    )
    question_code_type = StringField(
        "Question Code Type", validators=[Optional(), Length(max=25)]
    )
    question_code_example = TextAreaField(
        "Question Code Example", validators=[Optional()]
    )
    question_image_file = FileField(
        "Question Image", validators=[Optional()]
    )
    old_question_image = HiddenField(
        "Old Question Image"
    )
    answer_code_type = StringField(
        "Answer Code Type", validators=[Optional(), Length(max=25)]
    )
    answer_code_example = TextAreaField(
        "Answer Code Example", validators=[Optional()]
    )
    answer_image_file = FileField(
        "Answer Image", validators=[Optional()]
    )
    old_answer_image = HiddenField(
        "Old Answer Image"
    )

    # ==============================================================================================================
    def validate(self, extra_validators=None):
        '''
        Validates the submitted form data
        '''
        initial_validation = super(FlashcardForm, self).validate(extra_validators)
        if not initial_validation:
            return False
        
        # Check if there is anything on the question side of the flashcard
        if not (self.question and self.question_code_example and self.question_image_file):
            self.question.errors.append("Please enter a question.")
            return False
        
        # Check if there is a code type and example for questions
        if not self.question_code_type and self.question_code_example:
            self.question_code_type.errors.append("Code type is required!")
            return False
        elif self.question_code_type and not self.question_code_example:
            self.question_code_example.errors.append("Code example is required!")
            return False
        
        # Check if there is only one example for questions
        if self.question_code_example and self.question_image_file:
            self.question_image_file.errors.append("Can't have image and code examples!")
            self.question_code_example.errors.append("Can't have code and image examples!")
            return False
        
        # Check if there is anything on the answer side of the flashcard
        if not (self.answer and self.answer_code_example and self.answer_image_file):
            self.answer.errors.append("Please enter an answer.")
            return False
        
        # Check if there is a code type and example for answers
        if not self.answer_code_type and self.answer_code_example:
            self.answer_code_type.errors.append("Code type is required!")
            return False
        elif self.answer_code_type and not self.answer_code_example:
            self.answer_code_example.errors.append("Code example is required!")
            return False
        
        # Check if there is only one example for answers
        if self.answer_code_example and self.answer_image_file:
            self.answer_image_file.errors.append("Can't have image and code examples!")
            self.answer_code_example.errors.append("Can't have code and image examples!")
            return False
        
        return True