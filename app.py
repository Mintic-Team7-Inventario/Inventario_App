#<<<<<<< HEAD
from flask import Flask, render_template, request, flash

import utils
import os
#=======
from flask import Flask,flash, render_template, request

import os
import utils
import os

#>>>>>>> 990da5f7db7583c04b29c597c1335b314184a079

app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(12)


# dds
@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    try:
        print('aqui')
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            if not username:
                error = 'Debes ingresar un usuario'
                
                flash(error)
                return render_template('login.html')

            if not password:
                error = 'Debes ingresar una contraseña'
                flash(error)
                return render_template('login.html')
            
            return render_template('buscarProducto.html')

        return render_template('login.html')
       
    except Exception as ex:
        print("ex")
        print(ex)
        return render_template('login.html')


@app.route('/createuser', methods=('GET', 'POST'))
def createuser():
    try:
        if request.method == 'POST':
            username = request.form['username']
            nombre = request.form['nombre']
            email = request.form['email']
            password = request.form['password']
            apellido = request.form['apellido']
            phone = request.form['phone']
            confirmpassword = request.form['confirmpassword']

            if not utils.isUsernameValid(username):
                error = "El usuario no es valido"
                flash(error)
                return render_template('createuser.html')

            if not utils.isUserValid(nombre):
                error = "El nombre no es valido"
                flash(error)
                return render_template('createuser.html')

            if not utils.isUserValid(apellido):
                error = "El apellido no es valido"
                flash(error)
                return render_template('createuser.html')

            if not utils.isEmailValid(email):
                error = "El email no es valido"
                flash(error)
                return render_template('createuser.html')

            if not utils.isPhoneValid(phone):
                error = "El celular no es valido"
                flash(error)
                return render_template('createuser.html')

            if not utils.isPasswordValid(password):
                error = "El password no es valido"
                flash(error)
                return render_template('createuser.html')

            if not utils.isPasswordValid(confirmpassword):
                error = "El password no es valido"
                flash(error)
                return render_template('createuser.html')

        return render_template('createuser.html')
    except Exception as e:
        return render_template('createuser.html')


@app.route('/createproduct', methods=('GET', 'POST'))
def createproduct():
    try:
        if request.method == 'POST':
            nameproduct = request.form['nameproduct']
            codprovider = request.form['codprovider']
            brand = request.form['brand']
            state = request.form['state']
            inventory = request.form['inventory']
            codproduct = request.form['codproduct']
            price = request.form['price']
            amountmin = request.form['amountmin']
            description = request.form['description']

            if not utils.isTextValid(nameproduct):
                error = "El nombre de producto no es valido"
                flash(error)
                return render_template('createproduct.html')

            if not utils.isNumberValid(codprovider):
                error = "El codigo de proveedor no es valido"
                flash(error)
                return render_template('createproduct.html')

            if not utils.isTextValid(brand):
                error = "La marca no es valida"
                flash(error)
                return render_template('createproduct.html')

            if not utils.isTextValid(state):
                error = "El estado no es valido"
                flash(error)
                return render_template('createproduct.html')

            if not utils.isTextValid(inventory):
                error = "El inventario no es valido"
                flash(error)
                return render_template('createproduct.html')

            if not utils.isNumberValid(codproduct):
                error = "El codigo de producto no es valido"
                flash(error)
                return render_template('createproduct.html')

            if not utils.isNumberValid(price):
                error = "El precio no es valido"
                flash(error)
                return render_template('createproduct.html')

            if not utils.isNumberValid(amountmin):
                error = "La cantidad minima no es valida"
                flash(error)
                return render_template('createproduct.html')

            if not utils.isTextValid(description):
                error = "La descripción no es valida"
                flash(error)
                return render_template('createproduct.html')

        return render_template('createproduct.html')
    except Exception as e:
        return render_template('createproduct.html')


@app.route('/createprovider', methods=('GET', 'POST'))
def createprovider():
    try:
        if request.method == 'POST':
            company = request.form['company']
            codcompany = request.form['codcompany']
            correo = request.form['correo']
            city = request.form['city']
            address = request.form['address']
            phone = request.form['phone']
            state = request.form['state']

            if not utils.isUserValid(company):
                error = "El nombre de compañia no es valido"
                flash(error)
                return render_template('createprovider.html')

            if not utils.isNumberValid(codcompany):
                error = "El codigo de compañia no es valido"
                flash(error)
                return render_template('createprovider.html')

            if not utils.isEmailValid(correo):
                error = "El correo no es valido"
                flash(error)
                return render_template('createprovider.html')

            if not utils.isTextValid(city):
                error = "La ciudad no es valida"
                flash(error)
                return render_template('createprovider.html')

            if not utils.isAddressValid(address):
                error = "La dirección no es valida"
                flash(error)
                return render_template('createprovider.html')

            if not utils.isPhoneValid(phone):
                error = "El celular no es valido"
                flash(error)
                return render_template('createprovider.html')

            if not utils.isTextValid(state):
                error = "El estado no es valido"
                flash(error)
                return render_template('createprovider.html')

        return render_template('createprovider.html')
    except Exception as e:
        return render_template('createprovider.html')


@app.route('/createproduct_usuariofinal')
def createproduct_usuariofinal():
    return render_template('createproduct_usuariofinal.html')


@app.route('/createprovider_usuariofinal')
def createprovider_usuariofinal():
    return render_template('createprovider_usuariofinal.html')


@app.route('/editareliminarproducto')  # ETHEL
def editareliminarproducto():
    return render_template('editareliminarproducto.html')


@app.route('/editareliminarproveedor')  # ETHEL
def editareliminarproveedor():
    return render_template('editareliminarproveedor.html')


@app.route('/buscarProducto')
def buscarProducto():
    return render_template('buscarProducto.html')


@app.route('/buscarProvider')
def buscarProvider():
    return render_template('buscarProvider.html')


@app.route('/editareliminarusuario')  # ETHEL
def editareliminarusuario():
    return render_template('editareliminarusuario.html')


@app.route('/buscarProductoUsuarioFinal')
def buscarProductoUsuarioFinal():
    return render_template('buscarProductoUsuarioFinal.html')


@app.route('/PaginaProveedor')
def PaginaProveedor():
    return render_template('PaginaProveedor.html')

@app.route('/buscarusuario')
def buscarusuario():
    return render_template('buscarusuario.html')

@app.route('/PaginaProducto')
def PaginaProducto():
    return render_template('PaginaProducto.html')

if __name__ == '__main__':
    app.run()
