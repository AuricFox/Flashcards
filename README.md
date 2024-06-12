# Flashcards

Flashcards is a program designed to assist with memorizing terms for tests or interviews. The application utilizes Python for the server-side functionality and HTML/CSS/JavaScript for the client-side user interface.

![Home Page](home_page.jpg "Home Page")

## Features

- **Flashcards for Interview Preparation**: Create and review flashcards tailored for job interviews, covering a wide range of topics from technical questions to behavioral inquiries.

- **Knowledge Refresh**: Use the flashcards to reinforce and refresh your memory, ensuring you are well-prepared for tests or exams. The flashcards can be used for topics such as math, chemistry, biology, etc.

- **Server-Side**: The server-side of Flashcards is powered by Flask, providing a lightweight and efficient web framework. SQLAlchemy is used to manage the database containing the flashcards and user data.

- **Client-Side**: The client-side interface is built using a combination of HTML, CSS, and JavaScript, offering a seamless and interactive user experience.

## Getting Started

To get started with Flashcards, follow these steps:

1. **Clone the Repository:**
    ```
    git clone https://github.com/AuricFox/Flashcards.git
    ```

2. **Navigate to the Project Directory:**
    ```
    cd Flashcards
    ```

3. **Setup Environment:**
    ```
    pip install virtualenv  
    virtualenv env

    .\env\Scripts\activate      # Windows
    source env/bin/activate     # Mac OS
    ```

4. **Install Dependencies:**
    ```
    pip install Flask FLask-WTF Flask-SQLAlchemy Flask-Testing python-dotenv
    ```

5. **Run Server:**
    ```
    python wsgi.py
    ```

    The server will start running, and you can access the application by navigating to `http://localhost:5000` in your web browser.

## Database

### Creating Tables

The tables have not yet been added to the database and need to be created. Execute the following command from the base directory in the command-line:
```
python commands.py create_database
```

If the database needs to be re-initialized, then enter the following script into the command-line from the base directory:
```
python commands.py clear_database
```

Creating and clearing the database can also be accomplished in the flash shell. This is done by following these steps:

1. Open the Flask shell to create a table:  
```
flask shell
```

2. Run the folling code to create the table:  
```
from app.extensions import db
from app.models.flashcard_model import FlashcardModel, FigureModel
db.create_all()
```

3. To Update or Delete tables:
```
db.drop_all()
db.create_all()
```

4. Run the following code to exit:  
```
exit()
```

### Figure Table

Stores blocks of code, the coding language, or the filename of the image for figures related to any flashcards. Currently, users can 
only store one type (image or code/type) to prevent the flashcard from getting cluttered.

|**id**|code_example |code_type |image_example |
|:----:|:-----------:|:--------:|:------------:|

- **id (INTEGER)**: An autoincremented primary key.
- **code_example (TEXT)**: A block or snippet of code.
- **code_type (TEXT)**: The language that the code block is written in.
- **image_example (TEXT)**: A filename, not path, of the stored image.

### Flashcards Table

Stores the flashcard infomation and related figure id's for referencing. Users can create flashcards without a question or answer as long 
as there is an associated figure id attached, otherwise the card will not be saved.

|**id**|category |question |anwser |q_figure |a_figure |
|:----:|:-------:|:-------:|:-----:|:-------:|:-------:|

- **cid (INTEGER)**: An autoincremented primary key.
- **category (TEXT, Not Null)**: The subject or topic of the question.
- **question (TEXT)**: The query being asked.
- **answer (TEXT)**: The expected response to the question.
- **q_figure (INTEGER)**: A foreign key referencing the Figure table for any figures related to the question.
- **a_figure (INTEGER)**: A foreign key referencing the Figure table for any figures related to the answer.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) - see the [LICENSE](LICENSE) file for details.
