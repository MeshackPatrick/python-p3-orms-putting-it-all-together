import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    def __init__(self, name, breed, id=None):
        self.id = id
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs
                (id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        if self.id is None:
            sql = """
                INSERT INTO dogs (name, breed)
                VALUES (?, ?)
            """
            CURSOR.execute(sql, (self.name, self.breed))
            CONN.commit()
            self.id = CURSOR.lastrowid
        else:
            # Update existing row
            sql = """
                UPDATE dogs
                SET name = ?,
                    breed = ?
                WHERE id = ?
            """
            CURSOR.execute(sql, (self.name, self.breed, self.id))
            CONN.commit()

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        return cls(
            name=row[1],
            breed=row[2],
            id=row[0]
        )

    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM dogs
        """
        CURSOR.execute(sql)
        return [cls.new_from_db(row) for row in CURSOR.fetchall()]

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * FROM dogs
            WHERE name = ?
            LIMIT 1
        """
        CURSOR.execute(sql, (name,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        return None

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM dogs
            WHERE id = ?
            LIMIT 1
        """
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        return None

    @classmethod
    def find_or_create_by(cls, name, breed):
        found_dog = cls.find_by_name(name)
        if found_dog:
            return found_dog
        else:
            return cls.create(name, breed)

    def update(self):
        self.save()  # Calls save to update the row in the database

if __name__ == '__main__':
    Dog.create_table()  # Create the table if not exists
    CONN.close()  # Close the connection when the script is run