
from Administrador import Administrador
from db import get_db
from db import close_db
from werkzeug.security import generate_password_hash, check_password_hash

class Superadministrador(Administrador):

    def __init__(self,codigo,name, apellido, contraseña, celular,email,rol):
        super().__init__(codigo,name, apellido, contraseña, celular,email,rol)

    @property
    def name(self):
        return self.name
    
    @name.setter
    def name(self,name):
        self.name = name

    @property
    def codigo(self):
        return self.codigo
    
    @codigo.setter
    def codigo(self,codigo) :
        self.codigo= codigo
    

    def editarconsultarUser(self,label,valor): 
        try:
            print(label)
            db = get_db()
            query=db.execute("SELECT Codigo, Nombre, Apellido, Celular, Email, Rol FROM Usuario WHERE "+ label +" = ?", (valor,)).fetchall()
            close_db()
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