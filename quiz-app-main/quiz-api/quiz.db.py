import sqlite3

def create_database():
    conn = sqlite3.connect('quiz.db')
    conn.close()

if __name__ == '__main__':
    create_database()


