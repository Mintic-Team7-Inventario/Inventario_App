
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
        self.eliminar=None
        self.tamaño=None
        self.headers=None
        self.columns=None

    @property
    def columns(self):
        return self.columns
    
    @columns.setter
    def columns(self,columns):
        self.columns = columns
    
    
    @property
    def tamaño(self):
        return self.tamaño
    
    @tamaño.setter
    def tamaño(self,tamaño):
        self.tamaño = tamaño
    
    @property
    def headers(self):
        return self.headers
    
    @headers.setter
    def headers(self,headers):
        self.headers = headers
    
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
    
    @eliminar.setter
    def eliminar(self,listacodigos):
        self.eliminar = listacodigos
    
    def eliminarproveedor(self):
        try:
            db = get_db()
            cursor=db.cursor()
            value=[]
            for dato in self.eliminar:
                value.append((dato,))
            cursor.executemany("""DELETE FROM Proveedor WHERE Codigo = ?""", value)
            db.commit()
            close_db()
        except Exception as ex:
            print(ex)
        return 

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
    
    def buscarProveedor(self,label,value): 
        try:
            
            db = get_db()
            cursor=db.cursor()
            val=()
            for valores in value:
                val= val+(valores,)
            cursor.execute("SELECT * FROM Proveedor WHERE"+ label,val )
            query=cursor.fetchall()
            #db.commit()
            close_db()
            return query
        except Exception as ex:
            print(ex)
        return 
    
    def editarconsultarProveedor(self,label,valor): 
        try:
            db = get_db()
            value=[]
            if type(valor)==str:
                value=(valor,)
                query=db.execute("SELECT * FROM Proveedor WHERE "+ label +" = ?", value).fetchall()
            else:
                query=[]
                for dato in valor:
                    query.append(db.execute("SELECT * FROM Proveedor WHERE "+ label +" = ?", (dato,)).fetchall()[0])
            close_db()
            return query
        except Exception as ex:
            print(ex)
        return

    def datosproveedor(self, codigo):
        try:
            db = get_db()
            cursor=db.cursor()
            query=cursor.execute("SELECT Nombre, Codigo, Direccion, Ciudad, LineaProductos,Email, Estado, Celular FROM Proveedor WHERE Codigo = ?" , (codigo,)).fetchone()
            close_db()
            return query
        except Exception as ex:
            print(ex)
        return 

    def actualizarproveedor(self,codigo,column,valor):
        try:
            db = get_db()
            print(codigo)
            print(column)
            print(valor)
            db.execute("UPDATE Proveedor SET "+ column +" = ? WHERE Codigo = ?",
                           (valor, codigo)).fetchone()
            db.commit()
            close_db()
        except Exception as ex:
            print(ex)
        return 