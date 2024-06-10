from app.extensions import db
from app.utils import LOGGER, save_image_file, remove_image
from sqlalchemy import func

class FigureModel(db.Model):
    '''
    Model for flashcard figures
    '''
    __tablename__ = "figures"

    id = db.Column(db.Integer, primary_key=True)
    code_type = db.Column(db.String(25), nullable=True)
    code_example = db.Column(db.Text, nullable=True)
    image_example = db.Column(db.String(200), nullable=True)

    def __init__(self, code_type:str=None, code_example:str=None, image_example:str=None):
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
                file = save_image_file(image_example)
                # Check if a filename is returned
                if not file: 
                    raise Exception("Failed to save file!")
                else:
                    self.image_example = file
            
            db.session.add(self)
            db.session.flush()
            db.session.commit()
            LOGGER.info(f"Successfully created figure!")
            
        except Exception as e:
            db.session.rollback()
            LOGGER.error(f"An error occurred when entering figure data into the database: {e}")
            raise
    #-----------------------------------------------------------------------------------------------------------
    def update(self, code_type:str=None, code_example:str=None, image_example:str=None):
        '''
        Updates the figure data in the database
        
        Parameter(s):
            code_type (str, default=None): name of the programming language used for the code example
            code_example (str, default=None): a block of code used to support the flashcard
            image_example (str, default=None): a filename of the image used to support the flashcard
        
        Output(s):
            True if the figure is successfully updated, else False
        '''
        try:
            # Check if there are valid figure inputs
            if code_type and code_example and image_example:
                raise Exception("More than one figure type!")
            elif (not code_type and code_example) or (code_type and not code_example):
                raise Exception("Both code type and code example were not provided!")
            elif not code_type and not code_example and not image_example:
                raise Exception("No figure inputs provided!")

            # Check if there is both code type and example if submitted
            if code_type and code_example:
                self.code_type = code_type
                self.code_example = code_example

                if self.image_example:
                    remove_image(self.image_example)
                    self.image_example
            
            # Update image example if there is a new images
            if image_example and not isinstance(image_example, str):
                file = save_image_file(image_example)
                # Check if a filename is returned
                if not file: 
                    raise Exception("Failed to save file!")
                if self.image_example:
                    remove_image(self.image_example)
                
                self.image_example = file
                self.code_type = None
                self.code_example = None
            # Check if the image example is the old image
            elif image_example and isinstance(image_example, str):
                if self.image_example != image_example:
                    raise Exception("Invalid image filename!")

            db.session.flush()
            db.session.commit()
            LOGGER.info(f"Successfully updated figure {self.id}")
            return True

        except Exception as e:
            db.session.rollback()
            LOGGER.error(f"An error occurred when updating figure {self.id} : {e}")
            return False
    #-----------------------------------------------------------------------------------------------------------
    def delete(self):
        '''
        Deletes the figure data from the database

        Parameter(s): None

        Output(s):
            True if the data is successfully deleted, else False
        '''
        try:
            if self.image_example:
                remove_image(self.image_example)

            db.session.delete(self)
            db.session.flush()
            db.session.commit()

            LOGGER.info(f"Successfully Deleted figure {self.id} from the database!")
            return True

        except Exception as e:
            db.session.rollback()
            LOGGER.error(f"An error occurred when deleting figure {self.id} from the database: {e}")
            return False

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
    q_figure = db.Column(db.Integer, nullable=True)
    a_figure = db.Column(db.Integer, nullable=True)

    def __init__(
        self, 
        category:str, 
        question:str=None, 
        answer:str=None, 
        q_code_type:str=None,
        q_code_example:str=None,
        q_image_example:object=None, 
        a_code_type:str=None,
        a_code_example:str=None,
        a_image_example:object=None
    ):
        '''
        Initializes the flashcard data entry into the database

        Parameter(s):
            category (str): the question category
            question (str, default=None): a query about a certain topic
            answer (str, default=None): a response to the question
            q_code_type (str, default=None): the programming language of the question's code example
            q_code_example (str, default=None): a block of code supporting the question
            q_image_example (object, default=None): an image supporting the question
            a_code_type (str, default=None): the programming language of the code example use in the answer
            a_code_example (str, default=None): a block of code supporting the answer
            a_image_example (object, default=None): an image supporting the answer
        
        Output(s): None
        '''
        try:
            # Check if there is a category input
            if not category:
                raise Exception("Missing category input!")
            # Check if there are question inputs
            if not (question or (q_code_type and q_code_example) or q_image_example):
                raise Exception("No question inputs!")
            # Check if there are answer inputs
            if not (answer or (a_code_type and a_code_example) or a_image_example):
                raise Exception("No answer inputs!")
            
            # Process question figures
            if q_code_type or q_code_example or q_image_example:
                q_figure = FigureModel(
                    code_type=q_code_type, 
                    code_example=q_code_example,
                    image_example=q_image_example)
                
                if not q_figure:
                    raise Exception("Failed to save code or image figure for question")
                else:
                    self.q_figure = q_figure.id

            # Process answer figures
            if a_code_type or a_code_example or a_image_example:
                f_figure = FigureModel(
                    code_type=a_code_type, 
                    code_example=a_code_example,
                    image_example=a_image_example)
                
                if not f_figure:
                    raise Exception("Failed to save code or image figure for answer!")
                else:
                    self.a_figure = f_figure.id

            self.category = category
            self.question = question
            self.answer = answer

            db.session.add(self)
            db.session.flush()
            db.session.commit()
            LOGGER.info(f"Successfully created flashcard: {self.id}")

        except Exception as e:
            db.session.rollback()
            LOGGER.error(f"An error occurred when entering flashcard data into the database: {e}")
            raise
    #-----------------------------------------------------------------------------------------------------------
    def view(self):
        '''
        Fetches the flashcard data for viewing

        Parameter(s): None

        Output(s):
            response (dict): a dictionary of the Flashcard data if successful, else None

            response = {
                'id':int, 
                'category':str, 
                'question':str, 
                'answer':str, 
                'q_code_type':str,
                'q_code_example':str,
                'q_image_example':str,
                'a_code_type':str,
                'a_code_example':str,
                'a_image_example':str
            }
        '''
        try:
            response = {}

            # Get flashcard figures if there are any
            q_figure = FigureModel.query.get(self.q_figure) if self.q_figure else None
            a_figure = FigureModel.query.get(self.a_figure) if self.a_figure else None

            response = {
                'id': self.id,
                'category': self.category,
                'question': self.question,
                'answer': self.answer,
                'q_code_type': q_figure.code_type if q_figure else None,
                'q_code_example': q_figure.code_example if q_figure else None,
                'q_image_example': q_figure.image_example if q_figure else None,
                'a_code_type': a_figure.code_type if a_figure else None,
                'a_code_example': a_figure.code_example if a_figure else None,
                'a_image_example': a_figure.image_example if a_figure else None
            }

            return response
        
        except Exception as e:
            LOGGER.error(f"An error occurred when fetching flashcard {self.id} data: {e}")
            return None

    #-----------------------------------------------------------------------------------------------------------
    def update(
        self,
        category:str, 
        question:str=None, 
        answer:str=None, 
        q_code_type:str=None,
        q_code_example:str=None,
        q_image_example:object=None, 
        a_code_type:str=None,
        a_code_example:str=None,
        a_image_example:object=None
    ):
        '''
        Updates the flashcard data in the database

        Parameter(s):
            category (str): the question category
            question (str, default=None): a query about a certain topic
            answer (str, default=None): a response to the question
            q_code_type (str, default=None): the programming language of the question's code example
            q_code_example (str, default=None): a block of code supporting the question
            q_image_example (object, default=None): an image supporting the question
            a_code_type (str, default=None): the programming language of the code example use in the answer
            a_code_example (str, default=None): a block of code supporting the answer
            a_image_example (object, default=None): an image supporting the answer
        
        Output(s): 
            True if the flashcard is successfully updated, else False
        '''
        try:
            self.category = category
            self.question = question
            self.answer = answer

            # Update question figure if there is one
            if self.q_figure:
                figure = FigureModel.query.get(self.q_figure)

                # Check if there are figure inputs for question, if not delete the figure
                if not (q_code_type or q_code_example or q_image_example):
                    status = figure.delete()
                    self.q_figure = None
                else:
                    status = figure.update(code_type=q_code_type, code_example=q_code_example, image_example=q_image_example)

                if not status:
                    raise Exception(f"Failed to update question figure for flashcard {self.id}!")
            # Create question figure if there are inputs
            elif not self.q_figure and (q_code_type or q_code_example or q_image_example):
                q_figure = FigureModel(code_type=q_code_type, code_example=q_code_example, image_example=q_image_example)

                if not q_figure:
                    raise Exception(f"Failed to create question figure for flashcard: {self.id}!")
                
                self.q_figure = q_figure.id

            # Update answer figure if there is one
            if self.a_figure:
                figure = FigureModel.query.get(self.a_figure)
                
                # Check if there are figure inputs for answer, if not delete the figure
                if not (a_code_type or a_code_example or a_image_example):
                    status = figure.delete()
                    self.a_figure = None
                else:
                    status = figure.update(code_type=a_code_type, code_example=a_code_example, image_example=a_image_example)

                if not status:
                    raise Exception(f"Failed to update answer figure for flashcard {self.id}!")
            # Create answer figure if there are inputs
            elif not self.a_figure and (a_code_type or a_code_example or a_image_example):
                a_figure = FigureModel(code_type=a_code_type, code_example=a_code_example, image_example=a_image_example)

                if not a_figure:
                    raise Exception(f"Failed to create question figure for flashcard: {self.id}!")
                
                self.a_figure = a_figure.id

            db.session.flush()
            db.session.commit()
            LOGGER.info(f"Successfully updated flashcard ID: {self.id}")
            return True

        except Exception as e:
            db.session.rollback()
            LOGGER.error(f"An error occurred when updating the flashcard data: {e}")
            return False
    #-----------------------------------------------------------------------------------------------------------
    def delete(self):
        '''
        Deletes all the flashcard data and its figures from the database
        
        Parameter(s): None
        
        Output(s):
            True if the flashcard data was successfully deleted, else False
        '''
        try:
            if self.q_figure:
                figure = FigureModel.query.get(self.q_figure)
                figure.delete()
            if self.a_figure:
                figure = FigureModel.query.get(self.a_figure)
                figure.delete()

            db.session.delete(self)
            db.session.flush()
            db.session.commit()

            LOGGER.info(f"Successfully deleted flashcard {self.id} from the database!")
            return True

        except Exception as e:
            db.session.rollback()
            LOGGER.error(f"An error occurred when deleting flashcard {self.id} from the database: {e}")
            return False
    #-----------------------------------------------------------------------------------------------------------
    def __repr__(self):
        return (
            f"Category: {self.category}\n"
            f"Question: {self.question}\n"
            f"Answer: {self.answer}\n"
            f"Question figure ID: {self.q_figure}\n"
            f"Answer figure ID: {self.a_figure}"
        )
    
# ==============================================================================================================
# Functions for performing queries
# ==============================================================================================================
def view_all_cards(category:str=None):
    '''
    Fetches flashcards from the database with a matching category
    
    Parameter(s):
        category (str, default=None): the question category the flashcards are being filtered by
        
    Output(s):
        Returns a dictionary list of all the related flashcard data, else returns an empty list

        response = [{
            'id':int, 
            'category':str, 
            'question':str, 
            'answer':str, 
            'qid':int,
            'aid':int, 
            'q_code':str,
            'q_code_type':str,
            'q_image_example':str,
            'a_code':str,
            'a_code_type':str,
            'a_image_example':str
        }, ... ]
    '''
    try:
        # Return the flashcards with the specified category
        if category:
            flashcards = FlashcardModel.query.filter_by(category=category).all()
        # Return all Flashcards
        else:
            flashcards = FlashcardModel.query.all()

        response = []
        for flashcard in flashcards:

            # Get flashcard figures if there are any
            q_figure = FigureModel.query.get(flashcard.q_figure) if flashcard.q_figure else None
            a_figure = FigureModel.query.get(flashcard.a_figure) if flashcard.a_figure else None

            response.append({
                'id': flashcard.id,
                'category': flashcard.category,
                'question': flashcard.question,
                'answer': flashcard.answer,
                'q_code_type': q_figure.code_type if q_figure else None,
                'q_code_example': q_figure.code_example if q_figure else None,
                'q_image_example': q_figure.image_example if q_figure else None,
                'a_code_type': a_figure.code_type if a_figure else None,
                'a_code_example': a_figure.code_example if a_figure else None,
                'a_image_example': a_figure.image_example if a_figure else None
            })

        return response
        
    except Exception as e:
        LOGGER.error(f"An error occurred when fetching flashcard data: {e}")
        return []
# ==============================================================================================================
def view_all_categories():
    '''
    Fetches all the categories from the database
    
    Parameter(s): None
    
    Output(s):
        response (dict): a dictionary containing the question category and its count if successful, else an empty list

        response = {category: count, ... }
    '''
    try:
        categories = db.session.query(
            FlashcardModel.category, 
            func.count(FlashcardModel.id)
        ).group_by(FlashcardModel.category).all()

        response = {}
        for category in categories:
            response[category[0]] = category[1]

        return response

    except Exception as e:
        LOGGER.error(f"An error occurred when fetching categories from the database: {e}")
        return {}