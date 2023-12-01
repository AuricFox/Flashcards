import sqlite3

# Connection to the database
CONN = sqlite3.connect('flashcards.db')

# Allows commands to the database
C = CONN.cursor()

C.execute("""CREATE TABLE flashcards (
          question TEXT,
          code TEXT.
          image_path TEXT,
          answer TEXT
)""")    