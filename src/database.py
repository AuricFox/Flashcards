import sqlite3, utils

LOGGER = utils.LOGGER

def Create_Table(table:str, items:[str], types:[str]):

    if len(items) != len(types):
        return 
    return

# ==============================================================================================================
def add_card(category:str, question:str, code:str, image:str, answer:str):
    '''
    Adds the flashcard data to the database.

    Parameter(s):
        category (str): states what the question is related to
        question (str): information being asked
        code (str): a block of code used to support the question
        image (str): a filepath to an image that supports the question
        answer (str): the expected response to the question

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
def view_card(question):
    '''
    Adds the flashcard data to the database.

    Parameter(s):
        question (str): information being asked

    Output(s):
        returns a tuple of the Flashcard data if found, None otherwise
    '''
    try:
        with sqlite3.connect('flashcards.db') as conn:    # Connection to the database
            LOGGER.info(f"Searching the database for the following question:\n{question}")

            c = conn.cursor()
            c.execute("SELECT * FROM Flashcards WHERE question = ?", (question,))
            data = c.fetchone()
            conn.commit()

        return data
    
    except sqlite3.Error as e:
        LOGGER.error(f"An error occured when searching the database: {e}")
        return None

# ==============================================================================================================
def update_card(old_question: str, new_data: dict):
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
def delete_card():
    conn = sqlite3.connect('flashcards.db')     # Connection to the database
    c = conn.cursor()

    conn.commit()                               # Commit changes to database
    conn.close()                                # Close connection to the database
    return