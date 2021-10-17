
from db import get_db

class Usuario:

    def __init__(self,codigo,name, apellido, contraseña, celular,email,rol):
        super(name, codigo)
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
    


    def editarconsultarUser(self,label,valor): 
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Usuario WHERE "+ label +" = ?", (str(valor).strip())).fetchone()
        query = cursor.fetchall()
        cursor.close_db()
        return query
