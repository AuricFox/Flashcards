from app.extensions import db
from app.utils import LOGGER

class Figure(db.Model):
    '''
    Model for flashcard figures
    '''
    __tablename__ = "figures"

    id = db.Column(db.Integer, primary_key=True)
    code_type = db.Column(db.String(100), nullable=True)
    code_example = db.Column(db.Text, nullable=True)
    image_example = db.Column(db.String(200), nullable=True)

    def __int__(self, code_type:str=None, code_example:str=None, image_example:str=None):
        '''
        Initializes the figure data entry into the database
        
        Parameter(s):
            code_type (str, default=None): name of the programming language used for the code example
            code_example (str, default=None): a block of code used to support the flashcard
            image_example (str, default=None): a filename of the image used to support the flashcard
        
        Output(s): None
        '''
        try:
            if not (code_type and code_example or image_example):
                raise Exception("Missing figure inputs!")
            elif code_type and code_example and image_example:
                raise Exception("Can only have one figure type Code or Image!")
            
            self.code_type = code_type
            self.code_example = code_example
            self.image_example = image_example
            
        except Exception as e:
            LOGGER.error(f"An error occurred when entering figure data into the database: {e}")
# ==============================================================================================================
class User(db.Model):
    '''
    Model for flashcards
    '''
    __tablename__ = "flashcards"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    question = db.Column(db.String(100), unique=True, nullable=True)
    answer = db.Column(db.String(100), nullable=True)
    question_figure = db.Column(db.Interger, nullable=True)
    answer_figure = db.Column(db.Integer, nullable=True)

    def __init__(self, 
        category:str, 
        question:str=None, 
        answer:str=None, 
        question_figure:tuple=None, 
        answer_figure:tuple=None):

        '''
        Initializes the flashcard data entry into the database

        Parameter(s):
            category (str): the question category
            question (str, default=None): a query about a certain topic
            answer (str, default=None): a response to the question
            code_example (tuple, default=None): code type, code example, or file name of image for questions
            image_example (tuple, default=None): code type, code example, or file name of image for answers
        
        Output(s): None
        '''
        try:
            # Check if there are question inputs
            if not (question or question_figure):
                raise Exception("No question inputs!")
            # Check if there are answer inputs
            if not (answer or answer_figure):
                raise Exception("No answer inputs!")

            self.category = category
            self.question = question
            self.answer = answer

            # Process question figures
            if question_figure:
                self.question_figure = Figure(question_figure).id
            # Process answer figures
            if answer_figure:
                self.answer_figure = Figure(answer_figure).id

        except Exception as e:
            LOGGER.error(f"An error occurred when entering flashcard data into the database: {e}")

    def __repr__(self):
        return (
            f"Category: {self.category}\n"
            f"Question: {self.question}\n"
            f"Answer: {self.answer}\n"
            f"Question figure ID: {self.question_figure}\n"
            f"Answer figure ID: {self.answer_figure}"
        )