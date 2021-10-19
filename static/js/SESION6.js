
    document.addEventListener('DOMContentLoaded',

    function (){ document.querySelector('#busquedaeliminar').onchange=()=> {

        //Create array of options to be added
        var array = ["Activo","Inactivo"];

        if (document.querySelector('#busquedaeliminar').value==="Estado") { 
        //Create and append select list
        var selectList = document.createElement("select");
        selectList.id = "mySelect";
        document.querySelector('#tasks').append(selectList);

        //Create and append the options
        for (var i = 0; i < array.length; i++) {
            var option = document.createElement("option");
            option.value = array[i];
            option.text = array[i];
            selectList.appendChild(option);
        }
            

        } else {
      
            const li= document.createElement('input');
            li.id="mySelect";
            document.querySelector('#tasks').append(li);
        }
        document.getElementById("mySelect").remove();
        return false
    };
    
});


function validar_formulario(){
    //Almacena en variables los campos que obtiene del formulario
    var username = document.formUsuario.Nombreusuario;
    var email = document.formUsuario.Email;
    var password = document.formUsuario.password;

    //Almacena en una variable la longitud de lo ingresado en el formulario
    var username_len = username.value.length;
    if (username_len == 0 || username_len < 8) {
        alert("Debes ingresar un username con min. 8 caracteres");
        password.focus();
        return false; //Para la parte dos, que los datos se conserven
    }

    var formato_email = /^\w+([\.-]?\w+)@\w+([\.-]?\w+)(\.\w{2,3})+$/;
    if (!email.value.match(formato_email)) {
        alert("Debes ingresar un email electronico valido!");
        email.focus();
        return false; //Para la parte dos, que los datos se conserven
    }

    var passid_len = password.value.length;
    if (passid_len == 0 || passid_len < 8) {
        alert("Debes ingresar una password con mas de 8 caracteres");
        passid.focus();
    }
}

function mostrarPassword(){
    var obj = document.getElementById("password");
    obj.type = "text";
}

function ocultarPassword(){
    var obj = document.getElementById("password");
    obj.type = "password";
}