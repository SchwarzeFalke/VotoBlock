import hashlib


class Voter:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def create(self, electoral_key, name, middle_name, flastname, mlastname, address, birth_date):
        insert = (
            "INSERT INTO voter(electoral_key, name, middle_name, flastname, mlastname, address, birth_date) VALUES(%s, %s, %s, %s, %s, %s, %s)"
        )

        self.cursor.execute(insert, (electoral_key, name, middle_name,
                                     flastname, mlastname, address, birth_date))
        self.connection.commit()
        self.connection.close()
