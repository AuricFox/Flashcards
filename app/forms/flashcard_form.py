from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, RadioField
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

    q_figure_type = RadioField('Question Figure Type', choices=[
        ('code', 'Code'),
        ('image', 'Image'),
        ('none', 'None')
    ], default='none', validators=[DataRequired()])

    q_code_type = StringField(
        "Question Code Type", validators=[Optional(), Length(max=25)]
    )
    q_code_example = TextAreaField(
        "Question Code Example", validators=[Optional()]
    )
    q_image_file = FileField(
        "Question Image", validators=[Optional()]
    )

    a_figure_type = RadioField('Answer Figure Type', choices=[
        ('code', 'Code'),
        ('image', 'Image'),
        ('none', 'None')
    ], default='none', validators=[DataRequired()])

    a_code_type = StringField(
        "Answer Code Type", validators=[Optional(), Length(max=25)]
    )
    a_code_example = TextAreaField(
        "Answer Code Example", validators=[Optional()]
    )
    a_image_file = FileField(
        "Answer Image", validators=[Optional()]
    )

    # ==============================================================================================================
    def validate(self, extra_validators=None):
        '''
        Validates the submitted form data
        '''
        initial_validation = super(FlashcardForm, self).validate(extra_validators)
        if not initial_validation:
            return False
        #----------------------------------------------------------------------------
        # Validate Question attributes
        #----------------------------------------------------------------------------
        # Check if there is anything on the question side of the flashcard
        if not (self.question and self.q_code_example and self.q_image_file):
            self.question.errors.append("Missing question inputs!")
            return False
        
        # Check if the proper figure type has been selected
        if self.q_figure_type.data == 'code' and self.q_image_file.data:
            self.q_image_file.errors.append("Cannot submit an image if code is selected!")
            return False
        elif self.q_figure_type.data == 'image' and self.q_code_example.data:
            self.q_code_example.errors.append("Cannot submit code if image is selected!")
            return False
        elif self.q_figure_type.data == 'none' and self.q_image_file.data:
            self.q_image_file.errors.append("Cannot submit an image if none is selected!")
            return False
        elif self.q_figure_type.data == 'none' and self.q_code_example.data:
            self.q_code_example.errors.append("Cannot submit code if none is selected!")
            return False
        
        # Check if there is a code type and example for questions
        if self.q_figure_type.data == 'code' and not self.q_code_type and not self.q_code_example:
            self.q_code_type.errors.append("Code type is required!")
            self.q_code_example.errors.append("Code example is required!")
            return False
        elif self.q_figure_type.data == 'code' and not self.q_code_type and self.q_code_example:
            self.q_code_type.errors.append("Code type is required!")
            return False
        elif self.q_figure_type.data == 'code' and self.q_code_type and not self.q_code_example:
            self.q_code_example.errors.append("Code example is required!")
            return False
        
        # Check if there is an image if the image field is selected
        if self.q_figure_type.data == 'image' and not self.q_image_file.data:
            self.q_image_file.errors.append("Image is required if selected!")
            return False
        
        # Check if there is only one example for questions
        if self.q_code_example and self.q_image_file:
            self.q_image_file.errors.append("Can't have image and code examples!")
            self.q_code_example.errors.append("Can't have code and image examples!")
            return False
        #----------------------------------------------------------------------------
        # Validate Answer attributes
        #----------------------------------------------------------------------------
        # Check if there is anything on the answer side of the flashcard
        if not (self.answer and self.a_code_example and self.a_image_file):
            self.answer.errors.append("Missing answer inputs!")
            return False
        
        # Check if the proper figure type has been selected
        if self.a_figure_type.data == 'code' and self.a_image_file.data:
            self.a_image_file.errors.append("Cannot submit an image if code is selected!")
            return False
        elif self.a_figure_type.data == 'image' and self.a_code_example.data:
            self.a_code_example.errors.append("Cannot submit code if image is selected!")
            return False
        elif self.a_figure_type.data == 'none' and self.a_image_file.data:
            self.a_image_file.errors.append("Cannot submit an image if none is selected!")
            return False
        elif self.a_figure_type.data == 'none' and self.a_code_example.data:
            self.a_code_example.errors.append("Cannot submit code if none is selected!")
            return False
        
        # Check if there is a code type and example for answers
        if self.a_figure_type.data == 'code' and not self.a_code_type and not self.a_code_example:
            self.a_code_type.errors.append("Code type is required!")
            self.a_code_example.errors.append("Code example is required!")
            return False
        elif self.a_figure_type.data == 'code' and not self.a_code_type and self.a_code_example:
            self.a_code_type.errors.append("Code type is required!")
            return False
        elif self.a_figure_type.data == 'code' and self.a_code_type and not self.a_code_example:
            self.a_code_example.errors.append("Code example is required!")
            return False
        
        # Check if there is only one example for answers
        if self.a_code_example and self.a_image_file:
            self.a_image_file.errors.append("Can't have image and code examples!")
            self.a_code_example.errors.append("Can't have code and image examples!")
            return False
        
        return True