from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import hashlib


class Vote:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def generateVote(self, electionKey, voterKey, candidateKey):
        composedKey = electionKey+voterKey+candidateKey
        padded = pad(composedKey, AES.block_size, style='pkcs7')
        hashKey = hashlib.sha256(padded.encode()).hexdigest()[0:32]
        cypher = AES.new(hashKey.rjust(32), AES.MODE_ECB)
        encoded = base64.b64encode(cypher.encrypt(padded.rjust(32)))
        i = 32
        pointer = -1
        while(i > 0):
            self.generateDataBlock(hashKey[i-8:i], pointer)
            pointer = self.searchDataBlock(hashKey[i-8:i])
            i -= 8
        finalPointer = self.searchDataBlock(hashKey[0:8])
        insert = (
            "INSERT INTO vote(_data_block_pointer, _encrypted_info) VALUES(%s, %s)"
        )
        self.cursor.execute(insert, (finalPointer, encoded,))
        self.connection.commit()
        return 'OK'

    def generateDataBlock(self, block, pointer):
        insert = ("INSERT INTO data_block(_hash, _pointer) VALUES(%s, %s)")
        self.cursor.execute(insert, (block, pointer,))
        self.connection.commit()

    def retrieveDataBlock(self, pointer):
        search = ("SELECT _hash, _pointer FROM data_block WHERE _id = %s")
        self.cursor.execute(search, (pointer,))
        return self.cursor.fetchall()

    def searchDataBlock(self, block):
        search = ("SELECT _id FROM data_block WHERE _hash = %s")
        self.cursor.execute(search, (block,))
        return self.cursor.fetchone()[0]

    def retrieveVote(self, key):
        search = (
            "SELECT _data_block_pointer, _encrypted_info FROM vote WHERE _id = %s"
        )
        self.cursor.execute(search, (key,))
        tempData = self.cursor.fetchall()
        pointer = tempData[0][0]
        encoded = tempData[0][1]
        secretKey = ""
        while(pointer != -1):
            tempData = self.retrieveDataBlock(pointer)
            secretKey += tempData[0][0]
            pointer = tempData[0][1]

        cipher = AES.new(secretKey, AES.MODE_ECB)
        decoded = cipher.decrypt(base64.b64decode(encoded))
        return decoded.strip()
