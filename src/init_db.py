import sqlite3

def create_tables():
    
    conn = sqlite3.connect('flashcards.db')     # Connection to the database
    c = conn.cursor()                           # Allows entries to the database

    # Main flashcard elements
    c.execute("""CREATE TABLE Flashcards(
              category TEXT NOT NULL,
              question TEXT NOT NULL,
              code TEXT.
              image_path TEXT,
              answer TEXT NOT NULL
    )""")

    # Track the number of questions in each category
    c.execute("""CREATE TABLE Category(
              category TEXT NOT NULL,
              count INTEGER
    )""")

    conn.commit()                               # Commit changes to database
    conn.close()                                # Close connection to the database