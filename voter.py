import hashlib


class Voter:
    def __init__(self, connection, cursor):
        self.c = connection
        self.cur = cursor

    def create(self, nombre, contra, tipo):
        insert = (
            "INSERT INTO usuario(username, password, id_tipo) VALUES(%s, %s, %s)")
        h = hashlib.new('sha1', bytes(contra, 'utf-8'))
        contra = h.hexdigest()
        self.cur.execute(insertar, (nombre, contra, tipo))
        self.c.commit()

    def search(self, nombre):
        _buscar = ("SELECT * FROM usuario WHERE username =  %s")
        self.cur.execute(_buscar, (nombre,))
        resultados = self.cur.fetchall()

        return resultados

    def modificar(self):
        pass

    def login(self, u, p):
        pass_hash = hashlib.new('sha1', bytes(p, 'utf-8'))
        pass_hash = pass_hash.hexdigest()

        select = ("SELECT * FROM usuario WHERE username = %s AND password = %s")

        self.cur.execute(select, (u, pass_hash))
        resultado = self.cur.fetchall()

        if resultado:
            return True
        else:
            return False
