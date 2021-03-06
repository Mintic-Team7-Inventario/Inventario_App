import functools
import os
from flask import (Flask, flash, g, make_response, redirect,
                   render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
import os
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
                    session['user_name'] = user[2]
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

            vava=[celular]
            names=["celular"]
            for k, va in enumerate(vava):
                resultado=utils.isIntenger(va)
                if resultado== False:
                    error = 'El ' + names[k]+ ' no es númerico'
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
      
            db = get_db()
   
            for j, i in enumerate(lista):
                if not i:
                    error = 'Debes ingresar un ' + str(lista_nombres[j])
                    flash(error)
                    return render_template('createproduct.html',session=session.get('tipo_usuario'))

            vava=[precio, cantidadminima,inventario]
            names=["precio", "cantidad mínima", "inventario"]
            for k, va in enumerate(vava):
                resultado=utils.isIntenger(va)
                if resultado== False:
                    error = 'El ' + names[k]+ ' no es númerico'
                    flash(error)
                    return render_template('createproduct.html',session=session.get('tipo_usuario'))

            nameproduct = db.execute('SELECT CodigoProducto FROM Producto WHERE NombreProducto=?', (nombreproducto,)).fetchone()
            codproduct = db.execute('SELECT CodigoProducto FROM Producto WHERE CodigoProducto=?', (codigoproducto,)).fetchone()
            proveedor = db.execute('SELECT Nombre FROM Proveedor WHERE Codigo=?', (codigoprovider,)).fetchone()
            error = None

            if nameproduct is not None:
                error = 'El nombre de producto ya existe'
                flash(error)
                return render_template('createproduct.html',session=session.get('tipo_usuario'))

            if codproduct is not None:
                error = 'El código de producto ya existe'
                flash(error)
                return render_template('createproduct.html',session=session.get('tipo_usuario'))

            if proveedor is None:
                error = 'El código de proveedor registrado no existe'
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

            vava=[celular]
            names=["celular"]
            for k, va in enumerate(vava):
                resultado=utils.isIntenger(va)
                if resultado== False:
                    error = 'El ' + names[k]+ ' no es númerico'
                    flash(error)
                    return render_template('createprovider.html',session=session.get('tipo_usuario'))



            Proveedor.crearProvider(Proveedor, name, codigo, email, ciudad, direccion, celular, estado, lineaproductos)

        return render_template('createprovider.html',session=session.get('tipo_usuario'))

    except Exception as ex:

        print(ex)
        return render_template('createprovider.html',session=session.get('tipo_usuario'))

@app.route('/editarproducto', methods=('GET', 'POST'))  # ETHEL
@login_required
def editarproducto():
    try:
        if request.method == 'POST':
            if Producto.eliminar!= None:
                consulta = Producto.editarconsultarProducto(Producto, "CodigoProducto", Producto.eliminar)
                if consulta:
                    headers =["Producto","Nombre","Proveedor","Estado","Inventario","Mínimo","Marca","Precio"]
                    items=[]
                    for i in range(len(consulta)):
                        items.append(dict(producto=[consulta[i][5],0],nombre=[consulta[i][0],0],proveedor=[consulta[i][1],0],estado=[consulta[i][3],0],inventario=[consulta[i][4],0],minimo=[consulta[i][7],0],marca=[consulta[i][2],0],precio=[consulta[i][6],0]))
                        items.append({"producto"+str(i):[None,0],"nombre"+str(i):[None,0],"proveedor" +str(i):[None,0],"estado"+str(i):[None,1],"inventario"+str(i):[None,0],"minimo"+str(i):[None,0],"marca"+str(i):[None,0],"precio"+str(i):[None,0]})

                return render_template("editareliminarproducto.html",session=session.get('tipo_usuario'),number=0,headers = headers,objects = items,edit="SI")
            else:
                return render_template("editareliminarproducto.html",session=session.get('tipo_usuario'),number=0,headers = [""],objects = [dict(mensaje=["No existen productos para editar",0])],edit="NO")

        return render_template("editareliminarproducto.html",session=session.get('tipo_usuario'),number=0,headers = [""],objects = [dict(mensaje=["No existen productos para editar",0])],edit="NO")

    except Exception as ex:
        print(ex)
        return render_template("editareliminarproducto.html",session=session.get('tipo_usuario'),number=0,headers = [""],objects = [dict(mensaje=["No existen productos para editar",0])],edit="NO")

@app.route('/editarproveedor', methods=('GET', 'POST'))  # ETHEL
@login_required
def editarproveedor():
    try:
        if request.method == 'POST':
            print(Proveedor.eliminar)
            if Proveedor.eliminar!= None:
                consulta = Proveedor.editarconsultarProveedor(Proveedor, "Codigo", Proveedor.eliminar)
                if consulta:
               
                    headers =["Nombre","Código","Ciudad","Linea Producto","Estado"]
                    items=[]
                    print(consulta)
                    for i in range(len(consulta)):
                        print("consulta i")
                        print(consulta[i])
                        items.append(dict(nombre=[consulta[i][0],0],codigo=[consulta[i][1],0],ciudad=[consulta[i][3],0],linea=[consulta[i][7],0],estado=[consulta[i][6],0]))
                        items.append({"nombre"+str(i):[None,0],"codigo"+str(i):[None,0],"ciudad" +str(i):[None,0],"linea"+str(i):[None,2],"estado"+str(i):[None,1]})
                return render_template("editareliminarproveedor.html",session=session.get('tipo_usuario'),number=0,headers = headers,objects = items,edit="SI")
            else:
                return render_template("editareliminarproveedor.html",session=session.get('tipo_usuario'),number=0,headers = [""],objects = [dict(mensaje=["No existen productos para editar",0])],edit="NO")

        return render_template("editareliminarproveedor.html",session=session.get('tipo_usuario'),number=0,headers = [""],objects = [dict(mensaje=["No existen productos para editar",0])],edit="NO")

    except Exception as ex:
        print(ex)
        return render_template("editareliminarproducto.html",session=session.get('tipo_usuario'),number=0,headers = [""],objects = [dict(mensaje=["No existen productos para editar",0])],edit="NO")

@app.route('/editarusuario', methods=('GET', 'POST'))  # ETHEL
@login_required
def editarusuario():
    try:
        if request.method == 'POST':
            print("aqui")
            print(Superadministrador.eliminar)
            if Superadministrador.eliminar!= None:
                consulta = Superadministrador.editarconsultarUser(Superadministrador, "Codigo", Superadministrador.eliminar)
                if consulta:
                    headers =["Codigo", "Nombre","Apellido","Celular",
                                "Email","Rol"]
                    items=[]
                    print(consulta)
                    for i in range(len(consulta)):

                        items.append(dict(codigo=[consulta[i][0],0],nombre=[consulta[i][1],0],apellido=[consulta[i][2],0],celular=[consulta[i][3],0],email=[consulta[i][4],0],rol=[consulta[i][5],0]))
                        items.append({"codigo"+str(i):[None,0],"nombre"+str(i):[None,0],"apellido" +str(i):[None,0],"celular"+str(i):[None,0],"email"+str(i):[None,0],"rol"+str(i):[None,1]})
                return render_template("editareliminarusuario.html",session=session.get('tipo_usuario'),number=0,headers = headers,objects = items,edit="SI")
            else:
                return render_template("editareliminarusuario.html",session=session.get('tipo_usuario'),number=0,headers = [""],objects = [dict(mensaje=["No existen productos para editar",0])],edit="NO")
        return render_template("editareliminarusuario.html",session=session.get('tipo_usuario'),number=0,headers = [""],objects = [dict(mensaje=["No existen productos para editar",0])],edit="NO")

    except Exception as ex:
        print(ex)
        return render_template("editareliminarusuario.html",session=session.get('tipo_usuario'),number=0,headers = [""],objects = [dict(mensaje="No existen productos para editar")],edit="NO")

@app.route('/guardarproducto', methods=('GET', 'POST'))  # ETHEL
@login_required
def guardarproducto():
    try:
        if request.method == 'POST':
            estado = request.form
            cambios=[]
            col=0
            cod=0
            c=0
            estado=estado.to_dict()
            print(estado)
            for valor in estado.values():
                if c==0:
                    ida=Producto.eliminar[cod]
                elif c % Producto.tamaño[1]==0:
                    print("--Cambio a:")
                    cod+=1
                    ida=Producto.eliminar[cod]
                    col=0
                if valor:
                    cambios.append([ida,Producto.columns[col], valor])
                col+=1
                c+=1
          
            if cambios:
                for cambio in cambios:
                    Producto.actualizarproducto(Producto,cambio[0],cambio[1],cambio[2])
                return render_template("editareliminarproducto.html",session=session.get('tipo_usuario'),number=0,headers = [""],objects = [dict(mensaje=["Productos actualizados exitosamente",0])],edit="NO")

    except Exception as ex:
        print(ex)
        return render_template("editareliminarproducto.html",session=session.get('tipo_usuario'),number=0,headers = [""],objects = [dict(mensaje=["No existen productos para guardar",0])],edit="NO")

@app.route('/guardarproveedor', methods=('GET', 'POST'))  # ETHEL
@login_required
def guardarproveedor():
    try:
        if request.method == 'POST':
            estado = request.form
            cambios=[]
            col=0
            cod=0
            c=0
            estado=estado.to_dict()
            print(estado)
            for valor in estado.values():
                if c==0:
                    ida=Proveedor.eliminar[cod]
                elif c % Proveedor.tamaño[1]==0:
                    print("--Cambio a:")
                    cod+=1
                    ida=Proveedor.eliminar[cod]
                    col=0
                if valor:
                    cambios.append([ida,Proveedor.columns[col], valor])
                col+=1
                c+=1
            print(Proveedor.columns)
            print('cambios')
            print(cambios)
            if cambios:
                for cambio in cambios:
                    print(cambio)
                    Proveedor.actualizarproveedor(Proveedor,cambio[0],cambio[1],cambio[2])
                return render_template("editareliminarproveedor.html",session=session.get('tipo_usuario'),number=0,headers = [""],objects = [dict(mensaje=["Proveedores actualizados exitosamente",0])],edit="NO")

    except Exception as ex:
        print(ex)
        return render_template("editareliminarproveedor.html",session=session.get('tipo_usuario'),number=0,headers = [""],objects = [dict(mensaje=["No existen proveedores para guardar",0])],edit="NO")

@app.route('/guardarusuario', methods=('GET', 'POST'))  # ETHEL
@login_required
def guardarusuario():
    try:
        if request.method == 'POST':
            estado = request.form
            cambios=[]
            col=0
            cod=0
            c=0
            print(estado)
            estado=estado.to_dict()
            print(estado)
            for valor in estado.values():
                print(Superadministrador.eliminar)
                if c==0:
                    ida=Superadministrador.eliminar[cod]
                elif c % Superadministrador.tamaño[1]==0:
                    print("--Cambio a:")
                    cod+=1
                    ida=Superadministrador.eliminar[cod]
                    col=0
                if valor:
                    cambios.append([ida,Superadministrador.columns[col], valor])
                col+=1
                c+=1
            print(Superadministrador.columns)
            print('cambios')
            print(cambios)
            if cambios:
                for cambio in cambios:
                    print(cambio)
                    Superadministrador.actualizarusuario(Superadministrador,cambio[0],cambio[1],cambio[2])
                return render_template("editareliminarusuario.html",session=session.get('tipo_usuario'),number=0,headers = [""],objects = [dict(mensaje=["Usuarios actualizados exitosamente",0])],edit="NO")

    except Exception as ex:
        print(ex)
        return render_template("editareliminarusuario.html",session=session.get('tipo_usuario'),number=0,headers = [""],objects = [dict(mensaje=["No existen usuarios para guardar",0])],edit="NO")


@app.route('/eliminarproducto', methods=('GET', 'POST'))  # ETHEL
@login_required
def eliminarproducto():
    try:
        if request.method == 'POST':
            print(Producto.eliminar)
            if Producto.eliminar!= None:
                Producto.eliminarproductos(Producto)
                return render_template("editareliminarproducto.html",session=session.get('tipo_usuario'),number=0,headers = [""],objects = [dict(mensaje=["Productos eliminados",0])],edit="NO")
            else:
                return render_template("editareliminarproducto.html",session=session.get('tipo_usuario'),number=0,headers = [""],objects = [dict(mensaje=["No existen productos para eliminar",0])],edit="NO")

        return render_template("editareliminarproducto.html",session=session.get('tipo_usuario'),number=0,headers = [""],objects = [dict(mensaje=["No existen productos para eliminar",0])],edit="NO")

    except Exception as ex:
        print(ex)
        return render_template("editareliminarproducto.html",session=session.get('tipo_usuario'),number=0,headers = [""],objects = [dict(mensaje=["No existen productos para eliminar",0])],edit="NO")

@app.route('/eliminarproveedor', methods=('GET', 'POST'))  # ETHEL
@login_required
def eliminarproveedor():
    try:
        if request.method == 'POST':
            print(Proveedor.eliminar)
            if Proveedor.eliminar!= None:
                Proveedor.eliminarproveedor(Proveedor)
                return render_template("editareliminarproveedor.html",session=session.get('tipo_usuario'),number=0,headers = [""],objects = [dict(mensaje=["Proveedores eliminados",0])],edit="NO")
            else:
                return render_template("editareliminarproveedor.html",session=session.get('tipo_usuario'),number=0,headers = [""],objects = [dict(mensaje=["No existen proveedores para eliminar",0])],edit="NO")

        return render_template("editareliminarproveedor.html",session=session.get('tipo_usuario'),number=0,headers = [""],objects = [dict(mensaje=["No existen proveedores para eliminar",0])],edit="NO")

    except Exception as ex:
        print(ex)
        return render_template("editareliminarproveedor.html",session=session.get('tipo_usuario'),number=0,headers = [""],objects = [dict(mensaje=["No existen proveedores para eliminar",0])],edit="NO")


@app.route('/eliminarusuario', methods=('GET', 'POST'))  # ETHEL
@login_required
def eliminarusuario(URL="editareliminarusuario.html"):
    try:
        if request.method == 'POST':
            print(Superadministrador.eliminar)
            if Superadministrador.eliminar!= None:
                Superadministrador.eliminarusuario(Superadministrador)
                return render_template("editareliminarusuario.html",session=session.get('tipo_usuario'),number=0,headers = [""],objects = [dict(mensaje="Usuarios eliminados")],edit="NO")
            else:
                return render_template("editareliminarusuario.html",session=session.get('tipo_usuario'),number=0,headers = [""],objects = [dict(mensaje="No existen usuarios para eliminar")],edit="NO")

        return render_template("editareliminarusuario.html",session=session.get('tipo_usuario'),number=0,headers = [""],objects = [dict(mensaje="No existen usuarios para eliminar")],edit="NO")

    except Exception as ex:
        print(ex)
        return render_template("editareliminarusuario.html",session=session.get('tipo_usuario'),number=0,headers = [""],objects = [dict(mensaje="No existen proveedores para eliminar")],edit="NO")


@app.route('/buscarProducto', methods=('GET', 'POST'))
@login_required
def buscarProducto():
    try:
        if request.method == 'POST':
            col=["Marca", "CodigoProducto", "CantidadMinima", "NombreProducto", "CodigoProveedor",
                                "Estado"]   
            lista = []
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
            valores_buscar=[]
            count = 0
            count2 = 0
            ad = " AND "
            
            for i in lista:
                if i:
                    count += 1
            for j, i in enumerate(lista):
                if i:
                    count2+=1
                    if count2==count:
                        ad=""
                    if col[j]!="CantidadMinima":
                        colunms_buscar= colunms_buscar+''+col[j]+' = ?'+ ad
                        valores_buscar.append(str(lista[j]))
                    elif col[j]=="CantidadMinima":
                    
                        if lista[j]=="SI":
                            colunms_buscar= colunms_buscar+''+col[j]+' > Inventario'+ ad
                            
                        else:
                            colunms_buscar= colunms_buscar+''+col[j]+' < Inventario'+ ad
                           
            print(colunms_buscar)
            print(valores_buscar)
            consulta=Producto.buscarProducto(Producto,colunms_buscar,valores_buscar)
            if consulta:
                number=len(consulta)
                headers =["Producto","Nombre","Proveedor","Estado","Inventario","Mínimo","Marca","Precio"]
                items=[]
                print(consulta)
                for i in range(len(consulta)):
                    print("consulta i")
                    print(consulta[i])
                    items.append(dict(producto=consulta[i][5],nombre=consulta[i][0],proveedor=consulta[i][1],estado=consulta[i][3],inventario=consulta[i][4],minimo=consulta[i][7],marca=consulta[i][2],precio=consulta[i][6]))
                
                return render_template("/buscarProducto.html",session=session.get('tipo_usuario'),number=number,headers = headers,objects = items,usuario=session.get('user_name'))
            else:
                return render_template("/buscarProducto.html",session=session.get('tipo_usuario'),number=0,headers = [""],objects = [dict(mensaje="No existen productos con estas especificaciones")], usuario=session.get('user_name'))
        return render_template("/buscarProducto.html",session=session.get('tipo_usuario'),number=0,usuario=session.get('user_name'))

    except Exception as ex:

        print(ex)
        return render_template("/buscarProducto.html",session=session.get('tipo_usuario'),number=0, usuario=session.get('user_name'))


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
            valores_buscar =[]
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
                    colunms_buscar= colunms_buscar+''+columsbd_nombres[j]+' = ?'+ ad
                    valores_buscar.append(str(lista[j]))
            consulta=Proveedor.buscarProveedor(Proveedor,colunms_buscar,valores_buscar)
            if consulta:
                number=len(consulta)
                headers =["Nombre","Código","Ciudad","Linea Producto","Estado", "Email"]
                items=[]
                
                for i in range(len(consulta)):
                 
                    items.append(dict(nombre=consulta[i][0],codigo=consulta[i][1],proveedor=consulta[i][2],estado=consulta[i][3],inventario=consulta[i][5],correo=consulta[i][4]))
                
                return render_template("buscarProvider.html",session=session.get('tipo_usuario'),number=number,headers = headers,objects = items)
            else:
                return render_template("buscarProvider.html",session=session.get('tipo_usuario'),number=0,headers = [""],objects = [dict(mensaje="No existen productos con estas especificaciones")])
        return render_template("buscarProvider.html",session=session.get('tipo_usuario'),number=0)

    except Exception as ex:

        print(ex)
        return render_template("buscarProvider.html",session=session.get('tipo_usuario'),number=0)

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
            valores_buscar=[]
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
                    colunms_buscar= colunms_buscar+''+columsbd_nombres[j]+' = ?'+ ad
                    valores_buscar.append(str(lista[j]))
            
            consulta=Administrador.buscarUsuario(Administrador,colunms_buscar,valores_buscar)
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
                
                return render_template("buscarusuario.html",session=session.get('tipo_usuario'),number=number,headers = headers,objects = items)
            else:
                return render_template("buscarusuario.html",session=session.get('tipo_usuario'),number=0,headers = [""],objects = [dict(mensaje="No existen productos con estas especificaciones")])
        return render_template("buscarusuario.html",session=session.get('tipo_usuario'),number=0)

    except Exception as ex:

        print(ex)
        return render_template("buscarusuario.html",session=session.get('tipo_usuario'),number=0)

@app.route('/editareliminarproducto', methods=('GET', 'POST'))  # ETHEL
@login_required
def editareliminarproducto():
    try:
        if request.method == 'POST':
            busqueda = request.form['busqueda']
            valor = request.form['valor']
  
            consulta = Producto.editarconsultarProducto(Producto, busqueda, valor)
            Producto.eliminar=None
            if consulta:
                number=len(consulta)
                headers =["Producto","Nombre","Proveedor","Estado","Inventario","Mínimo","Marca","Precio"]
                items=[]
                it=[]
                for i in range(len(consulta)):
                    items.append(dict(producto=[consulta[i][5],0],nombre=[consulta[i][0],0],proveedor=[consulta[i][1],0],estado=[consulta[i][3],0],inventario=[consulta[i][4],0],minimo=[consulta[i][7],0],marca=[consulta[i][2],0],precio=[consulta[i][6],0]))
                    it.append(consulta[i][5])
                Producto.eliminar=it
                Producto.columns=["CodigoProducto", "NombreProducto", "CodigoProveedor",
                                "Estado", "Inventario", "CantidadMinima", "Marca", "Precio"]
                Producto.tamaño=[number,len(headers)]
                Producto.headers=headers
                print(Producto.eliminar)
                return render_template("editareliminarproducto.html",session=session.get('tipo_usuario'),headers = headers,objects = items,number=number,edit="NO")
            else:
                return render_template("editareliminarproducto.html",session=session.get('tipo_usuario'),headers = [""],objects = [dict(mensaje=["No existen productos con estas especificaciones",0])],number=0,edit="NO")
        
        return render_template("editareliminarproducto.html",session=session.get('tipo_usuario'),number=0,edit="NO")

    except Exception as ex:
        print(ex)
        return render_template("editareliminarproducto.html",session=session.get('tipo_usuario'),number=0,edit="NO")


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
                it=[]
                print(consulta)
                for i in range(len(consulta)):
                    items.append(dict(nombre=[consulta[i][0],0],codigo=[consulta[i][1],0],ciudad=[consulta[i][3],0],linea=[consulta[i][7],0],estado=[consulta[i][6],0]))
                    it.append(consulta[i][1])
                Proveedor.eliminar=it
                Proveedor.columns=["Nombre","Codigo","Ciudad","LineaProductos","Estado"]
                Proveedor.tamaño=[number,len(headers)]
                Proveedor.headers=headers
                print(Proveedor.eliminar)
                return render_template("editareliminarproveedor.html",session=session.get('tipo_usuario'),headers = headers,objects = items,number=number,edit="NO")
            else:
                return render_template("editareliminarproveedor.html",session=session.get('tipo_usuario'),headers = [""],objects = [dict(mensaje=["No existen productos con estas especificaciones",0])],number=0,edit="NO")
        return render_template("editareliminarproveedor.html",session=session.get('tipo_usuario'),number=0,edit="NO")

    except Exception as ex:

        print(ex)
        return render_template("editareliminarproveedor.html",session=session.get('tipo_usuario'),number=0,edit="NO")

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
                it=[]
                for i in range(len(consulta)):
                    items.append(dict(nombre=[consulta[i][0],0],codigo=[consulta[i][1],0],proveedor=[consulta[i][2],0],estado=[consulta[i][3],0],inventario=[consulta[i][4],0],rol=[consulta[i][5],0]))
                    it.append(consulta[i][0])
                Superadministrador.eliminar=it
                Superadministrador.columns=["Codigo", "Nombre","Apellido","Celular",
                                "Email","Rol"]
                Superadministrador.tamaño=[number,len(headers)]
                Superadministrador.headers=headers
                print(Superadministrador.eliminar)
                print(Superadministrador.columns)
                number=len(Superadministrador.eliminar)
                return render_template("editareliminarusuario.html",session=session.get('tipo_usuario'),headers = headers,objects = items,number=number,edit="NO")
            else:
                return render_template("editareliminarusuario.html",session=session.get('tipo_usuario'),headers = [""],objects = [dict(mensaje=["No existen productos con estas especificaciones",0])],number=0,edit="NO")
        return render_template("editareliminarusuario.html",session=session.get('tipo_usuario'),number=0,edit="NO")

    except Exception as ex:

        print(ex)
        return render_template("editareliminarusuario.html",session=session.get('tipo_usuario'),number=0,edit="NO")


@app.route('/PaginaProveedor/<codigo_proveedor>', methods=('GET', 'POST'))
@login_required
def PaginaProveedor(codigo_proveedor):
    try:
        if request.method == 'GET':
            lista_proveedor=Proveedor.datosproveedor(Proveedor,codigo_proveedor)   
            consulta=Producto.editarconsultarProducto(Producto,"CodigoProveedor",codigo_proveedor)
            print(lista_proveedor)
            print(lista_proveedor)
            if consulta:
                number=len(consulta)
                headers =["Producto","Nombre","Proveedor","Estado","Inventario","Mínimo","Marca","Precio"]
                items=[]
                it=[]
                for i in range(len(consulta)):
                    items.append(dict(producto=consulta[i][5],nombre=consulta[i][0],proveedor=consulta[i][1],estado=consulta[i][3],inventario=consulta[i][4],minimo=consulta[i][7],marca=consulta[i][2],precio=consulta[i][6]))
                print( lista_proveedor)
                return render_template('PaginaProveedor.html',session=session.get('tipo_usuario'),proveedor=lista_proveedor,headers = headers,objects = items,number=number,edit="NO")
            return render_template('PaginaProveedor.html',session=session.get('tipo_usuario'),proveedor=lista_proveedor,headers = [""],objects = [dict(mensaje="No existen productos asociados a este proveedor")],number=0,edit="NO")        
    except Exception as ex:
        print(ex)
        return render_template('PaginaProveedor.html',session=session.get('tipo_usuario'),headers = [""],objects = [dict(mensaje="No existen productos asociados a este proveedor")],number=0,edit="NO")


@app.route('/PaginaProducto/<codigo_producto>')
@login_required
def PaginaProducto(codigo_producto):
    try:
        if request.method == 'GET':
            lista_producto=Producto.datosproducto(Producto,codigo_producto)  
            consulta=Producto.editarconsultarProducto2(Producto,"CodigoProducto",codigo_producto)
            if consulta:
                number=len(consulta)
                headers =["Nombre","Código","Email","Linea Producto","Estado", "Dirección"]
                items=[]
                print(consulta)
                for i in range(len(consulta)):
                    print("consulta i")
                    print(consulta[i])
                    items.append(dict(nombre=consulta[i][0],codigo=consulta[i][1],producto=consulta[i][2],estado=consulta[i][7],inventario=consulta[i][6],correo=consulta[i][4]))
                return render_template('PaginaProducto.html',session=session.get('tipo_usuario'),producto=lista_producto,headers = headers,objects = items,number=number,edit="NO")
            return render_template('PaginaProducto.html',session=session.get('tipo_usuario'),producto=lista_producto,headers = [""],objects = [dict(mensaje="No existen proveedores asociados a este proveedor")],number=0,edit="NO")        
    except Exception as ex:
        print(ex)
        return render_template('PaginaProducto.html',session=session.get('tipo_usuario'),headers = [""],objects = [dict(mensaje="No existen proveedores asociados a este proveedor")],number=0,edit="NO")

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
    app.run(host='127.0.0.1')
