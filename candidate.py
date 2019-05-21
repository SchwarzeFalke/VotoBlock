import hashlib


class Candidate:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def create(self, electoral_key, election_id, name, middle_name, flastname, mlastname, party):
        status = 'C'
        insert = (
            "INSERT INTO candidate(electoral_key, election_id,name, middle_name, flastname, mlastname, party_id, status) VALUES(%s, %s, %s, %s, %s, %s, %s)"
        )

        self.cursor.execute(insert, (electoral_key, name, middle_name,
                                     flastname, mlastname, party, status))
        self.connection.commit()
