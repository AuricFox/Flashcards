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
                figure_query = "INSERT INTO Figure (code_block, code_type) VALUES (?,?)"
                figure_set = (code, code_type)

                c_figure = conn.cursor()
                LOGGER.info(f"{figure_query}\n{figure_set}")
                c_figure.execute(figure_query, figure_set)
                conn.commit()

                # Retrieve the generated primary key (fid) from the Figure table
                fid = c_figure.lastrowid

                # Insert flashcard information with the fid as the foreign key
                flashcard_query = "INSERT INTO Flashcards (category, question, answer, figure_id) VALUES (?,?,?,?)"
                flashcard_set = (category, question, answer, fid)

            # Build query using image file
            elif image_file:
                # Add image elements to the database
                figure_query = "INSERT INTO Figure (image_file) VALUES (?)"
                figure_set = (image_file,)

                i_figure = conn.cursor()
                LOGGER.info(f"{figure_query}\n{figure_set}")
                i_figure.execute(figure_query, figure_set)
                conn.commit()

                # Retrieve the generated primary key (fid) from the Figure table
                fid = i_figure.lastrowid

                flashcard_query = "INSERT INTO Flashcards (category, question, answer, figure_id) VALUES (?,?,?,?)"
                flashcard_set = (category, question, answer, fid)

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
            'key':int, 
            'category':str, 
            'question':str, 
            'answer':str, 
            'figure_id':int,  
            'code':str,
            'code_type':str,
            'image_file':str,
        }
    '''
    try:
        with sqlite3.connect('flashcards.db') as conn:
            c = conn.cursor()
            LOGGER.info(f"SELECT * FROM Flashcards WHERE cid = {key}")
            c.execute("SELECT * FROM Flashcards WHERE cid = ?", (key,))
            card_data = c.fetchone()

            # Convert the tuple into a dictionary
            response = {
                'key': card_data[0],
                'category': card_data[1],
                'question': card_data[2], 
                'answer': card_data[3],
                'figure_id': card_data[4]
            }

            # Get figure elements if figure_id is not null
            if response['figure_id'] is not None:
                LOGGER.info(f"SELECT * FROM Figure WHERE fid = {response['figure_id']}")
                c.execute("SELECT * FROM Figure WHERE fid = ?", (response['figure_id'],))
                figure_data = c.fetchone()

                response['code'] = figure_data[1]
                response['code_type'] = figure_data[2]
                response['file_image'] = figure_data[3]

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
                'figure_id':int, 
                'image_file':str, 
                'code':str,
                'code_type':str
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
                    'key': data[0], 
                    'category': data[1], 
                    'question': data[2], 
                    'answer': data[3], 
                    'figure_id': data[4]
                }
                
                # Retrieve figure elements if there is a figure_id
                if question['figure_id'] is not None:
                    c.execute("SELECT * FROM Figure WHERE fid = ?", (question['figure_id'],))
                    figure_data = c.fetchone()

                    question['code'] = figure_data[1]
                    question['code_type'] = figure_data[2]
                    question['image_file'] = figure_data[3]
                
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
            # Get the current image filename or code block if they exist
            LOGGER.info(f"SELECT figure_id FROM Flashcards WHERE cid = {key}")
            c.execute("SELECT figure_id FROM Flashcards WHERE cid = ?", (key,))
            figure_id = c.fetchone()[0]

            if figure_id is not None:
                LOGGER.info(f"SELECT image_file FROM Figure WHERE fid = {figure_id}")
                c.execute("SELECT image_file FROM Figure WHERE fid = ?", (figure_id,))

                current_image_file = c.fetchone()[0]
            
            # Update image file if one has been submitted along with other elements
            if image_file:
                # Delete current image from image folder
                if current_image_file: utils.remove_image(current_image_file)
                
                # Update image element in the Figure table if a figure_id exists
                if figure_id:
                    figure_query = "UPDATE Figure SET image_file = ? WHERE fid = ?"
                    figure_set = (image_file, figure_id)
                # Add new image element to the Figure table if figure_id does not exist
                else:
                    figure_query = "INSERT INTO Figure (image_file) VALUES (?)"
                    figure_set = (image_file,)

                # Commit image element changes
                c_figure = conn.cursor()
                LOGGER.info(f"{figure_query}\n{figure_set}")
                c_figure.execute(figure_query, figure_set)
                conn.commit()

                # Retrieve the generated primary key (fid) from the Figure table
                figure_id = c_figure.lastrowid if figure_id is None else figure_id
                flashcard_set = (category, question, answer, figure_id, key)

            # Update code block and code type if changed along with other elements
            elif code and code_type:
                # Delete current image from image folder
                if current_image_file: utils.remove_image(current_image_file)

                # Update code elements in the Figure table if a figure_id exists
                if figure_id:
                    figure_query = "UPDATE Figure SET code_block = ?, code_type = ? WHERE fid = ?"
                    figure_set = (code, code_type, figure_id)
                # Add new code elements to the Figure table if figure_id does not exist
                else:
                    figure_query = "INSERT INTO Figure (code_block, code_type) VALUES (?,?)"
                    figure_set = (code, code_type)

                # Commit code element changes
                c_figure = conn.cursor()
                LOGGER.info(f"{figure_query}\n{figure_set}")
                c_figure.execute(figure_query, figure_set)
                conn.commit()

                # Retrieve the generated primary key (fid) from the Figure table
                figure_id = c_figure.lastrowid if figure_id is None else figure_id
                flashcard_set = (category, question, answer, figure_id, key)

            # Update basic elements
            else:
                # Delete current image from image folder
                if current_image_file: utils.remove_image(current_image_file)
                # Delete current figure from the database
                if figure_id: delete_figure(figure_id)

                flashcard_set = (category, question, answer, None, key)

            flashcard_query = "UPDATE Flashcards SET category = ?, question = ?, answer = ?, figure_id = ? WHERE cid = ?"

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

            # Check for foreign keys to Figure table
            c.execute("SELECT figure_id FROM Flashcards WHERE cid = ?", (key,))
            figure_id = c.fetchone()[0]

            LOGGER.info(f"DELETE FROM Flashcards WHERE cid = {key}")
            c.execute("DELETE FROM Flashcards WHERE cid = ?", (key,))

            conn.commit()

            # Delete figure from database
            if figure_id:
                delete_figure(figure_id)

        return True
    
    except sqlite3.Error as e:
        LOGGER.error(f"An error occured when deleting the flashcard from the database: {e}")
        return False
    
# ==============================================================================================================
def delete_figure(key:int):
    '''
    Deletes the figure data from the database.

    Parameter(s):
        key (int): the primary key of the figure being deleted from the database

    Output(s):
        Bool: True if the deletion was successful, False otherwise
    '''
    try:
        with sqlite3.connect('flashcards.db') as conn:    # Connection to the database
            c = conn.cursor()

            LOGGER.info(f"DELETE FROM Figure WHERE fid = {key}")
            c.execute("DELETE FROM Figure WHERE fid = ?", (key,))
            conn.commit()

        return True
    
    except sqlite3.Error as e:
        LOGGER.error(f"An error occured when deleting the figure from the database: {e}")
        return False