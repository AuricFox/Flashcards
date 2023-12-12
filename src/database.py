import sqlite3, utils

LOGGER = utils.LOGGER

# ==============================================================================================================
def add_card(category:str, question:str, answer:str, code:str='NULL', image:str='NULL'):
    '''
    Adds the flashcard data to the database.

    Parameter(s):
        category (str): states what the question is related to
        question (str): information being asked
        answer (str): the expected response to the question
        code (str, default='NULL'): a block of code used to support the question
        image (str, default='NULL'): a filepath to an image that supports the question

    Output(s): 
        returns if the data is inserted into the database, else returns false
    '''
    try:
        with sqlite3.connect('flashcards.db') as conn:      # Connection to the database
            LOGGER.info(f"Adding the following row to the database:\n{category}, {question}, {code}, {image}, {answer}")

            c = conn.cursor()
            c.execute("INSERT INTO Flashcards VALUES (?,?,?,?,?)", (category,question,code,image,answer))
            conn.commit()                                   # Commit changes to database

        return True
    
    except sqlite3.Error as e:
        LOGGER.error(f"An error occured when adding to the database: {e}")
        return False

# ==============================================================================================================
def view_card(question:str):
    '''
    Retrieves the flashcard data with the queried question from the database.

    Parameter(s):
        question (str): variable being queried from the database

    Output(s):
        returns a dictionary of the Flashcard data if found, None otherwise
    '''
    try:
        with sqlite3.connect('flashcards.db') as conn:    # Connection to the database
            LOGGER.info(f"Searching the database for the following question:\n{question}")

            c = conn.cursor()
            c.execute("SELECT * FROM Flashcards WHERE question = ?", (question,))
            # Get the flash data: (category, question, code, image, answer)
            fd = c.fetchone()

            # Convert the tuple into a dictionary
            data = {'category': fd[0], 'question': fd[1], 'code': fd[2], 'image': fd[3], 'answer': fd[4]}

        return data
    
    except sqlite3.Error as e:
        LOGGER.error(f"An error occured when searching the database: {e}")
        return None

# ==============================================================================================================
def view_allcategories():
    '''
    Retrieves all the categories from the database.

    Parameter(s): None

    Output(s):
        a dictionary containing the question category and its count if successful, an empty dictionary otherwise
    '''
    try:
        with sqlite3.connect('flashcards.db') as conn:    # Connection to the database
            LOGGER.info(f"Retrieving all categories from the database.")

            c = conn.cursor()
            c.execute("SELECT category, COUNT(*) as count FROM Flashcards GROUP BY category")
            fd = c.fetchall()

            data = {}
            for x in fd:
                key = x[0]          # Category type
                data[key] = x[1]    # Number of question in the category

        return data
    
    except sqlite3.Error as e:
        LOGGER.error(f"An error occured when retrieving from the database: {e}")
        return []
       
# ==============================================================================================================
def view_allcards(category:str=None):
    '''
    Retrieves all the flashcard data from the database in a specified category.

    Parameter(s):
        category (str, defualt=None): specifies which group of cards to retrieve

    Output(s):
        a dictionary containing flashcard data if successful, an dictionary with an empty list otherwise
    '''
    try:
        with sqlite3.connect('flashcards.db') as conn:    # Connection to the database
            c = conn.cursor()

            # Retrieve all cards in a specified category
            if category:
                LOGGER.info(f"Retrieving {category} flashcards from the database.")
                c.execute("SELECT * FROM Flashcards WHERE category = ?", (category,))
            # Retrieve all cards in the database
            else:
                LOGGER.info(f"Retrieving all flashcards from the database.")
                c.execute("SELECT * FROM Flashcards")

            flash_data = c.fetchall()

            # Convert the list of tuples into a dictionary
            data = {'questions': []}
            for q in flash_data:
                question = {'category': q[0], 'question': q[1], 'code': q[2], 'image': q[3], 'answer': q[4]}
                data['questions'].append(question)


        return data
    
    except sqlite3.Error as e:
        LOGGER.error(f"An error occured when retrieving from the database: {e}")
        return []

# ==============================================================================================================
def update_card(old_question:str, new_data:dict):
    '''
    Updates flashcard data in the database.

    Parameters:
        old_question (str): the original question identifying the flashcard to be updated
        new_data (dict): a dictionary containing the new data for the flashcard
            {'category': value, 'question': value, 'code', value, 'image': value, 'answer':value}

    Returns:
        bool: True if the update was successful, False otherwise
    '''
    try:
        with sqlite3.connect('flashcards.db') as conn:
            LOGGER.info(f"Updating the following quetion with new data:\nOld Question: {old_question}\nNew Data: {new_data}")

            c = conn.cursor()
            # Construct the SET clause dynamically based on the new_data dictionary
            set_clause = ', '.join(f"{key} = ?" for key in new_data.keys())

            # Build the query and execute
            query = f"UPDATE Flashcards SET {set_clause} WHERE question = ?"
            c.execute(query, (old_question,))

            conn.commit()  # Commit changes to the database

        return True
    
    except sqlite3.Error as e:
        LOGGER.error(f"An error occurred when updating the database: {e}")
        return False

# ==============================================================================================================
def delete_card(question:str):
    '''
    Deletes the flashcard data from the database.

    Parameter(s):
        question (str): variable being queried from the database for deletion

    Output(s):
        bool: True if the delete was successful, False otherwise
    '''
    try:
        with sqlite3.connect('flashcards.db') as conn:    # Connection to the database
            LOGGER.info(f"Deleting the following question from the database:\n{question}")

            c = conn.cursor()
            c.execute("DELETE FROM Flashcards WHERE question = ?", (question,))
            conn.commit()

        return True
    
    except sqlite3.Error as e:
        LOGGER.error(f"An error occured when deleting the question from the database: {e}")
        return False