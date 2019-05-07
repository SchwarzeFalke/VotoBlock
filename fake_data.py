import mysql.connector
import os

from dotenv import load_dotenv
from faker import Faker

fake = Faker('es_MX')
load_dotenv()  # Load .env file with the env variables

connection = mysql.connector.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"),
                                     host=os.getenv("DB_HOST"),
                                     database=os.getenv("DB_NAME"))
cursor = connection.cursor()

id = 0
for _ in range(2000):
    voter = fake.profile(fields=None, sex=None)

    fake_user = (
        "INSERT INTO user(electoral_key, password, email, privilages, exist) VALUES(%s, %s, %s, %s, %s)"
    )
    fake_voter = (
        "INSERT INTO voter(electoral_key, name, middle_name, flastname, mlastname, address, birth_date) VALUES(%s, %s, %s, %s, %s, %s, %s)"
    )

    cursor.execute(fake_user, (id, fake.password(length=20, special_chars=True, digits=True, upper_case=True, lower_case=True),
                               voter['mail'], 'U', 1))
    connection.commit()

    cursor.execute(fake_voter, (id, fake.first_name(),
                                fake.first_name(), fake.last_name(), fake.last_name(), voter['address'], voter['birthdate']))
    connection.commit()
    id += 1
