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

    Output(s): returns if the data is inserted into the database, else returns false
    '''
    try:
        conn = sqlite3.connect('flashcards.db')     # Connection to the database
        c = conn.cursor()
        c.execute(f"INSERT INTO Flashcards VALUES (?,?,?,?,?)", (category,question,code,image,answer))
        conn.commit()                               # Commit changes to database

        return True
    
    except sqlite3.Error as e:
        LOGGER.error(f"An error occured when adding to the database: {e}")
        return False
    
    finally:
        if conn:
            conn.close()                            # Close connection to the database

# ==============================================================================================================
def view_card():
    conn = sqlite3.connect('flashcards.db')     # Connection to the database
    c = conn.cursor()

    conn.commit()                               # Commit changes to database
    conn.close()                                # Close connection to the database
    return

# ==============================================================================================================
def update_card():
    conn = sqlite3.connect('flashcards.db')     # Connection to the database
    c = conn.cursor()

    conn.commit()                               # Commit changes to database
    conn.close()                                # Close connection to the database
    return

# ==============================================================================================================
def delete_card():
    conn = sqlite3.connect('flashcards.db')     # Connection to the database
    c = conn.cursor()

    conn.commit()                               # Commit changes to database
    conn.close()                                # Close connection to the database
    return