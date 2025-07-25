from employee import Employee
from datetime import date
from random import choice, randint
from faker import Faker

fake = Faker("ru_RU")


def generate_random_employees(count):
    employees = []
    genders = ['M', 'F']

    for _ in range(count):
        name = fake.name() # ФИО
        birth_year = randint(1950, 2005) # Случайная дата
        birth_date = date(birth_year, randint(1, 12), randint(1, 28))
        gender = choice(genders) # Пол
        employees.append(Employee(name, birth_date, gender))

    return employees


def generate_custom_employees(gender, letter, count):
    employees = []
    # Проверяем корректность буквы
    if not ('А' <= letter <= 'Я'):
        print(f"Внимание: буква '{letter}' не является русской заглавной. Используется стандартная буква из фамилии.")
        letter = ''

    for _ in range(count):
        first_name = fake.first_name_male() if gender == 'M' else fake.first_name_female()
        last_name = fake.last_name_male() if gender == 'M' else fake.last_name_female()

        if letter:
            last_name = letter + last_name[1:] if len(last_name) > 1 else letter

        middle_name = fake.first_name_male() + 'ович' if gender == 'M' else fake.first_name_female() + 'овна'
# Случайное имя
        name = f"{last_name} {first_name} {middle_name}"
# Случайная Дата
        birth_year = randint(1950, 2005)
        birth_date = date(birth_year, randint(1, 12), randint(1, 28))
        employees.append(Employee(name, birth_date, gender))
    return employees
