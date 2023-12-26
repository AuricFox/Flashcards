import sqlite3, utils

LOGGER = utils.LOGGER

# ==============================================================================================================
def add_card(category:str, question:str, answer:str, code:str=None, code_type:str=None, image_file:str=None):
    '''
    Adds the flashcard data to the database.

    Parameter(s):
        category (str): states what the question is related to
        question (str): information being asked
        answer (str): the expected response to the question
        code (str, default=None): a block of code used to support the question
        code_type (str, default=None): the language of the code block being used
        image_file (str, default=None): a filename of the image that supports the question

    Output(s): 
        Bool: returns true if the data is inserted into the database, else returns false
    '''
    try:
        with sqlite3.connect('flashcards.db') as conn:      # Connection to the database
            category = utils.sanitize(category)             # Sanitizing category before adding

            # Build query using code example and code type
            if code and code_type:
                # Add code elements to the database
                code_query = "INSERT INTO Code (code_block, code_type) VALUES (?,?)"
                code_set = (code, code_type)

                c_code = conn.cursor()
                c_code.execute(code_query, code_set)
                conn.commit()

                # Retrieve the generated primary key (ckey) from the Code table
                cid = c_code.lastrowid

                # Insert flashcard information with the ckey as the foreign key
                flashcard_query = "INSERT INTO Flashcards (category, question, answer, code_id) VALUES (?,?,?,?)"
                flashcard_set = (category, question, answer, cid)

            # Build query using image file
            elif image_file:
                flashcard_query = "INSERT INTO Flashcards (category, question, answer, image_file) VALUES (?,?,?,?)"
                flashcard_set = (category, question, answer, image_file)

            # Build query without code and image examples
            else:
                flashcard_query = "INSERT INTO Flashcards (category, question, answer) VALUES (?,?,?)"
                flashcard_set = (category, question, answer)

            LOGGER.info(f"{flashcard_query}\n{flashcard_set}")

            c = conn.cursor()
            c.execute(flashcard_query, flashcard_set)
            conn.commit()                                   # Commit changes to database

        return True
    
    except sqlite3.Error as e:
        LOGGER.error(f"An error occured when adding to the database: {e}")
        return False

# ==============================================================================================================
def view_card(fid:int):
    '''
    Retrieves the flashcard data with the queried primary key from the database.

    Parameter(s):
        fid (str): the primary key of the flashcard being queried

    Output(s):
        data (dict): a dictionary of the Flashcard data if found, None otherwise

        data = {
            'fid':int, 
            'category':str, 
            'question':str, 
            'answer':str, 
            'code_id':str, 
            'image_file':str, 
            'code':str if code_id not null,
            'code_type':str if code_id not null
        }
    '''
    try:
        with sqlite3.connect('flashcards.db') as conn:    # Connection to the database
            LOGGER.info(f"SELECT * FROM Flashcards WHERE fid = {fid}")

            c = conn.cursor()
            c.execute("SELECT * FROM Flashcards WHERE fid = ?", (fid,))
            # Get the flash data: (category, question, code, image_file, answer)
            card_data = c.fetchone()

            # Convert the tuple into a dictionary
            data = {
                'fid': card_data[0],
                'category': card_data[1],
                'question': card_data[2], 
                'answer': card_data[3],
                'code_id': card_data[4],
                'image_file': card_data[5]
            }

            # Get code elements if code_id is not null
            if data['code_id'] is not None:
                LOGGER.info(f"SELECT * FROM Code WHERE cid = {data['code_id']}")
                c.execute("SELECT * FROM Code WHERE cid = ?", (data['code_id'],))
                code_data = c.fetchone()

                data['code'] = code_data[1]
                data['code_type'] = code_data[2]

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
        data (dict): a dictionary containing the question category and its count if successful, an empty dictionary otherwise

        data = {'category': count})
    '''
    try:
        with sqlite3.connect('flashcards.db') as conn:    # Connection to the database
            LOGGER.info(f"SELECT category, COUNT(*) as count FROM Flashcards GROUP BY category")

            c = conn.cursor()
            c.execute("SELECT category, COUNT(*) as count FROM Flashcards GROUP BY category")
            card_data = c.fetchall()

            data = {}
            for x in card_data:
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
        data (dict): a dictionary containing flashcard data if successful, an dictionary with an empty list otherwise

        data = {
            'questions': [
                {
                'key':int, 
                'category':str, 
                'question':str, 
                'answer':str, 
                'code_id':str, 
                'image_file':str, 
                'code':str if code_id not null,
                'code_type':str if code_id not null
                }, ...
            ]}
    '''
    try:
        with sqlite3.connect('flashcards.db') as conn:    # Connection to the database
            c = conn.cursor()

            # Retrieve all cards in a specified category
            if category:
                LOGGER.info(f"SELECT * FROM Flashcards WHERE category = {category}")
                c.execute("SELECT * FROM Flashcards WHERE category = ?", (category,))
            # Retrieve all cards in the database
            else:
                LOGGER.info(f"SELECT * FROM Flashcards")
                c.execute("SELECT * FROM Flashcards")

            card_data = c.fetchall()

            # Convert the list of tuples into a dictionary
            data = {'questions': []}
            for q in card_data:
                question = {
                    'fid': q[0], 
                    'category': q[1], 
                    'question': q[2], 
                    'answer': q[3], 
                    'code_id': q[4], 
                    'image_file': q[5]
                }
                
                
                
                data['questions'].append(question)


        return data
    
    except sqlite3.Error as e:
        LOGGER.error(f"An error occured when retrieving from the database: {e}")
        return []

# ==============================================================================================================
def update_card(key:int, category:str, question:str, answer:str, code:str=None, code_type:str=None, image_file:str=None):
    '''
    Updates flashcard data in the database.

    Parameters:
        key (int): the primary key of the flashcard being updated
        category (str): states what the question is related to
        question (str): information being asked
        answer (str): the expected response to the question
        code (str, default=None): a block of code used to support the question
        code_type (str, default=None): the language of the code block being used
        image_file (str, default=None): a filename of the image that supports the question

    Returns:
        Bool: True if the update was successful, False otherwise
    '''
    try:
        with sqlite3.connect('flashcards.db') as conn:
            # Sanitize category of special characters
            category = utils.sanitize(category)

            # Construct the SET clause based on the new_data dictionary
            set_clause = 'category = ?, question = ?, code = ?, answer = ?'
            set_query = (category, question, answer)

            c = conn.cursor()
            # Get the current image filename and code block if they exist
            c.execute("SELECT image_file, code FROM Flashcards WHERE key = ?", (key,))
            current_data= c.fetchone()
            current_image_file = current_data[0]
            current_code = current_data[1]
            
            # Update image file if one has been submitted
            if image_file:

                # Delete current image from image folder
                if current_image_file: utils.remove_image(current_image_file)

                set_clause += ', image_file = ?'
                set_query += (image_file,)

            set_query += (key,)

            LOGGER.info(f"UPDATE Flashcards SET {set_clause} WHERE key = ?\n{set_query}")

            
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
            LOGGER.info(f"DELETE FROM Flashcards WHERE key = {key}")

            c = conn.cursor()
            c.execute("DELETE FROM Flashcards WHERE key = ?", (key,))
            conn.commit()

        return True
    
    except sqlite3.Error as e:
        LOGGER.error(f"An error occured when deleting the flashcard from the database: {e}")
        return False