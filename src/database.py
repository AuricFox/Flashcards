import sqlite3, utils

LOGGER = utils.LOGGER

# ==============================================================================================================
def add_card(category:str, question:str, answer:str, code:str=None, code_type:str=None, image_file:str=None):
    '''
    Adds the flashcard data to the database. User can only store code elements or an image and not both. This prevents 
    the flashcard from becoming too cluttered (NOTE: may change in the future).

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
                LOGGER.info(f"{code_query}\n{code_set}")
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

            c = conn.cursor()
            LOGGER.info(f"{flashcard_query}\n{flashcard_set}")
            c.execute(flashcard_query, flashcard_set)
            conn.commit()

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
        response (dict): a dictionary of the Flashcard data if found, None otherwise

        response = {
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
        with sqlite3.connect('flashcards.db') as conn:
            c = conn.cursor()
            LOGGER.info(f"SELECT * FROM Flashcards WHERE fid = {key}")
            c.execute("SELECT * FROM Flashcards WHERE fid = ?", (key,))
            card_data = c.fetchone()

            # Convert the tuple into a dictionary
            response = {
                'fid': card_data[0],
                'category': card_data[1],
                'question': card_data[2], 
                'answer': card_data[3],
                'code_id': card_data[4],
                'image_file': card_data[5]
            }

            # Get code elements if code_id is not null
            if response['code_id'] is not None:
                LOGGER.info(f"SELECT * FROM Code WHERE cid = {response['code_id']}")
                c.execute("SELECT * FROM Code WHERE cid = ?", (response['code_id'],))
                code_data = c.fetchone()

                response['code'] = code_data[1]
                response['code_type'] = code_data[2]

        return response
    
    except sqlite3.Error as e:
        LOGGER.error(f"An error occured when searching the database: {e}")
        return None

# ==============================================================================================================
def view_allcategories():
    '''
    Retrieves all the categories from the database.

    Parameter(s): None

    Output(s):
        response (dict): a dictionary containing the question category and its count if successful, none otherwise

        response = {'category': count}
    '''
    try:
        with sqlite3.connect('flashcards.db') as conn:
            c = conn.cursor()

            LOGGER.info(f"SELECT category, COUNT(*) as count FROM Flashcards GROUP BY category")
            c.execute("SELECT category, COUNT(*) as count FROM Flashcards GROUP BY category")
            card_data = c.fetchall()

            response = {}
            for x in card_data:
                key = x[0]              # Category type
                response[key] = x[1]    # Number of question in the category

        return response
    
    except sqlite3.Error as e:
        LOGGER.error(f"An error occured when retrieving from the database: {e}")
        return None
       
# ==============================================================================================================
def view_allcards(category:str=None):
    '''
    Retrieves all the flashcard data from the database in a specified category.

    Parameter(s):
        category (str, defualt=None): specifies which group of cards to retrieve

    Output(s):
        response (dict): a dictionary containing flashcard data if successful, none otherwise

        response = {
            'questions': [{
                'key':int, 
                'category':str, 
                'question':str, 
                'answer':str, 
                'code_id':str, 
                'image_file':str, 
                'code':str if code_id not null,
                'code_type':str if code_id not null
            }, ... ]}
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
            response = {'questions': []}
            for data in card_data:
                question = {
                    'fid': data[0], 
                    'category': data[1], 
                    'question': data[2], 
                    'answer': data[3], 
                    'code_id': data[4], 
                    'image_file': data[5]
                }
                
                # Retrieve code elements if there is a code_id
                if question['code_id'] is not None:
                    c.execute("SELECT * FROM Code WHERE cid = ?", (question['code_id'],))
                    code_data = c.fetchone()

                    question['code'] = code_data[1]
                    question['code_type'] = code_data[2]
                
                response['questions'].append(question)

        return response
    
    except sqlite3.Error as e:
        LOGGER.error(f"An error occured when retrieving from the database: {e}")
        return None

# ==============================================================================================================
def update_card(key:int, category:str, question:str, answer:str, code:str=None, code_type:str=None, image_file:str=None):
    '''
    Updates flashcard data in the database. User can only store code elements or an image and not both. This prevents 
    the flashcard from becoming too cluttered (NOTE: may change in the future).

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

            c = conn.cursor()
            # Get the current image filename and code block if they exist
            LOGGER.info(f"SELECT image_file, code_id FROM Flashcards WHERE fid = {key}")
            c.execute("SELECT image_file, code_id FROM Flashcards WHERE fid = ?", (key,))
            current_data= c.fetchone()
            current_image_file = current_data[0]
            current_code_id = current_data[1]
            
            # Update image file if one has been submitted along with other elements
            if image_file:
                # Delete current image from image folder
                if current_image_file: utils.remove_image(current_image_file)
                # Delete current code from the database
                if current_code_id: delete_code(current_code_id)

                flashcard_set = (category, question, answer, None, image_file, key)

            # Update code block and code type if changed along with other elements
            elif code and code_type:
                # Delete current image from image folder
                if current_image_file: utils.remove_image(current_image_file)

                # Update code elements if a code_id exists
                if current_code_id:
                    code_query = "UPDATE Code SET code_block = ?, code_type = ? WHERE cid = ?"
                    code_set = (code, code_type, current_code_id)
                # Add new code elements to the code table if code_id does not exist
                else:
                    code_query = "INSERT INTO Code (code_block, code_type) VALUES (?,?)"
                    code_set = (code, code_type)

                # Commit code element changes
                c_code = conn.cursor()
                LOGGER.info(f"{code_query}\n{code_set}")
                c_code.execute(code_query, code_set)
                conn.commit()

                # Retrieve the generated primary key (ckey) from the Code table
                current_code_id = c_code.lastrowid
                flashcard_set = (category, question, answer, current_code_id, None, key)

            # Update basic elements
            else:
                # Delete current image from image folder
                if current_image_file: utils.remove_image(current_image_file)
                # Delete current code from the database
                if current_code_id: delete_code(current_code_id)

                flashcard_set = (category, question, answer, None, None, key)

            flashcard_query = "UPDATE Flashcards SET category = ?, question = ?, answer = ?, code_id = ?, image_file = ? WHERE fid = ?"

            LOGGER.info(f"{flashcard_query}\n{flashcard_set}")
            c.execute(flashcard_query, flashcard_set)
            conn.commit()

        return True
    
    except sqlite3.Error as e:
        LOGGER.error(f"An error occurred when updating the database: {e}")
        return False

# ==============================================================================================================
def delete_card(key:int):
    '''
    Deletes the flashcard data from the database.

    Parameter(s):
        key (int): the primary key of the flashcard being deleted from the database

    Output(s):
        Bool: True if the deletion was successful, False otherwise
    '''
    try:
        with sqlite3.connect('flashcards.db') as conn:    # Connection to the database
            c = conn.cursor()

            # Check for foreign keys to code table
            c.execute("SELECT code_id FROM Flashcards WHERE fid = ?", (key,))
            code = c.fetchone()[0]

            LOGGER.info(f"DELETE FROM Flashcards WHERE fid = {key}")
            c.execute("DELETE FROM Flashcards WHERE fid = ?", (key,))

            conn.commit()

            # Delete code from database
            if code:
                delete_code(code)

        return True
    
    except sqlite3.Error as e:
        LOGGER.error(f"An error occured when deleting the flashcard from the database: {e}")
        return False
    
# ==============================================================================================================
def delete_code(key:int):
    '''
    Deletes the code data from the database.

    Parameter(s):
        key (int): the primary key of the code being deleted from the database

    Output(s):
        Bool: True if the deletion was successful, False otherwise
    '''
    try:
        with sqlite3.connect('flashcards.db') as conn:    # Connection to the database
            c = conn.cursor()

            LOGGER.info(f"DELETE FROM Code WHERE cid = {key}")
            c.execute("DELETE FROM Code WHERE cid = ?", (key,))
            conn.commit()

        return True
    
    except sqlite3.Error as e:
        LOGGER.error(f"An error occured when deleting the code from the database: {e}")
        return False