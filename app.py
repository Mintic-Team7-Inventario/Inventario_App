import functools
import os
from flask import (Flask, flash, g, jsonify, make_response, redirect,
                   render_template, request, send_file, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

import utils
from Administrador import Administrador
from db import close_db, get_db
from Producto import Producto
from Proveedor import Proveedor
from Superadministrador import Superadministrador
from UsuarioFinal import UsuarioFinal

app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(12)


@app.route('/')
def index():
    if g.user:
            return redirect(url_for('buscarProducto'))
    return render_template('login.html')


@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        db = get_db()
        g.user = db.execute('SELECT * FROM Usuario WHERE Codigo = ?', (user_id,)).fetchone()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))
        return view(**kwargs)

    return wrapped_view


@app.route('/login', methods=('GET', 'POST'))
def login():
    try:
        print('aqui')
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            error = None
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
@login_required
def createuser():
    try:
        if request.method == 'POST':
            lista = []
            lista_nombres = ["código", "nombre", "nombre usuario", "apellido", "celular", "email", "contraseña",
                             "confirmar contraseña"]
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

            for j, i in enumerate(lista):
                if not i:
                    error = 'Debes ingresar un ' + str(lista_nombres[j])
                    flash(error)
                    return render_template('createuser.html',session=session.get('tipo_usuario'))

            if contrasena != contrasena2:
                error = 'Las contraseñas no son iguales'
                flash(error)
                return render_template('createuser.html',session=session.get('tipo_usuario'))

            error = None
            if not utils.isEmailValid(email):
                error = "El email no es valido"
                flash(error)
                return render_template('createuser.html',session=session.get('tipo_usuario'))

            if not utils.isUsernameValid(nombreusuario):
                error = "El usuario no es valido"
                flash(error)
                return render_template('createuser.html',session=session.get('tipo_usuario'))

            if not utils.isPasswordValid(contrasena):
                error = "El password no es valido"
                flash(error)
                return render_template('createuser.html',session=session.get('tipo_usuario'))

            db = get_db()

            user = db.execute('SELECT Codigo FROM Usuario WHERE NombreUsuario=?', (nombreusuario,)).fetchone()
            mail = db.execute('SELECT Codigo FROM Usuario WHERE Email=?', (email,)).fetchone()
            coduser = db.execute('SELECT Codigo FROM Usuario WHERE Codigo=?', (codigo,)).fetchone()
            error = None

            if user is not None:
                error = 'El nombre de usuario ya existe'.format(email)
                flash(error)
                return render_template('createuser.html',session=session.get('tipo_usuario'))

            if coduser is not None:
                error = 'El código de usuario ya existe'.format(email)
                flash(error)
                return render_template('createuser.html',session=session.get('tipo_usuario'))

            if mail is not None:
                error = 'El email ya existe'.format(email)
                flash(error)
                return render_template('createuser.html',session=session.get('tipo_usuario'))

            Superadministrador.crearUsuario(Superadministrador, codigo, nombre, nombreusuario, apellido, contrasena,
                                            celular, email, rol)

        return render_template('createuser.html',session=session.get('tipo_usuario'))

    except Exception as ex:

        print(ex)
        return render_template('createuser.html',session=session.get('tipo_usuario'))


@app.route('/createproduct', methods=('GET', 'POST'))
@login_required
def createproduct():
    try:
        if request.method == 'POST':
            lista = []
            lista_nombres = ["nombre producto", "código proveedor", "marca", "estado", "inventario", "código producto",
                             "precio", "cantidad minima", "descripción"]
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
            description = request.form["description"]
            lista.append(description)
            for j, i in enumerate(lista):
                if not i:
                    error = 'Debes ingresar un ' + str(lista_nombres[j])
                    flash(error)
                    return render_template('createproduct.html',session=session.get('tipo_usuario'))

            db = get_db()

            nameproduct = db.execute('SELECT CodigoProducto FROM Producto WHERE NombreProducto=?', (nombreproducto,)).fetchone()
            codproduct = db.execute('SELECT CodigoProducto FROM Producto WHERE CodigoProducto=?', (codigoproducto,)).fetchone()
            error = None

            if nameproduct is not None:
                error = 'El nombre de producto ya existe'
                flash(error)
                return render_template('createproduct.html',session=session.get('tipo_usuario'))

            if codproduct is not None:
                error = 'El código de producto ya existe'
                flash(error)
                return render_template('createproduct.html',session=session.get('tipo_usuario'))

            Producto.crearProducto(Producto,nombreproducto,codigoprovider,marca, estado, inventario,codigoproducto,precio,cantidadminima,description)

        return render_template('createproduct.html',session=session.get('tipo_usuario'))

    except Exception as ex:

        print(ex)
        return render_template('createproduct.html',session=session.get('tipo_usuario'))


@app.route('/createprovider', methods=('GET', 'POST'))
@login_required
def createprovider():
    try:
        if request.method == 'POST':
            lista = []
            lista_nombres = ["nombre empresa", "código empresa", "email", "ciudad", "dirección", "celular", "estado",
                             "linea de productos"]
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

            for j, i in enumerate(lista):
                if not i:
                    error = 'Debes ingresar un ' + str(lista_nombres[j])
                    flash(error)
                    return render_template('createprovider.html',session=session.get('tipo_usuario'))

            Proveedor.crearProvider(Proveedor, name, codigo, email, ciudad, direccion, celular, estado, lineaproductos)

        return render_template('createprovider.html',session=session.get('tipo_usuario'))

    except Exception as ex:

        print(ex)
        return render_template('createprovider.html',session=session.get('tipo_usuario'))


@app.route('/editareliminarproducto', methods=('GET', 'POST'))  # ETHEL
@login_required
def editareliminarproducto():
    try:
        if request.method == 'POST':
           
            lista = []
            busqueda = request.form['busqueda']
            lista.append(busqueda)
            valor = request.form['valor']
            lista.append(valor)
            consulta = Producto.editarconsultarProducto(Producto, busqueda, valor)
            if consulta:
                number=len(consulta)
                headers =["Producto","Nombre","Proveedor","Estado","Inventario","Mínimo","Marca","Precio"]
                items=[]
                ite=[]
                for i in range(len(consulta)):
                    items.append(dict(producto=consulta[i][5],nombre=consulta[i][0],proveedor=consulta[i][1],estado=consulta[i][3],inventario=consulta[i][4],minimo=consulta[i][7],marca=consulta[i][2],precio=consulta[i][6]))
                    ite.append(consulta[i][5])
                session['delete']=ite
                return render_template("editareliminarproducto.html",session=session.get('tipo_usuario'),headers = headers,objects = items,number=number)
            else:
                return render_template("editareliminarproducto.html",session=session.get('tipo_usuario'),headers = [""],objects = [dict(mensaje="No existen productos con estas especificaciones")],number=0)
        
        return render_template("editareliminarproducto.html",session=session.get('tipo_usuario'),number=0)

    except Exception as ex:
        print(ex)
        return render_template("editareliminarproducto.html",session=session.get('tipo_usuario'),number=0)



@app.route('/editareliminarproveedor', methods=('GET', 'POST'))  # ETHEL
@login_required
def editareliminarproveedor():
    try:
        if request.method == 'POST':
            lista = []
            busqueda = request.form['busqueda']
            lista.append(busqueda)
            valor = request.form['valor']
            lista.append(valor)
            consulta = Proveedor.editarconsultarProveedor(Proveedor, busqueda, valor)
            if consulta:
                number=len(consulta)
                headers =["Nombre","Código","Ciudad","Linea Producto","Estado"]
                items=[]
                print(consulta)
                for i in range(len(consulta)):
                    print("consulta i")
                    print(consulta[i])
                    items.append(dict(nombre=consulta[i][0],codigo=consulta[i][1],proveedor=consulta[i][2],estado=consulta[i][4],inventario=consulta[i][2]))
                
                return render_template("editareliminarproveedor.html",session=session.get('tipo_usuario'),headers = headers,objects = items,number=number)
            else:
                return render_template("editareliminarproveedor.html",session=session.get('tipo_usuario'),headers = [""],objects = [dict(mensaje="No existen productos con estas especificaciones")],number=0)
        return render_template("editareliminarproveedor.html",session=session.get('tipo_usuario'),number=0)

    except Exception as ex:

        print(ex)
        return render_template("editareliminarproveedor.html",session=session.get('tipo_usuario'),number=0)


@app.route('/buscarProducto', methods=('GET', 'POST'))
@login_required
def buscarProducto():
    try:
        if request.method == 'POST':

            lista = []
            lista_nombres = ["marca", "código producto", "cantidad minima", "nombre producto", "código proveedor",
                             "estado"]
            columsbd_nombres = ["Marca", "CodigoProducto", "CantidadMinima", "NombreProducto", "CodigoProveedor",
                                "Estado"]
            marca = request.form['brand']
            lista.append(marca)
            codigo = request.form['codproduct']
            lista.append(codigo)
            cantidadminima = request.form['amountmin']
            lista.append(cantidadminima)
            name = request.form['nameproduct']
            lista.append(name)
            codprovider = request.form['codprovider']
            lista.append(codprovider)
            estado = request.form['state']
            lista.append(estado)
            colunms_buscar = " "
            count = 0
            count2 = 0
            ad = " AND "

            for i in lista:
                if i:
                    count += 1
            for j, i in enumerate(lista):
                if i:
                    count2+=1
                    print(columsbd_nombres[j])
                    if count2==count:
                        ad=""
                    if columsbd_nombres[j]!="CantidadMinima":
                        colunms_buscar= colunms_buscar+''+columsbd_nombres[j]+' = "'+str(lista[j])+'"'+ ad
                    elif columsbd_nombres[j]=="CantidadMinima":
                    
                        if lista[j]=="SI":
                            colunms_buscar= colunms_buscar+''+columsbd_nombres[j]+' > Inventario'+ ad
                        else:
                           
                            colunms_buscar= colunms_buscar+''+columsbd_nombres[j]+' < Inventario'+ ad
            
            
            consulta=Producto.buscarProducto(Producto,colunms_buscar)
            if consulta:
                headers =["Producto","Nombre","Proveedor","Estado","Inventario","Mínimo","Marca","Precio"]
                items=[]
                print(consulta)
                for i in range(len(consulta)):
                    print("consulta i")
                    print(consulta[i])
                    items.append(dict(producto=consulta[i][5],nombre=consulta[i][0],proveedor=consulta[i][1],estado=consulta[i][3],inventario=consulta[i][4],minimo=consulta[i][7],marca=consulta[i][2],precio=consulta[i][6]))
                
                return render_template("/buscarProducto.html",session=session.get('tipo_usuario'),headers = headers,objects = items)
            else:
                return render_template("/buscarProducto.html",session=session.get('tipo_usuario'),headers = [""],objects = [dict(mensaje="No existen productos con estas especificaciones")])
        return render_template("/buscarProducto.html",session=session.get('tipo_usuario'))

    except Exception as ex:

        print(ex)
        return render_template("/buscarProducto.html",session=session.get('tipo_usuario'))


@app.route('/buscarProvider', methods=('GET', 'POST'))
@login_required
def buscarProvider():
    try:
        if request.method == 'POST':

            lista = []
            columsbd_nombres = ["Nombre", "Codigo", "Ciudad",
                                "Estado","LineaProductos"]
            nombrep = request.form['nombrep ']
            lista.append(nombrep)
            codigo = request.form['codprovee']
            lista.append(codigo)
            ciudad = request.form['ciudad']
            lista.append(ciudad)
            estado= request.form['state']
            lista.append(estado)
            linea = request.form['linea']
            lista.append(linea)
            colunms_buscar = " "
            count = 0
            count2 = 0
            ad = " AND "

            for i in lista:
                if i:
                    count += 1
            for j, i in enumerate(lista):
                if i:
                    count2+=1
                    print(columsbd_nombres[j])
                    if count2==count:
                        ad=""
                    if columsbd_nombres[j]!="CantidadMinima":
                        colunms_buscar= colunms_buscar+''+columsbd_nombres[j]+' = "'+str(lista[j])+'"'+ ad
                    elif columsbd_nombres[j]=="CantidadMinima":
                    
                        if lista[j]=="SI":
                            colunms_buscar= colunms_buscar+''+columsbd_nombres[j]+' > Inventario'+ ad
                        else:
                           
                            colunms_buscar= colunms_buscar+''+columsbd_nombres[j]+' < Inventario'+ ad
            
            
            consulta=Proveedor.buscarProveedor(Proveedor,colunms_buscar)
            if consulta:
                headers =["Nombre","Código","Ciudad","Linea Producto","Estado"]
                items=[]
                print(consulta)
                for i in range(len(consulta)):
                    print("consulta i")
                    print(consulta[i])
                    items.append(dict(nombre=consulta[i][0],codigo=consulta[i][1],proveedor=consulta[i][2],estado=consulta[i][4],inventario=consulta[i][2]))
                
                return render_template("buscarProvider.html",session=session.get('tipo_usuario'),headers = headers,objects = items)
            else:
                return render_template("buscarProvider.html",session=session.get('tipo_usuario'),headers = [""],objects = [dict(mensaje="No existen productos con estas especificaciones")])
        return render_template("buscarProvider.html",session=session.get('tipo_usuario'))

    except Exception as ex:

        print(ex)
        return render_template("buscarProvider.html",session=session.get('tipo_usuario'))



@app.route('/editareliminarusuario', methods=('GET', 'POST'))  # ETHEL
@login_required
def editareliminarusuario():
    try:
        if request.method == 'POST':
            lista = []
            busqueda = request.form['busqueda']
            lista.append(busqueda)
            valor = request.form['valor']
            lista.append(valor)
        
            consulta = Superadministrador.editarconsultarUser(Superadministrador, busqueda, valor)
            if consulta:
                number=len(consulta)
                headers =["Codigo", "Nombre","Apellido","Celular",
                                "Email","Rol"]
                items=[]
                print(consulta)
                for i in range(len(consulta)):
                    print("consulta i")
                    print(consulta[i])
                    items.append(dict(nombre=consulta[i][0],codigo=consulta[i][1],proveedor=consulta[i][2],estado=consulta[i][3],inventario=consulta[i][4],rol=consulta[i][5]))
                
                return render_template("editareliminarusuario.html",session=session.get('tipo_usuario'),headers = headers,objects = items,number=number)
            else:
                return render_template("editareliminarusuario.html",session=session.get('tipo_usuario'),headers = [""],objects = [dict(mensaje="No existen productos con estas especificaciones")],number=0)
        return render_template("editareliminarusuario.html",session=session.get('tipo_usuario'),number=0)

    except Exception as ex:

        print(ex)
        return render_template("editareliminarusuario.html",session=session.get('tipo_usuario'),number=0)



@app.route('/PaginaProveedor', methods=('GET', 'POST'))
@login_required
def PaginaProveedor():
    return render_template('PaginaProveedor.html',session=session.get('tipo_usuario'))


@app.route('/buscarusuario', methods=('GET', 'POST'))
@login_required
def buscarusuario():
    try:
        if request.method == 'POST':

            lista = []
            columsbd_nombres = ["Codigo", "Nombre","Rol","Apellido",
                                "Email"]
            codigo = request.form['codigo']
            lista.append(codigo)
            codigo = request.form['nombre']
            lista.append(codigo)
            ol = request.form['rol']
            lista.append(ol)
            apellido= request.form['apellido']
            lista.append(apellido)
            email = request.form['email']
            lista.append(email)
            colunms_buscar = " "
            count = 0
            count2 = 0
            ad = " AND "

            for i in lista:
                if i:
                    count += 1
            for j, i in enumerate(lista):
                if i:
                    count2+=1
                    print(columsbd_nombres[j])
                    if count2==count:
                        ad=""
                    colunms_buscar= colunms_buscar+''+columsbd_nombres[j]+' = "'+str(lista[j])+'"'+ ad
                   
            
            consulta=Administrador.buscarUsuario(Administrador,colunms_buscar)
            if consulta:
                headers =["Codigo", "Nombre","Apellido","Celular",
                                "Email","Rol"]
                items=[]
                print(consulta)
                for i in range(len(consulta)):
                    print("consulta i")
                    print(consulta[i])
                    items.append(dict(nombre=consulta[i][0],codigo=consulta[i][1],proveedor=consulta[i][2],estado=consulta[i][3],inventario=consulta[i][4],rol=consulta[i][5]))
                
                return render_template("buscarusuario.html",session=session.get('tipo_usuario'),headers = headers,objects = items)
            else:
                return render_template("buscarusuario.html",session=session.get('tipo_usuario'),headers = [""],objects = [dict(mensaje="No existen productos con estas especificaciones")])
        return render_template("buscarusuario.html",session=session.get('tipo_usuario'))

    except Exception as ex:

        print(ex)
        return render_template("buscarusuario.html",session=session.get('tipo_usuario'))



@app.route('/PaginaProducto')
@login_required
def PaginaProducto():
    return render_template('PaginaProducto.html',session=session.get('tipo_usuario'))


@app.route('/changepass', methods=('GET', 'POST'))
@login_required
def changepass():
    try:
        if request.method == 'POST':
            passwordold = request.form['password']
            passwordnew = request.form['newpassword']
            passwordnew2 = request.form['confirmpassword']

            if not utils.isPasswordValid(passwordold):
                error = "La contraseña actual no es valida"
                flash(error)
                return render_template('changepass.html')

            if not utils.isPasswordValid(passwordnew):
                error = "La nueva contraseña no es valida"
                flash(error)
                return render_template('changepass.html')

            if not utils.isPasswordValid(passwordnew2):
                error = "La confirmación de contraseña no es valida"
                flash(error)
                return render_template('changepass.html')

            db = get_db()
            results = check_password_hash(g.user[3], passwordold)

            if results is False:
                error = 'La contraseña actual es inválida'
                flash(error)
            elif passwordnew != passwordnew2:
                error = 'Las nuevas contraseñas no son iguales'
                flash(error)
            else:
                db.execute("UPDATE Usuario SET Contrasena = ? WHERE codigo = ?",
                           (generate_password_hash(passwordnew), g.user[0])).fetchone()
                db.commit()
        return render_template('changepass.html',session=session.get('tipo_usuario'))
    except Exception as ex:

        print(ex)
        return render_template('changepass.html',session=session.get('tipo_usuario'))


@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8443)
