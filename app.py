from flask import Flask, render_template, request, flash, jsonify, redirect, g, url_for, session, send_file, \
    make_response
from db import get_db
from db import close_db
import os
from werkzeug.security import generate_password_hash, check_password_hash
import functools
from Administrador import Administrador
import utils
from UsuarioFinal import UsuarioFinal
from Producto import Producto
from Proveedor import Proveedor
from Superadministrador import Superadministrador

app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(12)

@app.route('/')
def index():
    if g.user:
        if session['tipo_usuario']=="Usuariofinal":
            return redirect(url_for('buscarProductoUsuarioFinal'))
        else:
            return redirect(url_for('buscarProducto'))
    return render_template('login.html')

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        db = get_db()
        g.user = db.execute('SELECT * FROM Usuario WHERE Codigo = ?', (user_id, )).fetchone()
      

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login.html'))
        return view(**kwargs)

    return wrapped_view

@app.route('/login', methods=('GET', 'POST'))
def login():
    try:
        print('aqui')
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
    
            error=None
            if not username:
                error = 'Debes ingresar un usuario'
                
                flash(error)
                return render_template('login.html')

            if not password:
                error = 'Debes ingresar una contraseña'
                flash(error)
                return render_template('login.html')
            db = get_db()

            user = db.execute("SELECT * FROM Usuario WHERE NombreUsuario = ?", (username,)).fetchone()

            print(user)
            if user is None:
                error = 'Usuario o contraseña inválidos'
            else:
                store_password = user[3]
                result = check_password_hash(store_password, password)
                if result is False:
                    error = 'Usuario o contraseña inválidos'
                else:
                    session.clear()
                    session['user_id'] = user[0]
                    session['tipo_usuario'] = user[6]
                    if session['tipo_usuario']=="Usuariofinal":
                         resp = make_response(redirect(url_for('buscarProductoUsuarioFinal')))
                    else:
                        resp = make_response(redirect(url_for('buscarProducto')))
                    resp.set_cookie('username', username)
                    return resp
            flash(error)

        return render_template('login.html')
       
    except Exception as ex:
        print("ex")
        print(ex)
        return render_template('login.html')


@app.route('/createuser', methods=('GET', 'POST'))
def createuser():
    try:
        if request.method == 'POST':
            lista=[]
            lista_nombres=["código","nombre","nombre usuario","apellido","celular","email","contraseña","confirmar contraseña"]
            codigo = request.form['Código']
            lista.append(codigo)
            nombre = request.form['Nombre']
            lista.append(nombre)
            nombreusuario = request.form['Nombreusuario']
            lista.append(nombreusuario)
            apellido = request.form['Apellido']
            lista.append(apellido)
            celular = request.form['Celular']
            lista.append(celular)
            email = request.form['Email']
            lista.append(email)
            contrasena = request.form['password']
            lista.append(contrasena)
            contrasena2 = request.form['password2']
            lista.append(contrasena2)
            rol = request.form['Rol']
            lista.append(rol)

            for j,i in enumerate(lista):
                if not i:
                    error = 'Debes ingresar un '+ str(lista_nombres[j])
                    flash(error)
                    return render_template('createuser.html')

            if contrasena!=contrasena2:
                    error = 'Las contraseñas no son iguales'
                    flash(error)
                    return render_template('createuser.html')
            
            error = None
            if not utils.isEmailValid(email):
                error = "El email no es valido"
                flash(error)
                return render_template('createuser.html')

            if not utils.isUsernameValid(nombreusuario):
                error = "El usuario no es valido"
                flash(error)
                return render_template('createuser.html')

            if not utils.isPasswordValid(contrasena):
                error = "El password no es valido"
                flash(error)
                return render_template('createuser.html')
            
            db = get_db()
        
            user = db.execute('SELECT Codigo FROM Usuario WHERE NombreUsuario=?', (nombreusuario,)).fetchone()
            mail = db.execute('SELECT Codigo FROM Usuario WHERE Email=?', (email,)).fetchone()
            coduser = db.execute('SELECT Codigo FROM Usuario WHERE Codigo=?', (codigo,)).fetchone()
            error=None

            if user is not None:
                error = 'El nombre de usuario ya existe'.format(email)
                flash(error)
                return render_template('register.html')
            
            if coduser is not None:
                error = 'El código de usuario ya existe'.format(email)
                flash(error)
                return render_template('register.html')
            
            if mail is not None:
                error = 'El email ya existe'.format(email)
                flash(error)
                return render_template('register.html')
            
            Superadministrador.crearUsuario(Superadministrador,codigo,nombre,nombreusuario, apellido, contrasena, celular,email,rol)

        return render_template('createuser.html')
    
    except Exception as ex:

        print(ex)
        return render_template('createuser.html')


@app.route('/createproduct',methods=('GET', 'POST'))
def createproduct():
    try:
        if request.method == 'POST':
            lista=[]
            lista_nombres=["nombre producto","código proveedor","marca","estado","inventario","código producto","precio","cantidad minima","descripción"]
            nombreproducto = request.form['nameproduct']
            lista.append(nombreproducto)
            codigoprovider = request.form['codprovider']
            lista.append(codigoprovider)
            marca = request.form['brand']
            lista.append(marca)
            estado = request.form['state']
            lista.append(estado)
            inventario = request.form['inventory']
            lista.append(inventario)
            codigoproducto = request.form['codproduct']
            lista.append(codigoproducto)
            precio = request.form['price']
            lista.append(precio)
            cantidadminima = request.form['amountmin']
            lista.append(cantidadminima)
            description= request.form["description"]
            lista.append(description)
            for j,i in enumerate(lista):
                if not i:
                    error = 'Debes ingresar un '+ str(lista_nombres[j])
                    flash(error)
                    return render_template('createproduct.html')
            

            Producto.crearProducto(Producto,nombreproducto,codigoprovider,marca, estado, inventario,codigoproducto,precio,cantidadminima,description)

        return render_template('createproduct.html')
    
    except Exception as ex:

        print(ex)
        return render_template('createproduct.html')


@app.route('/createprovider',methods=('GET', 'POST'))
def createprovider():
    try:
        if request.method == 'POST':
            lista=[]
            lista_nombres=["nombre empresa","código empresa","email","ciudad","dirección","celular","estado","linea de productos"]
            name = request.form['company']
            lista.append(name)
            codigo = request.form['codcompany']
            lista.append(codigo)
            email = request.form['correo']
            lista.append(email)
            ciudad = request.form['city']
            lista.append(ciudad)
            direccion = request.form['address']
            lista.append(direccion)
            celular = request.form['celular']
            lista.append(celular)
            estado = request.form['state']
            lista.append(estado)
            lineaproductos = request.form['lineaproductos']
            lista.append(lineaproductos)
            
            for j,i in enumerate(lista): 
                if not i:
                    error = 'Debes ingresar un '+ str(lista_nombres[j])
                    flash(error)
                    return render_template('createprovider.html')

            Proveedor.crearProvider(Proveedor,name,codigo,email, ciudad, direccion,celular, estado,lineaproductos)

        return render_template('createprovider.html')
    
    except Exception as ex:

        print(ex)
        return render_template('createprovider.html')



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

@app.route('/editareliminarusuario', methods=('GET', 'POST')) #ETHEL
def editareliminarusuario():
    try:
        if request.method == 'POST':
            lista=[]
            lista_nombres=["Buscar por","Valor"]
            busqueda = request.form['busqueda']
            lista.append(busqueda)
            valor = request.form['valor']
            lista.append(valor)
            for j,i in enumerate(lista):
                if not i:
                    error = 'Debes ingresar un '+ str(lista_nombres[j])
                    flash(error)
                    return render_template('createuser.html')
            us=Superadministrador.editarconsultarUser(Superadministrador,busqueda,valor)
            print(us)
        return render_template('editareliminarusuario.html')

    except Exception as ex:

        print(ex)
        return render_template('editareliminarusuario.html')
   

@app.route('/buscarProductoUsuarioFinal', methods=('GET', 'POST'))
def buscarProductoUsuarioFinal():
    try:
        if request.method == 'POST':
            
            lista=[]
            lista_nombres=["marca","código producto","cantidad minima","nombre producto","código proveedor","estado"]
            columsbd_nombres=["Marca","CodigoProducto","CantidadMinima","NombreProducto","CodigoProveedor","Estado"]
            marca = request.form['brand']
            lista.append(marca)
            codigo = request.form['codproduct']
            lista.append(codigo)
            cantidadminima= request.form['amountmin']
            lista.append(cantidadminima)
            name = request.form['nameproduct']
            lista.append(name)
            codprovider = request.form['codprovider']
            lista.append(codprovider)
            estado = request.form['state']
            lista.append(estado)
            colunms_buscar=""
            count=0
            count2=0
            ad=" AND "
            for i in lista:
                if i:
                    count+=1
            for j,i in enumerate(lista): 
                if i:
                    count2+=1
                    if count2==count:
                        ad=""
                    if columsbd_nombres[j]!="CantidadMinima":
                        colunms_buscar= colunms_buscar+'"'+columsbd_nombres[j]+'" == "'+str(lista[j])+'"'+ ad
                    elif lista[j]=="SI":
                        colunms_buscar= colunms_buscar+'"'+columsbd_nombres[j]+'" > "Inventario"'+ ad

            consulta=Producto.buscarProducto(Producto,colunms_buscar)
            print(consulta)
        return render_template("/buscarProductoUsuarioFinal.html")
    
    except Exception as ex:

        print(ex)
        return render_template("/buscarProductoUsuarioFinal.html")


@app.route('/buscarProviderUsuarioFinal')
def buscarProviderUsuarioFinal():
    return render_template('buscarProviderUsuarioFinal.html')  

@app.route('/PaginaProveedor')
def PaginaProveedor():
    return render_template('PaginaProveedor.html')

@app.route('/buscarusuario')
def buscarusuario():
    return render_template('buscarusuario.html')

@app.route('/PaginaProducto')
def PaginaProducto():
    return render_template('PaginaProducto.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8443)
