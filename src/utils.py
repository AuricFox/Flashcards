import logging, os, re, mimetypes
from typing import List

PATH = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(
    filename=os.path.join(PATH, './output/app.log'),
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
        file_path (str): the path to the saved file
    '''

    # Replace special characters with underscores
    sanitized_name = re.sub(r'[\\/*?:"<>|]', '_', file.filename)
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
    
    original_file_path = os.path.join(path, f'{sanitized_name}{file_extension}')
    new_file_path = original_file_path
    
    counter = 1
    # loop thru the files to ensure the saved file does not have the same name as another
    while os.path.exists(new_file_path):
        new_file_path = os.path.join(path, f'{sanitized_name}_{counter}{file_extension}')
        counter += 1
    
    LOGGER.info(f"Creating file: {new_file_path}")
    file.save(new_file_path)

    return new_file_path

# ========================================================================================================================================
# Functions used for removing files
# ========================================================================================================================================
def remove_file(filename:str):
    '''
    Takes in a file object and removes the file from the temp directory

    Parameter(s):
        file (str): the input file being removed

    Output(s): None
    '''

    try:
        path = os.path.join(os.path.dirname(__file__), "../static/image")   # Path where file is saved
        file_path = os.path.join(path, filename)                            # Creating saved file path
        os.remove(file_path)                                                # File is no longer needed
        LOGGER.info(f"Successfully removed {file_path}")

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
class InvalidFile(Exception):
    pass

class FileNotFound(Exception):
    pass

class InvalidInput(Exception):
    pass