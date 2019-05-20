import hashlib
import json


class Access:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def login(self, electoralKey, password):
        hashKey = hashlib.sha256(password.encode()).hexdigest()
        select = (
            "SELECT * FROM user WHERE electoral_key = %s AND password = %s"
        )
        result = self.cursor.execute(select, (electoralKey, hashKey,))
        items = [dict(zip([key[0] for key in self.cursor.description], row))
                 for row in result]
        return(json.dumps({'items': items}))

    def register(self, electoralKey, password, email):
        hashKey = hashlib.sha256(str(password).encode()).hexdigest()
        privileges = 'V'
        value = None
        insert = (
            "INSERT INTO user(electoral_key, password, email, privilages, profile_pic, exist) VALUES(%s, %s, %s, %s, %s, %)")
        self.cursor.execute(
            insert, (electoralKey, hashKey, email, privileges, value, True))
        self.connection.commit()
        return 'Ok'
