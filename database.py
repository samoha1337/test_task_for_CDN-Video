import sqlite3

# Функция для создания подключения к базе данных SQLite
def get_db_connection():
    conn = sqlite3.connect('cities.db')
    conn.row_factory = sqlite3.Row
    return conn

# Функция для создания таблиц в базе данных, если они еще не созданы
def create_tables():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50) NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    
# Создание таблиц при запуске скрипта
create_tables()
