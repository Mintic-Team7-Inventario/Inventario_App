from flask import Flask,flash, render_template, request
import utils

app = Flask(__name__)
app.debug = True

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

            #db = get_db()
            error = None
            print(username)
            if not username:
                error = 'Debes ingresar un usuario'
                flash(error)
                return render_template('login.html')

            if not password:
                error = 'Debes ingresar una contraseña'
                flash(error)
                return render_template('login.html')

            if not utils.isUsernameValid(username):
                error = "El usuario no es valido, elija un nombre valido"
                flash(error)
                return render_template('login.html')

            if not utils.isPasswordValid(password):
                error = "El password no es valido, ingresar caracteres especiales y mayusculas"
                flash(error)
                return render_template('login.html')

            #user = db.execute('SELECT * FROM usuario WHERE usuario= ? AND contraseña= ?', (username, password)).fetchone()
            #user=None
            #if user is None:
             #   error = 'Usuario o contraseña inválidos'
              #  flash(error)
            #else:
            #    return render_template('login.html')

            #db.close_db()
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

if __name__ == '__main__':
    app.run()
