# запрос по созданию базы данных
import sqlite3

def initiate_db():
    connection = sqlite3.connect('Products.db')
    cursor = connection.cursor()  # объект, который взаимодействует с базой данных

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    price INTEGER NOT NULL
    )
    ''')




    for i in range(1, 5):           # заполнение таблицы
        cursor.execute(" INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                       (f"Продукт {i}", f"Описание {i}", f"{i * 100}"))
    connection.commit()
    connection.close()  # закрытие подключения


def get_all_products():                     # возвращает все записи из таблицы Products, полученные при помощи SQL запроса
    connection = sqlite3.connect("Products.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    product = cursor.fetchall()
    connection.commit() # после отработки к connection производим commit для сохранения состояния
    connection.close()  # закрытие подключения
    return product




