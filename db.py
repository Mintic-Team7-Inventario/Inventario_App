import sqlite3
from sqlite3 import Error
from flask import g

def get_db():
    try:
        if 'db' not in g:
            gdb = sqlite3.connect('bd.db')
        return gdb
    except Error:
        print(Error)


def close_db():
    db = g.pop('db', None)
    if db is not None:
        db.close()


#INSERT INTO Usuario(Codigo, Nombre,Apellido, Contrasena, Celular,Email,Rol)
#VALUES (2112,'Ethel', 'Garcia', 'wsw',3123,'Barranquilla','Administrador')