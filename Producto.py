
from UsuarioFinal import UsuarioFinal
from db import get_db
from db import close_db

class Producto:
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
    
    def eliminarproductos(self):
        try:
            db = get_db()
            cursor=db.cursor()
            value=[]
            for dato in self.eliminar:
                value.append((dato,))
            cursor.executemany("""DELETE FROM Producto WHERE CodigoProducto = ?""", value)
            db.commit()
            close_db()
        except Exception as ex:
            print(ex)
        return 


    
    def buscarProducto(self,label): 
        try:
            print(label)
            db = get_db()
            cursor=db.cursor()
            cursor.execute("SELECT * FROM Producto WHERE"+ label )
            query=cursor.fetchall()
            #db.commit()
            close_db()
            return query
        except Exception as ex:
            print(ex)
        return 
                        
    def crearProducto(self,name,codigoProveedor,marca, estado, inventario,codigoProducto,precio,cantidadMinima,descripcion):
        try:
            db = get_db()
            db.execute("INSERT INTO Producto(NombreProducto, CodigoProveedor,Marca, Estado, Inventario,CodigoProducto,Precio, CantidadMinima, Descripcion) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (name,codigoProveedor,marca, estado, inventario,codigoProducto,precio,cantidadMinima,descripcion)).fetchone()
            db.commit()
            close_db()
        except Exception as ex:
            print(ex)
        return 
    
    def editarconsultarProducto(self,label,valor): 
        try:
            db = get_db()
            value=[]
            if type(valor)==str:
                value=(valor,)
                query=db.execute("SELECT * FROM Producto WHERE "+ label +" = ?", value).fetchall()
            else:
                query=[]
                for dato in valor:
                    query.append(db.execute("SELECT * FROM Producto WHERE "+ label +" = ?", (dato,)).fetchall()[0])
            close_db()
            return query
        except Exception as ex:
            print(ex)
        return
    
    def consultartodosProducto(self,valor): 
        try:
            db = get_db()
            query=db.execute("SELECT * FROM Producto WHERE CodigoProducto = ?", (valor,)).fetchall()
            close_db()
            return query
        except Exception as ex:
            print(ex)
        return 