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
        self.cursor.execute(select, (electoralKey, hashKey,))
        result = self.cursor.fetchall()
        # items = [dict(zip([key[0] for key in self.cursor.description], row))
        #         for row in result]
        self.connection.close()
        return(result)

    def register(self, electoralKey, password, email):
        hashKey = hashlib.sha256(password.encode()).hexdigest()
        privileges = 'V'
        value = None
        insert = (
            "INSERT INTO user(electoral_key, password, email, privilages, profile_pic, exist) VALUES(%s, %s, %s, %s, %s, %s)"
        )
        try:
            self.cursor.execute(
                insert, (electoralKey, hashKey, email, privileges, value, True,))
            self.connection.commit()
            # self.connection.close()
        except self.connection.Error as err:
            print("Something went wrong: {}".format(err))
        return 'Ok'
