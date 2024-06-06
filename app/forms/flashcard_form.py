from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, RadioField, HiddenField
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
    q_image_example = FileField(
        "Question Image", validators=[Optional()]
    )

    q_old_image = StringField(
        "Old Question Image", validators=[Optional()]
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
    a_image_example = FileField(
        "Answer Image", validators=[Optional()]
    )
    a_old_image = StringField(
        "Old Answer Image", validators=[Optional()]
    )

    # ==============================================================================================================
    def validate(self, extra_validators=None):
        '''
        Validates the submitted form data
        '''
        initial_validation = super(FlashcardForm, self).validate(extra_validators)
        if not initial_validation:
            return False
        
        # Validate Question attributes
        if not (self.question.data or self.q_code_example.data or self.q_image_example.data):
            self.question.errors.append("At least one question input is required!")
            return False

        # Validate question figures if code is selected
        if self.q_figure_type.data == 'code':
            if self.q_image_example.data:
                self.q_image_example.errors.append("Cannot submit an image if code is selected!")
                return False
            if not self.q_code_type.data or not self.q_code_example.data:
                if not self.q_code_type.data:
                    self.q_code_type.errors.append("Code type is required!")
                if not self.q_code_example.data:
                    self.q_code_example.errors.append("Code example is required!")
                return False
        # Validate question figures if image is selected
        elif self.q_figure_type.data == 'image':
            if self.q_code_example.data:
                self.q_code_example.errors.append("Cannot submit code if image is selected!")
                return False
            if not self.q_image_example.data and not self.q_old_image:
                self.q_image_example.errors.append("Image is required if selected!")
                return False
        # Validate question figures if none is selected
        elif self.q_figure_type.data == 'none':
            if self.q_code_example.data or self.q_image_example.data:
                if self.q_code_example.data:
                    self.q_code_example.errors.append("Cannot submit code if none is selected!")
                if self.q_image_example.data:
                    self.q_image_example.errors.append("Cannot submit an image if none is selected!")
                return False

        # Validate Answer attributes
        if not (self.answer.data or self.a_code_example.data or self.a_image_example.data):
            self.answer.errors.append("At least one answer input is required!")
            return False

        # Validate anwser figures if code is selected
        if self.a_figure_type.data == 'code':
            if self.a_image_example.data:
                self.a_image_example.errors.append("Cannot submit an image if code is selected!")
                return False
            if not self.a_code_type.data or not self.a_code_example.data:
                if not self.a_code_type.data:
                    self.a_code_type.errors.append("Code type is required!")
                if not self.a_code_example.data:
                    self.a_code_example.errors.append("Code example is required!")
                return False
        # Validate anwser figures if image is selected
        elif self.a_figure_type.data == 'image':
            if self.a_code_example.data:
                self.a_code_example.errors.append("Cannot submit code if image is selected!")
                return False
            if not self.a_image_example.data and not self.a_old_image:
                self.a_image_example.errors.append("Image is required if selected!")
                return False
        # Validate anwser figures if none is selected
        elif self.a_figure_type.data == 'none':
            if self.a_code_example.data or self.a_image_example.data:
                if self.a_code_example.data:
                    self.a_code_example.errors.append("Cannot submit code if none is selected!")
                if self.a_image_example.data:
                    self.a_image_example.errors.append("Cannot submit an image if none is selected!")
                return False

        return True