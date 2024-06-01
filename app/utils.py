import logging, os, re, mimetypes
from typing import List

PATH = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(
    filename=os.path.join(PATH, '../logs/app.log'),
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s'
)

LOGGER = logging.getLogger(__name__)

# ========================================================================================================================================
# Functions used for processing files
# ========================================================================================================================================
def save_image_file(file):
    '''
    Takes in a file object, sanitizes, validates, and saves it to the temp directory

    Parameter(s):
        file: the user input file being saved

    Output(s):
        filename (str): name of the saved file
    '''
    try:
        # Replace special characters with underscores
        sanitized_name = re.sub(r'[\\/*?:"<>| ]', '_', file.filename)
        # Remove leading and trailing whitespace
        sanitized_name = sanitized_name.strip()
        # Getting the name of the file without the extension
        sanitized_name = sanitized_name.split('.')[0]

        allowed_mime_types = ['image/jpeg', 'image/png', 'application/pdf']
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.pdf']

        # Get the file's MIME type and extension
        file_mime_type, _ = mimetypes.guess_type(file.filename)
        file_extension = os.path.splitext(file.filename)[1].lower()

        # Check if the file's MIME type or extension is allowed
        if file_mime_type is not None and file_mime_type not in allowed_mime_types:
            LOGGER.error(f'{file.filename} MIME type is not supported! MIME type: {file_mime_type}')
            return None

        if file_extension not in allowed_extensions:
            LOGGER.error(f'{file.filename} extension is not supported! Extension: {file_extension}')
            return None

        path = os.path.join(PATH, "../static/images")               # Path where file will be saved
        os.makedirs(path, exist_ok=True)                            # Create path if it doesn't exist

        counter = 0
        original_file_path = os.path.join(path, f'{sanitized_name}_{counter}{file_extension}')
        new_file_path = original_file_path

        # loop thru the files to ensure the saved file does not have the same name as another
        while os.path.exists(new_file_path):
            new_file_path = os.path.join(path, f'{sanitized_name}_{counter}{file_extension}')
            counter += 1

        LOGGER.info(f"Creating file: {new_file_path}")
        file.save(new_file_path)

        return os.path.basename(new_file_path)
    
    except Exception as e:
        LOGGER.error(f"An error occured when saving {file.filename}: {e}")
        return None

# ========================================================================================================================================
def verify_file(file:str):
    '''
    Verifies input file

    Parameter(s):
        file (str): name of the provided file

    Output(s):
        True if the file is valid, else False
    '''
    try:
        # Replace special characters with underscores
        sanitized_name = re.sub(r'[\\/*?:"<>| ]', '_', file)
        # Remove leading and trailing whitespace
        sanitized_name = sanitized_name.strip()
        # Getting the name of the file without the extension
        sanitized_name = sanitized_name.split('.')[0]

        allowed_mime_types = ['application/json']
        allowed_extensions = ['.json']

        # Get the file's MIME type and extension
        file_mime_type, _ = mimetypes.guess_type(file)
        file_extension = os.path.splitext(file)[1].lower()

        # Check if the file's MIME type or extension is allowed
        if file_mime_type is not None and file_mime_type not in allowed_mime_types:
            LOGGER.error(f'{file} MIME type is not supported! MIME type: {file_mime_type}')
            return False

        if file_extension not in allowed_extensions:
            LOGGER.error(f'{file} extension is not supported! Extension: {file_extension}')
            return False
        
        return True

    except Exception as e:
        LOGGER.error(f"An error occured when validating {file}: {e}")
        return False
    
# ========================================================================================================================================
# Functions used for removing files
# ========================================================================================================================================
def remove_image(filename:str):
    '''
    Takes in an image file and removes the file from the image directory

    Parameter(s):
        file (str): the input file being removed

    Output(s): None
    '''
    try:
        # Building a path to the image directory
        path = os.path.join(os.path.dirname(__file__), "../static/images")
        # Creating full file path
        file_path = os.path.join(path, filename)
        
        # Check if the file exists before attempting to remove it
        if os.path.exists(file_path):
            os.remove(file_path)  # File is no longer needed
            LOGGER.info(f"Successfully removed {file_path}")
        else:
            LOGGER.warning(f"The file {file_path} does not exist.")

    except OSError as e:
        LOGGER.error(f'Error while removing {filename}: {str(e)}')

# ----------------------------------------------------------------------------------------------------------------------------
def remove_files(files:List[str]):
    '''
    Remove files from memory

    Parameter(s):
        files (List[str]): a list of files being removed

    Output(s): None
    '''
    for file in files:

        try:
            file_path = os.path.join(PATH, file)                # Creating saved file path
            os.remove(file_path)                                # File is no longer needed
            LOGGER.info(f"Successfully removed {file_path}")

        except OSError as e:
            LOGGER.error(f'Error while removing {file}: {str(e)}')

# ========================================================================================================================================
# Error Handling
# ========================================================================================================================================
class InvalidFile(Exception): pass
class FileNotFound(Exception): pass
class InvalidInput(Exception): pass
# ========================================================================================================================================
# Functions for processing text
# ========================================================================================================================================
def sanitize(text:str):
    '''
    Removes special characters from the string.

    Parameter(s):
        text (str): the string being sanitized

    Output(s):
        str: a sanitized string
    '''
    return re.sub(r'[\\/*?:"<>|]', '_', text)

# ========================================================================================================================================
class Cache:
    '''
    Creates a cache of data to prevent repetitive calls
    '''
    def __init__(self):
        '''
        Initializes the cache with an empty dictionary
        '''
        self.cache = {}

    # ------------------------------------------------------------
    def update(self, dict1:dict):
        '''
        Updates the current cache with new data

        Parameter(s):
            dict1 (dict): dictionary with new data

        Output(s): None
        '''
        self.cache.update(dict1)

    # ------------------------------------------------------------
    def drop(self, key:str):
        '''
        Drops a key element from the cahce
        
        Parameter(s):
            key (str): the key element in the dict being dropped

        Output(s):
            Raises a keyError if an error occurs, else None
        '''
        if key in self.cache:
            self.cache.pop(key)
        else:
            raise KeyError(f"Key '{key}' not found in cache")

    # ------------------------------------------------------------
    def clear(self):
        '''
        Resets the cache to an empty dictionary
        '''
        self.cache = {}