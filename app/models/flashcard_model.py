from app.extensions import db
from app.utils import LOGGER, save_image_file

class FigureModel(db.Model):
    '''
    Model for flashcard figures
    '''
    __tablename__ = "figures"

    id = db.Column(db.Integer, primary_key=True)
    code_type = db.Column(db.String(25), nullable=True)
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

            # Save the image if there is one
            if image_example:
                status = save_image_file(image_example)
                # Check if a filename is returned
                if not status: 
                    raise Exception("Failed to save file!")
                else:
                    self.image_example = status
            
        except Exception as e:
            LOGGER.error(f"An error occurred when entering figure data into the database: {e}")

# ==============================================================================================================
class FlashcardModel(db.Model):
    '''
    Model for flashcards
    '''
    __tablename__ = "flashcards"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    question = db.Column(db.Text, nullable=True)
    answer = db.Column(db.Text, nullable=True)
    question_figure = db.Column(db.Integer, nullable=True)
    answer_figure = db.Column(db.Integer, nullable=True)

    def __init__(self, 
        category:str, 
        question:str=None, 
        answer:str=None, 
        question_code_type:str=None,
        question_code_example:str=None,
        question_image_example:object=None, 
        answer_code_type:str=None,
        answer_code_example:str=None,
        answer_image_example:object=None):

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
            # Check if there is a category input
            if not category:
                raise Exception("Missing category input!")
            # Check if there are question inputs
            if not (question or (question_code_type and question_code_example) or question_image_example):
                raise Exception("No question inputs!")
            # Check if there are answer inputs
            if not (answer or (answer_code_type and answer_code_example) or answer_image_example):
                raise Exception("No answer inputs!")
            
            # Process question figures
            elif question_code_example or question_image_example:
                q_figure = FigureModel(
                    code_type=question_code_type, 
                    code_example=question_code_example,
                    image_example=question_image_example)
                
                if not q_figure:
                    raise Exception("Failed to save code or image figure for question")
                else:
                    self.question_figure = q_figure.id

            # Process answer figures
            elif answer_code_example or answer_image_example:
                f_figure = FigureModel(
                    code_type=answer_code_type, 
                    code_example=answer_code_example,
                    image_example=answer_image_example)
                
                if not f_figure:
                    raise Exception("Failed to save code or image figure for answer!")
                else:
                    self.answer_figure = f_figure.id

            self.category = category
            self.question = question
            self.answer = answer

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