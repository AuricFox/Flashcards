import sqlite3

def create_tables():
    
    conn = sqlite3.connect('flashcards.db')     # Connection to the database
    c = conn.cursor()                           # Allows entries to the database

    # Code elements for supporting the flashcard
    c.execute("""CREATE TABLE Code(
            cid INTEGER PRIMARY KEY AUTOINCREMENT,
            code_block TEXT NOT NULL,
            code_type TEXT NOT NULL
    )""")

    # Main flashcard elements
    c.execute("""CREATE TABLE Flashcards(
            fid INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            code_id INTEGER REFERENCES Code(ckey),
            image_file TEXT
              
    )""")

    conn.commit()                               # Commit changes to database
    conn.close()                                # Close connection to the database

if __name__ == "__main__":
    create_tables()