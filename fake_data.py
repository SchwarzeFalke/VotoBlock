from faker import Faker
from access import Access
from vote import Vote
from voter import Voter

import hashlib
import json
import os
import mysql.connector


class Fakerism:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def fake_users(self):
        fake = Faker('es_MX')
        create_user = Access(self.connection, self.cursor)
        electoral_key = fake.bban()
        password = fake.password(
            length=20, special_chars=False, digits=True, upper_case=True, lower_case=True)
        mail = fake.simple_profile(sex=None)['mail']
        result = create_user.register(
            str(electoral_key), str(password), str(mail))
        return(result)

    def fake_voters(self):
        fake = Faker('es_MX')
        select = (
            "SELECT TOP 15 electoral_key FROM user ORDER BY electoral_key ASC"
        )
        self.cursor.execute(select)
        result = self.cursor.fetchall()
        self.connection.close()
        for row in result:
            create_voter = Voter(self.connection, self.cursor)
            electoral_key = row["electoral_key"]
            name = fake.first_name()
            middle_name = fake.first_name()
            flastname = fake.last_name()
            mlastname = fake.last_name()
            address = fake.simple_profile(sex=None)['address']
            birth_date = fake.simple_profile(sex=None)['birthdate']
            create_voter.create(electoral_key, name, middle_name,
                                flastname, mlastname, address, birth_date)

        return("OK")
