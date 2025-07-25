import mysql.connector
from mysql.connector import Error


class DBConnection:
    def __init__(self, host=input('Введите host'), user=input('Логин:'), password=input('Пароль:'), database=input('Название БД: ')):
        self.connection = None
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            print("Подключение к базе данных установлено.")
        except Error as e:
            print(f"Ошибка подключения: {e}")

    def execute_query(self, query, params=None, commit=True):
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            if commit:
                self.connection.commit()
            self.connection.commit()
        except Error as e:
            print(f"Ошибка выполнения запроса: {e}")
            self.connection.rollback()
        finally:
            cursor.close()

    def fetch_all(self, query, params=None):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
        except Error as e:
            print(f"Ошибка выборки: {e}")
        finally:
            cursor.close()
        return result

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Соединение закрыто.")