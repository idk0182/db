from datetime import date


class Employee:
    def __init__(self, full_name, birth_date, gender):
        self.full_name = full_name
        self.birth_date = birth_date
        self.gender = gender

    def get_age(self):
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    def to_sql_insert(self):
        return (self.full_name, self.birth_date.strftime('%Y-%m-%d'), self.gender)

    def save_to_db(self, db, commit=True):
        query = """
        INSERT INTO employees (full_name, birth_date, gender)
        VALUES (%s, %s, %s)
        """
        db.execute_query(query, self.to_sql_insert(), commit=commit)