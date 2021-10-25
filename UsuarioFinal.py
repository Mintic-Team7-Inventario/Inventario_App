
from db import get_db
from db import close_db
from Credenciales import Credenciales
class UsuarioFinal:
    def __init__(self):
        pass
    def __init__(self,codigo,name, apellido, contraseña, celular,email,rol):
        self.name = name
        self.codigo = codigo
        self.apellido = apellido
        self.contraseña= contraseña
        self.celular= celular
        self.email= email
        self.rol= Credenciales.__init__(rol)
        self.eliminar=None
    
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
    
    @property
    def eliminar(self):
        return self.eliminar
    
    @name.setter
    def eliminar(self,listacodigos):
        self.eliminar = listacodigos
    
    def eliminarusuario(self):
        try:
            db = get_db()
            cursor=db.cursor()
            value=[]
            for dato in self.eliminar:
                value.append((dato,))
            cursor.executemany("""DELETE FROM Usuario WHERE Codigo = ?""", value)
            db.commit()
            close_db()
        except Exception as ex:
            print(ex)
        return 


    def buscarProducto(self,label,valor): 
        try:
            db = get_db()
            query=db.execute("SELECT * FROM Producto WHERE "+ label +" = ?", (valor,)).fetchone()
            close_db()
            return query
        except Exception as ex:
            print(ex)
        return 
                        
 