
from UsuarioFinal import UsuarioFinal
from db import get_db
from db import close_db

class Administrador(UsuarioFinal):

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
    


    def buscarUsuario(self,label): 
        try:
            print(label)
            db = get_db()
            cursor=db.cursor()
            cursor.execute("SELECT Codigo, Nombre, Apellido, Celular, Email, Rol FROM Usuario WHERE"+ label )
            query=cursor.fetchall()
            #db.commit()
            close_db()
            return query
        except Exception as ex:
            print(ex)
        return       

    