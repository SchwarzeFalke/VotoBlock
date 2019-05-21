from faker import Faker
from access import Access
from vote import Vote
from voter import Voter
from candidate import Candidate

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
            "SELECT electoral_key FROM user ORDER BY electoral_key DESC LIMIT 70"
        )
        self.cursor.execute(select)
        result = self.cursor.fetchall()
        for row in result:
            create_voter = Voter(self.connection, self.cursor)
            electoral_key = row[0]
            name = fake.first_name()
            middle_name = fake.first_name()
            flastname = fake.last_name()
            mlastname = fake.last_name()
            address = fake.simple_profile(sex=None)['address']
            birth_date = fake.simple_profile(sex=None)['birthdate']
            create_voter.create(electoral_key, name, middle_name,
                                flastname, mlastname, address, birth_date)
        return("OK")

    def fake_candidate(self):
        fake = Faker('es_MX')
        select = (
            "SELECT electoral_key FROM user WHERE electoral_key NOT IN (SELECT electoral_key FROM voter) LIMIT 5"
        )
        self.cursor.execute(select)
        candidates = self.cursor.fetchall()

        select = (
            "SELECT _id FROM party"
        )
        self.cursor.execute(select)
        parties = self.cursor.fetchall()
        i = 0
        for row in candidates:
            create_candidate = Candidate(self.connection, self.cursor)
            electoral_key = row[0]
            party = parties[i][0]
            name = fake.first_name()
            middle_name = fake.first_name()
            flastname = fake.last_name()
            mlastname = fake.last_name()

            create_candidate.create(electoral_key, name, middle_name,
                                    flastname, mlastname, party)
            i += 1

        return('Ok')
