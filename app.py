from flask import Flask,flash, render_template, request

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

            if not username:
                error = 'Debes ingresar un usuario'
                flash(error)
                return render_template('login.html')

            if not password:
                error = 'Debes ingresar una contraseña'
                flash(error)
                return render_template('login.html')

            #user = db.execute('SELECT * FROM usuario WHERE usuario= ? AND contraseña= ?', (username, password)).fetchone()
            user=None
            if user is None:
                error = 'Usuario o contraseña inválidos'
                flash(error)
            else:
                return render_template('mensaje')

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

<<<<<<< HEAD
@app.route('/createproduct_usuariofinal')
def createproduct_usuariofinal():
    return render_template('createproduct_usuariofinal.html')


@app.route('/createprovider_usuariofinal')
def createprovider_usuariofinal():
    return render_template('createprovider_usuariofinal.html')

@app.route('/editareliminarproducto') #ETHEL
def editareliminarproducto():
    return render_template('editareliminarproducto.html')

#dsdsd
=======
#kevin ASDASDFKAFF


>>>>>>> 303701dd6e993f353c97f9a891657ef687d86f69
if __name__ == '__main__':
    app.run()
