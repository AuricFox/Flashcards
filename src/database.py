import sqlite3, utils

LOGGER = utils.LOGGER

# ==============================================================================================================
def add_figure(code_block:str=None, code_type:str=None, image_file:str=None):
    '''
    Adds the figure data to the database. User can only store code elements or an image and not both. This prevents 
    the flashcard from becoming too cluttered (NOTE: may change in the future).

    Parameter(s):
        code_block (str, default=None): a block of code used to support the question
        code_type (str, default=None): the language of the code block being used
        image_file (str, default=None): a filename of the image that supports the question

    Output(s): 
        key: returns the primary key od the figure if the data is inserted into the database, else returns None
    '''
    try:
        with sqlite3.connect('flashcards.db') as conn:
            # Build query using image file
            if image_file:
                # Add image elements to the database
                figure_query = "INSERT INTO Figure (image_file) VALUES (?)"
                figure_set = (image_file,)

                i_figure = conn.cursor()
                LOGGER.info(f"{figure_query}\n{figure_set}")
                i_figure.execute(figure_query, figure_set)
                conn.commit()

                # Retrieve the generated primary key (fid) from the Figure table
                key = i_figure.lastrowid
            
            # Build query using code example and code type
            elif code_block and code_type:
                # Add code elements to the database
                figure_query = "INSERT INTO Figure (code_block, code_type) VALUES (?,?)"
                figure_set = (code_block, code_type)

                c_figure = conn.cursor()
                LOGGER.info(f"{figure_query}\n{figure_set}")
                c_figure.execute(figure_query, figure_set)
                conn.commit()

                # Retrieve the generated primary key (fid) from the Figure table
                key = c_figure.lastrowid
            
            else:
                LOGGER.info("No figure inputs entered!")
                key = None

            return key

    except sqlite3.Error as e:
        LOGGER.error(f"An error occured when adding figure to the database: {e}")
        return None  

# ==============================================================================================================
def add_card(data:dict):
    '''
    Adds the flashcard data to the database. User can only store code elements or an image and not both. This prevents 
    the flashcard from becoming too cluttered (NOTE: may change in the future).

    Parameter(s):
        data (dict): a dictionary that can contain the following inputs

        category (str): states what the question is related to
        question (str): information being asked
        answer (str): the expected response to the question
        q_code_block (str, default=None): a block of code used to support the question
        q_code_type (str, default=None): the language of the code block being used in the question
        q_image_file (str, default=None): a filename of the image that supports the question
        a_code_block (str, default=None): a block of code used to support the answer
        a_code_type (str, default=None): the language of the code block being used in the answer
        a_image_file (str, default=None): a filename of the image that supports the answer

    Output(s): 
        Bool: returns true if the data is inserted into the database, else returns false
    '''
    try:
        with sqlite3.connect('flashcards.db') as conn:      # Connection to the database
            category = utils.sanitize(data['category'])     # Sanitizing category before adding
            question = data.get('question')
            answer = data.get('answer')
            
            # Retrieve the generated primary key(s) for question and/or answer figure(s)
            qid = add_figure(code_block=data.get('q_image_file'), code_type=data.get('a_code_type'), image_file=data.get('q_image_file'))
            aid = add_figure(code_block=data.get('a_image_file'), code_type=data.get('a_code_type'), image_file=data.get('a_image_file'))

            if question is None and qid is None:
                # Question side of flashcard is blank
                LOGGER.warning("Question side is blank!")
                return False
            
            if answer is None and aid is None:
                # Answer side of flashcard is blank
                LOGGER.warning("Answer side is blank!")
                return False

            flashcard_query = "INSERT INTO Flashcards (category, question, answer, qid, aid) VALUES (?,?,?,?,?)"
            flashcard_set = (category, question, answer, qid, aid)

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
            'qid':int,
            'aid':int, 
            'q_code':str,
            'q_code_type':str,
            'q_image_file':str,
            'a_code':str,
            'a_code_type':str,
            'a_image_file':str
        }

    +-----+-----------+------------+----------+-----+-----+----------------+---------------+----------------+----------------+---------------+----------------+
    | cid | category  | question   | answer   | qid | aid | qid_code_block | qid_code_type | qid_image_file | aid_code_block | aid_code_type | aid_image_file |
    +-----+-----------+------------+----------+-----+-----+----------------+---------------+----------------+----------------+---------------+----------------+
    '''
    try:
        with sqlite3.connect('flashcards.db') as conn:
            c = conn.cursor()
            LOGGER.info(f"Selecting data from tables where cid = {key}...")
            c.execute("""
                SELECT 
                    Flashcards.cid,
                    Flashcards.category,
                    Flashcards.question,
                    Flashcards.answer,
                    Flashcards.qid,
                    Flashcards.aid,
                    QFigure.code_block AS q_code_block,
                    QFigure.code_type AS q_code_type,
                    QFigure.image_file AS q_image_file,
                    AFigure.code_block AS a_code_block,
                    AFigure.code_type AS a_code_type,
                    AFigure.image_file AS a_image_file
                FROM Flashcards
                LEFT JOIN Figure AS QFigure ON Flashcards.qid = QFigure.fid
                LEFT JOIN Figure AS AFigure ON Flashcards.aid = AFigure.fid
                WHERE Flashcards.cid = ?
                """, (key,))

            data = c.fetchone()

            # Convert the tuple into a dictionary
            response = {
                'key': data[0], 
                'category': data[1], 
                'question': data[2], 
                'answer': data[3], 
                'qid': data[4], 
                'aid': data[5],
                'q_code_block': data[6], 
                'q_code_type': data[7], 
                'q_image_file': data[8],
                'a_code_block': data[9], 
                'a_code_type': data[10], 
                'a_image_file': data[11],
            }

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
                'qid':int,
                'aid':int, 
                'q_code':str,
                'q_code_type':str,
                'q_image_file':str,
                'a_code':str,
                'a_code_type':str,
                'a_image_file':str
            }, ... ]}
    '''
    try:
        with sqlite3.connect('flashcards.db') as conn:    # Connection to the database
            c = conn.cursor()

            # Retrieve all cards in a specified category
            if category:
                LOGGER.info(f"Selecting data from Flashcards category = {category}")
                c.execute("""
                    SELECT 
                        Flashcards.cid,
                        Flashcards.category,
                        Flashcards.question,
                        Flashcards.answer,
                        Flashcards.qid,
                        Flashcards.aid,
                        QFigure.code_block AS q_code_block,
                        QFigure.code_type AS q_code_type,
                        QFigure.image_file AS q_image_file,
                        AFigure.code_block AS a_code_block,
                        AFigure.code_type AS a_code_type,
                        AFigure.image_file AS a_image_file
                    FROM Flashcards
                    LEFT JOIN Figure AS QFigure ON Flashcards.qid = QFigure.fid
                    LEFT JOIN Figure AS AFigure ON Flashcards.aid = AFigure.fid
                    WHERE Flashcards.category = ?
                    """, (category,))
            # Retrieve all cards in the database
            else:
                LOGGER.info(f"SELECT * FROM Flashcards")
                c.execute("""
                    SELECT 
                        Flashcards.cid,
                        Flashcards.category,
                        Flashcards.question,
                        Flashcards.answer,
                        Flashcards.qid,
                        Flashcards.aid,
                        QFigure.code_block AS q_code_block,
                        QFigure.code_type AS q_code_type,
                        QFigure.image_file AS q_image_file,
                        AFigure.code_block AS a_code_block,
                        AFigure.code_type AS a_code_type,
                        AFigure.image_file AS a_image_file
                    FROM Flashcards
                    LEFT JOIN Figure AS QFigure ON Flashcards.qid = QFigure.fid
                    LEFT JOIN Figure AS AFigure ON Flashcards.aid = AFigure.fid
                    """)

            card_data = c.fetchall()

            # Convert the list of tuples into a dictionary
            response = {'questions': []}
            for data in card_data:
                question = {
                    'key': data[0], 
                    'category': data[1], 
                    'question': data[2], 
                    'answer': data[3], 
                    'qid': data[4], 
                    'aid': data[5],
                    'q_code_block': data[6], 
                    'q_code_type': data[7], 
                    'q_image_file': data[8],
                    'a_code_block': data[9], 
                    'a_code_type': data[10], 
                    'a_image_file': data[11],
                }
                
                response['questions'].append(question)

        return response
    
    except sqlite3.Error as e:
        LOGGER.error(f"An error occured when retrieving from the database: {e}")
        return None

# ==============================================================================================================
def update_figure(key:int, code_block:str=None, code_type:str=None, image_file:str=None):
    '''
    Updates the figure data to the database. User can only store code elements or an image and not both. This prevents 
    the flashcard from becoming too cluttered (NOTE: may change in the future).

    Parameter(s):
        key (int): the primary key of the figure
        code_block (str, default=None): a block of code used to support the question
        code_type (str, default=None): the language of the code block being used
        image_file (str, default=None): a filename of the image that supports the question

    Output(s): 
        key: returns the primary key od the figure if the data is inserted into the database, else returns None
    '''
    try:
        with sqlite3.connect('flashcards.db') as conn:

            c = conn.cursor()
            # Get the current image filename or code block if they exist
            LOGGER.info(f"SELECT image_file FROM Figure WHERE fid = {key}")
            c.execute("SELECT image_file FROM Figure WHERE fid = ?", (key,))
            current_image = c.fetchone()[0]

            # Build query using a new image file
            if image_file and image_file != current_image:
                # Add image elements to the database
                figure_query = "UPDATE Figure SET code_block = ?, code_type = ?, image_file = ? WHERE fid = ?"
                figure_set = (None, None, image_file, key)
            
            # New image is the same as the current image
            elif image_file and image_file == current_image:
                return key

            # Build query using code example and code type
            elif code_block and code_type:
                # Add code elements to the database
                figure_query = "UPDATE Figure SET code_block = ?, code_type = ?, image_file = ? WHERE fid = ?"
                figure_set = (code_block, code_type, None, key)
            
            # Nothing to update
            else:
                LOGGER.info("No figure inputs updated!")
                return None

            LOGGER.info(f"{figure_query}\n{figure_set}")
            c.execute(figure_query, figure_set)
            conn.commit()

            if current_image: utils.remove_image(current_image)

            return key

    except sqlite3.Error as e:
        LOGGER.error(f"An error occured when updating figure to the database: {e}")
        return None
# ==============================================================================================================
def update_card(data:dict):
    '''
    Updates flashcard data in the database. User can only store code elements or an image and not both. This prevents 
    the flashcard from becoming too cluttered (NOTE: may change in the future).

    Parameters:
        data (dict): a dictionary that can contain the following inputs

        key (int): the primary key of the flashcard being updated
        category (str): states what the question is related to
        question (str): information being asked
        answer (str): the expected response to the question
        q_code_block (str, default=None): a block of code used to support the question
        q_code_type (str, default=None): the language of the code block being used in the question
        q_image_file (str, default=None): a filename of the image that supports the question
        a_code_block (str, default=None): a block of code used to support the answer
        a_code_type (str, default=None): the language of the code block being used in the answer
        a_image_file (str, default=None): a filename of the image that supports the answer

    Returns:
        Bool: True if the update was successful, False otherwise
    '''
    try:
        with sqlite3.connect('flashcards.db') as conn:
            key = data.get('key')
            category = utils.sanitize(data.get('category'))     # Sanitize category of special characters
            question = data.get('question')
            answer = data.get('answer')

            c = conn.cursor()
            # Get the current figure info
            LOGGER.info(f"SELECT qid, aid FROM Flashcards WHERE cid = {key}")
            c.execute("SELECT qid, aid FROM Flashcards WHERE cid = ?", (key,))
            result = c.fetchone()
            qid = result[0] if result is not None else None
            aid = result[1] if result is not None else None

            q_code_block = data.get('q_code_block')
            q_code_type = data.get('q_code_type')
            q_image_file = data.get('q_image_file')

            a_code_block = data.get('a_code_block')
            a_code_type = data.get('a_code_type')
            a_image_file = data.get('a_image_file')

            # Update current question figure
            if qid:
                qid = update_figure(qid, code_block=q_code_block, code_type=q_code_type, image_file=q_image_file)
            # Add a question figure
            elif qid is None and q_code_block and q_code_type and q_image_file:
                qid = add_figure(code_block=q_code_block, code_type=q_code_type, image_file=q_image_file)
            else:
                qid = None

            # Update curent answer figure
            if aid:
                aid = update_figure(aid, code_block=a_code_block, code_type=a_code_type, image_file=a_image_file)
            # Add a answer figure
            elif aid is None and a_code_block and a_code_type and a_image_file:
                aid = add_figure(code_block=a_code_block, code_type=a_code_type, image_file=a_image_file)
            else:
                aid = None

            flashcard_query = "UPDATE Flashcards SET category = ?, question = ?, answer = ?, qid = ?, aid = ? WHERE cid = ?"
            flashcard_set = (category, question, answer, qid, aid, key)

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
            c.execute("""
                SELECT 
                    Flashcards.qid,
                    Flashcards.aid,
                    QFigure.image_file AS q_image_file,
                    AFigure.image_file AS a_image_file
                FROM Flashcards
                LEFT JOIN Figure AS QFigure ON Flashcards.qid = QFigure.fid
                LEFT JOIN Figure AS AFigure ON Flashcards.aid = AFigure.fid
                WHERE Flashcards.cid = ?
                """, (key,))
            
            qid, aid, q_image_file, a_image_file = c.fetchone()

            LOGGER.info(f"DELETE FROM Flashcards WHERE cid = {key}")
            c.execute("DELETE FROM Flashcards WHERE cid = ?", (key,))
            conn.commit()

            # Delete question figure from database
            if qid:
                delete_figure(qid)
                utils.remove_image(q_image_file)  

            # Delete answer figure from database
            if aid:
                delete_figure(aid)
                utils.remove_image(a_image_file)

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