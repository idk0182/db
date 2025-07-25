from db_connector import DBConnection
from employee import Employee
from filler import generate_random_employees, generate_custom_employees
from utils import measure_time
import time
from datetime import datetime
from mysql.connector import Error
from faker import Faker


fake = Faker("ru_RU")


def create_table(db):
    query = """
    CREATE TABLE IF NOT EXISTS employees (
        id INT AUTO_INCREMENT PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        birth_date DATE NOT NULL,
        gender ENUM('M', 'F') NOT NULL
    )
    """
    db.execute_query(query)
    print("Таблица создана или уже существует.")


def add_employee(db):
    full_name = input("ФИО: ")
    birth_date_str = input("Дата рождения (YYYY-MM-DD): ")
    gender = input("Пол (M/F): ").upper()

    try:
        birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Неверный формат даты.")
        return

    emp = Employee(full_name, birth_date, gender)
    emp.save_to_db(db, commit=False)
    print("Сотрудник добавлен.")


def show_employees(db):
    query = "SELECT * FROM employees ORDER BY full_name"
    results = db.fetch_all(query)
    for row in results:
        age = Employee(row['full_name'], row['birth_date'], row['gender']).get_age()
        print(f"{row['full_name']} | {row['birth_date']} | {row['gender']} | {age} лет")


def execute_query(self, query, params=None, commit=True):
    cursor = self.connection.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        if commit:
            self.connection.commit()
    except Error as e:
        print(f"Ошибка выполнения запроса: {e}")
        self.connection.rollback()
    finally:
        cursor.close()

def save_to_db(self, db, commit=True):
    query = """
    INSERT INTO employees (full_name, birth_date, gender)
    VALUES (%s, %s, %s)
    """
    db.execute_query(query, self.to_sql_insert(), commit=commit)


def auto_fill(db):
    count = int(input("Сколько строк автоматически заполнить? "))
    gender = input(f"Пол для {count} записей (M/F): ").upper()
    surname_letter = input(f"Начальная буква фамилии для {count} записей: ").upper()

    if gender == '':
        bulk_data = generate_random_employees(count)
        all_data = bulk_data
    else:
        custom_data = generate_custom_employees(gender, surname_letter, count)
        all_data = custom_data

    conn = db.connection
    try:
        if not conn.in_transaction:
            conn.start_transaction()
        for emp in all_data:
            emp.save_to_db(db, commit=False)
        conn.commit()
        print(f"Добавлено {len(all_data)} записей.")
    except Exception as e:
        conn.rollback()
        print("Ошибка при добавлении записей:", e)


def search_employees(db):
    gender = input("Пол (M/F) [оставьте пустым для всех]: ").upper() or ""
    surname_letter = input("Начальная буква фамилии: ").upper() or ""

    start_time = time.time()

    query = "SELECT * FROM employees WHERE 1=1"
    params = []

    if gender:
        query += " AND gender = %s"
        params.append(gender)
    if surname_letter:
        query += " AND full_name LIKE %s"
        params.append(f"{surname_letter}%")

    results = db.fetch_all(query, tuple(params))
    end_time = time.time()

    for row in results:
        age = Employee(row['full_name'], row['birth_date'], row['gender']).get_age()
        print(f"{row['full_name']} | {row['birth_date']} | {row['gender']} | {age} лет")

    print(f"Время выполнения: {end_time - start_time:.4f} секунд")


def optimize_and_test_search(db):
    print("Измеряем время без индексов:")
    search_employees(db)
    print("Создаём индексы (если их ещё нет):")
    
    db.execute_query("CREATE INDEX idx_gender ON employees(gender)")

    db.execute_query("CREATE INDEX idx_full_name ON employees(full_name)")

    print("\n Измеряем время после создания индексов:")
    search_employees(db)
    print("Оптимизация завершена. Рекомендуется использовать индексы для ускорения поиска.")


def clear_employees_table(db, batch_size=1000):
    confirm = input("Вы уверены, что хотите удалить все записи из таблицы сотрудников? (да/нет): ").strip().lower()
    if confirm != 'да':
        print("Операция отменена.")
        return

    print("Начинается пошаговая очистка таблицы...")
    total_deleted = 0
    while True:
        fetch_query = f"SELECT id FROM employees ORDER BY id ASC LIMIT {batch_size}"
        ids_to_delete = db.fetch_all(fetch_query)

        if not ids_to_delete:
            break

        id_list = [row['id'] for row in ids_to_delete]
        
        ids_placeholder = ','.join(['%s'] * len(id_list))

        delete_query = f"DELETE FROM employees WHERE id IN ({ids_placeholder})"
        
        db.execute_query(delete_query, tuple(id_list))
        
        deleted_in_batch = len(id_list)
        total_deleted += deleted_in_batch
        print(f"Удалено {deleted_in_batch} записей. Всего удалено: {total_deleted}")


    print(f"Очистка завершена. Всего удалено {total_deleted} записей.")




def menu():
    db = DBConnection(database="employees_db")
    while True:
        print("\n=== Меню ===")
        print("1. Создать таблицу")
        print("2. Добавить сотрудника")
        print("3. Показать всех сотрудников")
        print("4. Автозаполнить данные")
        print("5. Поиск по параметрам")
        print("6. Оптимизация и тестирование")
        print("7. Очистка БД(вне ТЗ, дополнительная функция)")
        print("8. Выход")

        choice = input("Выбор: ")

        if choice == "1":
            create_table(db)
        elif choice == "2":
            add_employee(db)
        elif choice == "3":
            show_employees(db)
        elif choice == "4":
            auto_fill(db)
        elif choice == "5":
            search_employees(db)
        elif choice == "6":
            optimize_and_test_search(db)
        elif choice == "7":
            clear_employees_table(db)
        elif choice == "8":
            db.close()
            break
        else:
            print("Неверный выбор.")

if __name__ == "__main__":
    menu()