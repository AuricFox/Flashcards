import sqlite3, sys

sys.path.append('./src/')
import utils

LOGGER = utils.LOGGER

def create_tables():
    '''
    Creates the Code and Flashcards tables used by the flask server.

    Parameter(s): None

    Output(s): 
        Bool: returns true if the tables are created, else returns false
    '''
    
    try:
        with sqlite3.connect('flashcards.db') as conn:      

            c = conn.cursor()
                     # Code elements for supporting the flashcard
            LOGGER.info("""CREATE TABLE Figure(
                    fid INTEGER PRIMARY KEY AUTOINCREMENT,
                    code_block TEXT,
                    code_type TEXT,
                    image_file TEXT
            )""")
            c.execute("""CREATE TABLE Figure(
                    fid INTEGER PRIMARY KEY AUTOINCREMENT,
                    code_block TEXT,
                    code_type TEXT,
                    image_file TEXT
            )""")
        
            # Main flashcard elements
            LOGGER.info("""CREATE TABLE Flashcards(
                    cid INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    figure_id INTEGER REFERENCES Figure(cid)        
            )""")
            c.execute("""CREATE TABLE Flashcards(
                    cid INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    figure_id INTEGER REFERENCES Figure(fid)        
            )""")

            conn.commit()
        
        return True
        
    except Exception as e:
        LOGGER.error(f"An error occured when creating tables: {e}")

# ==============================================================================================================
def clear_tables():
    '''
    Wipes the data from the Code and Flashcards tables used by the flask server. Used for data corruption of 

    Parameter(s): None

    Output(s): 
        Bool: returns true if the tables are wiped, else returns false
    '''

    try:
        with sqlite3.connect('flashcards.db') as conn:
            c = conn.cursor()
            LOGGER.info("DELETE FROM Flashcards")
            c.execute("DELETE FROM Flashcards")

            LOGGER.info("DELETE FROM Figure")
            c.execute("DELETE FROM Figure")
            conn.commit()

        return True
    
    except sqlite3.Error as e:
        LOGGER.error(f"An error occurred when deleting all records from the tables: {e}")
        return False

# ==============================================================================================================
if __name__ == "__main__":
    #clear_tables()
    create_tables()