class Credenciales:
    def __init__(self,tipousuario):
        self.usuarios=["Usuariofinal","Administrador","Superadministrador"]
        if tipousuario in self.usuarios:
            self.tipousuario=tipousuario
        else:
            print("Credenciale no existe")
    
    @property
    def tipousuario(self):
        return self.tipousuario
    
    @tipousuario.setter
    def tipousuario(self,tipousuario):
        if tipousuario in self.usuarios:
            self.tipousuario=tipousuario
        else:
            print("Credenciale no existe")

    
        