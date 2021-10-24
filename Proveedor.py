
from UsuarioFinal import UsuarioFinal
from db import get_db
from db import close_db

class Proveedor:
    def __init__(self):
        pass
    def __init__(self,codigo,name, apellido, contraseña, celular,email,rol):
        self.name = name
        self.codigo = codigo
        self.apellido = apellido
        self.contraseña= contraseña
        self.celular= celular
        self.email= email
        self.rol= rol
    
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
    


    def editarconsultarProveedor(self,label,valor): 
        try:
            print(label)
            db = get_db()
            query=db.execute("SELECT * FROM Proveedor WHERE "+ label +" = ?", (valor,)).fetchall()
            close_db()
            return query
        except Exception as ex:
            print(ex)
        return 
                        
    def crearProvider(self,name,codigo,email, ciudad, direccion,celular,estado,lineaproductos):
        try:
            db = get_db()
            db.execute("INSERT INTO Proveedor(Nombre, Codigo,Email, Ciudad, Direccion,Celular,Estado, LineaProductos) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (name,codigo,email, ciudad, direccion,celular, estado,lineaproductos)).fetchone()
            db.commit()
            close_db()
        except Exception as ex:
            print(ex)
        return 
    
    def buscarProveedor(self,label): 
        try:
            print(label)
            db = get_db()
            cursor=db.cursor()
            print("SELECT * FROM Producto WHERE"+ label )
            cursor.execute("SELECT Nombre, Codigo, Ciudad, LineaProductos, Estado FROM Proveedor WHERE"+ label )
            query=cursor.fetchall()
            close_db()
            return query
        except Exception as ex:
            print(ex)
        return 