import sqlite3

def create_tables():
    
    conn = sqlite3.connect('flashcards.db')     # Connection to the database
    c = conn.cursor()                           # Allows entries to the database

    # Main flashcard elements
    c.execute("""CREATE TABLE Flashcards(
              key INTEGER PRIMARY KEY AUTOINCREMENT,
              category TEXT NOT NULL,
              question TEXT NOT NULL,
              code TEXT,
              image_path TEXT,
              answer TEXT NOT NULL
    )""")

    conn.commit()                               # Commit changes to database
    conn.close()                                # Close connection to the database

if __name__ == "__main__":
    create_tables()