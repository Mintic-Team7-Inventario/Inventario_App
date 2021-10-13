from flask import Flask,flash, render_template, request

import os

import utils
import os


app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(12)
<<<<<<< HEAD
=======

>>>>>>> fd77033d0aec5b05e1c1e902736291447adbf6f7
#dds
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

<<<<<<< HEAD
            #db = get_db()
            error = None
     
=======
>>>>>>> fd77033d0aec5b05e1c1e902736291447adbf6f7
            if not username:
                error = 'Debes ingresar un usuario'
                print('aqui')
                flash(error)
                return render_template('login.html')

            if not password:
                error = 'Debes ingresar una contraseña'
                flash(error)
                return render_template('login.html')
            return render_template('buscarProducto.html')
        return render_template('login.html')
    except Exception as ex:
        print(ex)
        return render_template('login.html')


@app.route('/createuser')
def createuser():
    return render_template('createuser.html')


@app.route('/createproduct')
def createproduct():
    return render_template('createproduct.html')


@app.route('/createprovider')
def createprovider():
    return render_template('createprovider.html')


@app.route('/createproduct_usuariofinal')
def createproduct_usuariofinal():
    return render_template('createproduct_usuariofinal.html')


@app.route('/createprovider_usuariofinal')
def createprovider_usuariofinal():
    return render_template('createprovider_usuariofinal.html')

@app.route('/editareliminarproducto') #ETHEL
def editareliminarproducto():
    return render_template('editareliminarproducto.html')


@app.route('/editareliminarproveedor') #ETHEL
def editareliminarproveedor():
    return render_template('editareliminarproveedor.html')

@app.route('/buscarProducto')
def buscarProducto():
    return render_template('buscarProducto.html')

@app.route('/buscarProvider')
def buscarProvider():
    return render_template('buscarProvider.html')

@app.route('/editareliminarusuario') #ETHEL
def editareliminarusuario():
    return render_template('editareliminarusuario.html')

@app.route('/buscarProductoUsuarioFinal')
def buscarProductoUsuarioFinal():
    return render_template('buscarProductoUsuarioFinal.html')

@app.route('/PaginaProveedor')
def PaginaProveedor():
    return render_template('PaginaProveedor.html')



if __name__ == '__main__':
    app.run()
