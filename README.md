# Interview Cards

Interview Cards is a flashcard program designed to assist in preparing for job interviews or refreshing general knowledge. The application utilizes Python for the server-side functionality and HTML/CSS/JavaScript for the client-side user interface.

## Features

- **Flashcards for Interview Preparation**: Create and review flashcards tailored for job interviews, covering a wide range of topics from technical questions to behavioral inquiries.

- **Knowledge Refresh**: Use the flashcards to reinforce and refresh your programming knowledge, ensuring you are well-prepared for technical discussions during interviews. The flashcards can also be used for general knowledge or topics not related to software such as math, chemistry, or 
biology.

- **Server-Side**: The server-side of Interview Cards is powered by Flask, providing a lightweight and efficient web framework. SQLite3 is used as the database to manage flashcards and user data.

- **Client-Side**: The client-side interface is built using a combination of HTML, CSS, and JavaScript, offering a seamless and interactive user experience.

## Getting Started

To get started with Interview Cards, follow these steps:

1. **Clone the Repository:**
    ```
    git clone https://github.com/AuricFox/Interview_Cards.git
    ```

2. **Navigate to the Project Directory:**
    ```
    cd interview_cards
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
    (env) pip install flask
    ```

5. **Run Server:**
    ```
    (env) python app.py
    ```

    The server will start running, and you can access the application by navigating to `http://localhost:5000` in your web browser.

## Database Schema

Below is the schema of the SQLite3 database used in Interview Cards:

### Code Table

- **cid**: INTEGER (Primary Key)
- **code_block**: TEXT NOT NULL
- **code_type**: TEXT NOT NULL

### Flashcards Table

- **fid**: INTEGER (Primary Key)
- **category**: TEXT NOT NULL 
- **question**: TEXT NOT NULL
- **answer**: TEXT NOT NULL
- **code_id**: INTEGER (Foreign Key referencing Code Table)
- **image_file**: TEXT

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) - see the [LICENSE](LICENSE) file for details.