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

    def fake_user(self):
        insert = (
            "INSERT INTO user(electoral_key, password, email, privilages, profile_pic, exist) VALUES(%s, %s, %s, %s, %s, %s)"
        )

        fake = Faker('es_MX')
        electoral_key = fake.bban()
        privileges = 'V'
        value = None
        password = fake.password(
            length=20, special_chars=False, digits=True, upper_case=True, lower_case=True)
        hashKey = hashlib.sha256(password.encode()).hexdigest()
        mail = fake.simple_profile(sex=None)['mail']
        try:
            self.cursor.execute(
                insert, (electoral_key, hashKey, mail, privileges, value, True,))
            self.connection.commit()
            # self.connection.close()
        except self.connection.Error as err:
            print("Something went wrong: {}".format(err))

        return('Ok')

    def fake_voter(self):
        fake = Faker('es_MX')
        select = (
            "SELECT TOP 15 electoral_key FROM user ORDER BY electoral_key ASC"
        )
        self.cursor.execute(select)
        result = self.cursor.fetchall()
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
