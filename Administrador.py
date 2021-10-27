
from UsuarioFinal import UsuarioFinal
from db import get_db
from db import close_db

class Administrador(UsuarioFinal):

    def __init__(self,codigo,name, apellido, contraseña, celular,email,rol):
        super().__init__(codigo,name, apellido, contraseña, celular,email,rol)


    def buscarUsuario(self,label,value): 
        try:
            
            db = get_db()
            cursor=db.cursor()
            val=()
            for valores in value:
                val= val+(valores,)
            cursor.execute("SELECT  Codigo, Nombre, Apellido, Celular, Email, Rol FROM Usuario WHERE"+ label,val )
            query=cursor.fetchall()
            #db.commit()
            close_db()
            return query
        except Exception as ex:
            print(ex)
        return       

       

    