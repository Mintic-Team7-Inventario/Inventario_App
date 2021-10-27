
from Administrador import Administrador
from db import get_db
from db import close_db
from werkzeug.security import generate_password_hash, check_password_hash

class Superadministrador(Administrador):

    def __init__(self,codigo,name, apellido, contraseña, celular,email,rol):
        super().__init__(codigo,name, apellido, contraseña, celular,email,rol)



    def editarconsultarUser(self,label,valor): 
        try:
            print(label)
            db = get_db()
            value=[]
            if type(valor)==str:
                value=(valor,)
                query=db.execute("SELECT Codigo, Nombre, Apellido, Celular, Email, Rol FROM Usuario WHERE "+ label +" = ?", value).fetchall()
            else:
                query=[]
                for dato in valor:
                    query.append(db.execute("SELECT Codigo, Nombre, Apellido, Celular, Email, Rol FROM Usuario WHERE "+ label +" = ?", (dato,)).fetchall()[0])
            close_db()
            print(query)
            return query
        except Exception as ex:
            print(ex)
        return 

    
                        
    def crearUsuario(self,codigo,name,nombreusuario, apellido, contrasena, celular,email,rol):
        try:
            db = get_db()
            db.execute("INSERT INTO Usuario(Codigo, Nombre,Apellido, Contrasena, Celular,Email,Rol,NombreUsuario) VALUES (?, ?, ?, ?, ?, ?, ?,?)", (codigo,name, apellido, generate_password_hash(contrasena), celular,email,rol,nombreusuario)).fetchone()
            db.commit()
            close_db()
        except Exception as ex:
            print(ex)
        return 
    
    def actualizarusuario(self,codigo,column,valor):
        try:
            db = get_db()
            print(codigo)
            print(column)
            print(valor)
            db.execute("UPDATE Usuario SET "+ column +" = ? WHERE Codigo = ?",
                           (valor, codigo)).fetchone()
            db.commit()
            close_db()
        except Exception as ex:
            print(ex)
        return 
        
