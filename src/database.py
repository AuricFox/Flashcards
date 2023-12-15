import sqlite3, utils

LOGGER = utils.LOGGER

# ==============================================================================================================
def add_card(category:str, question:str, answer:str, code:str='NULL', image_path:str='NULL'):
    '''
    Adds the flashcard data to the database.

    Parameter(s):
        category (str): states what the question is related to
        question (str): information being asked
        answer (str): the expected response to the question
        code (str, default='NULL'): a block of code used to support the question
        image_path (str, default='NULL'): a filepath to an image that supports the question

    Output(s): 
        Bool: returns true if the data is inserted into the database, else returns false
    '''
    try:
        with sqlite3.connect('flashcards.db') as conn:      # Connection to the database
            category = utils.sanitize(category)             # Sanitizing category before adding
            LOGGER.info(f"Adding the following row to the database:\n{category}, {question}, {code}, {image_path}, {answer}")

            c = conn.cursor()
            c.execute("INSERT INTO Flashcards (category, question, code, image_path, answer) VALUES (?,?,?,?,?)", (category,question,code,image_path,answer))
            conn.commit()                                   # Commit changes to database

        return True
    
    except sqlite3.Error as e:
        LOGGER.error(f"An error occured when adding to the database: {e}")
        return False

# ==============================================================================================================
def view_card(key:int):
    '''
    Retrieves the flashcard data with the queried primary key from the database.

    Parameter(s):
        key (str): the primary key of the flashcard being queried

    Output(s):
        data (dict={'key':int, 'category':str, 'question':str, 'code':str, 'image_path':str, 'answer':str}): returns a 
        dictionary of the Flashcard data if found, None otherwise
    '''
    try:
        with sqlite3.connect('flashcards.db') as conn:    # Connection to the database
            LOGGER.info(f"Searching the database for the following key:\n{key}")

            c = conn.cursor()
            c.execute("SELECT * FROM Flashcards WHERE key = ?", (key,))
            # Get the flash data: (category, question, code, image_path, answer)
            fd = c.fetchone()

            # Convert the tuple into a dictionary
            data = {'key': fd[0], 'category': fd[1], 'question': fd[2], 'code': fd[3], 'image_path': fd[4], 'answer': fd[5]}

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
        data (dict = {'category': count}): a dictionary containing the question category and its count if successful, 
        an empty dictionary otherwise
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
        return {}
       
# ==============================================================================================================
def view_allcards(category:str=None):
    '''
    Retrieves all the flashcard data from the database in a specified category.

    Parameter(s):
        category (str, defualt=None): specifies which group of cards to retrieve

    Output(s):
        data (dict={'questions':[{'key':int, 'category':str, 'question':str, 'code':str, 'image_path':str, 'answer':str},...]}): a dictionary 
        containing flashcard data if successful, an dictionary with an empty list otherwise
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
                question = {'key': q[0], 'category': q[1], 'question': q[2], 'code': q[3], 'image_path': q[4], 'answer': q[5]}
                data['questions'].append(question)


        return data
    
    except sqlite3.Error as e:
        LOGGER.error(f"An error occured when retrieving from the database: {e}")
        return []

# ==============================================================================================================
def update_card(key:int, new_data:dict):
    '''
    Updates flashcard data in the database.

    Parameters:
        key (int): the primary key of the flashcard being updated
        new_data (dict): a dictionary containing the new data for the flashcard
            {'category': value, 'question': value, 'code', value, 'image_path': value, 'answer':value}

    Returns:
        Bool: True if the update was successful, False otherwise
    '''
    try:
        with sqlite3.connect('flashcards.db') as conn:
            # Check if there is a category and sanitize it
            if 'category' in new_data:
                new_data['category'] = utils.sanitize(new_data['category'])

            LOGGER.info(f"Updating the database with new data:\nKey: {key}\nNew Data: {new_data}")

            c = conn.cursor()
            # Construct the SET clause based on the new_data dictionary
            set_clause = 'category = ?, question = ?, code = ?, answer = ?'
            set_query = (new_data['category'], new_data['question'], new_data['code'], new_data['answer'])

            # Update image file if one has been submitted
            if new_data['image_path'] != '':
                set_clause += ', image_path = ?'
                set_query = (new_data['image_path'],)

            set_query += (key,)

            # Build the query and execute
            query = f"UPDATE Flashcards SET {set_clause} WHERE key = ?"
            c.execute(query, set_query)

            conn.commit()  # Commit changes to the database

        return True
    
    except sqlite3.Error as e:
        LOGGER.error(f"An error occurred when updating the database: {e}")
        return False

# ==============================================================================================================
def delete_card(key:int):
    '''
    Deletes the flashcard data from the database.

    Parameter(s):
        question (str): variable being queried from the database for deletion

    Output(s):
        Bool: True if the delete was successful, False otherwise
    '''
    try:
        with sqlite3.connect('flashcards.db') as conn:    # Connection to the database
            LOGGER.info(f"Deleting the following key from the database:\n{key}")

            c = conn.cursor()
            c.execute("DELETE FROM Flashcards WHERE key = ?", (key,))
            conn.commit()

        return True
    
    except sqlite3.Error as e:
        LOGGER.error(f"An error occured when deleting the flashcard from the database: {e}")
        return False