function show_hide_pass(){
    var checkbox = document.getElementById('show_pass');
    var input_pass = document.getElementById('password');
    if(checkbox.checked == true){
        input_pass.type = 'text';
    }else{
        input_pass.type = 'password';
    }
}

function val_email(){
    var input_email = document.getElementById('email').value;
    var show_error = document.getElementById('show_error');
    if(input_email.match(/^[a-z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-z0-9-]+(?:\.[a-z0-9-]+)*$/)) {
        // /^[a-z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-z0-9-]+(?:\.[a-z0-9-]+)*$/
        // /^[a-z0-9_]+@[a-z_]+?\.[a-z]{2,3}$/
        show_error.innerHTML = "";
        return true;
    }
    show_error.style.color = "red";
    show_error.innerHTML = "Email Invalid";
    return false;
}

function val_pass(){
    var input_pass = document.getElementById('password').value;
    var show_error = document.getElementById('show_error');
    if (input_pass.match(/^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s).{8,32}$/) && input_pass.length >= 8) {
        show_error.innerHTML = "";
        return true;
    }
    show_error.style.color = "red";
    show_error.innerHTML = "Password requirements: 1 capital, 1 special, 1 number, 8-32 characters";
    return false;
}

function check_pass(){
    var input_pass = document.getElementById('password').value;
    var input_pass1 = document.getElementById('password1').value;
    var show_error = document.getElementById('show_error');
    if (input_pass === input_pass1){
        show_error.innerText = "";
        return true;
    }else{
        show_error.style.color = "red";
        show_error.innerText = "Passwords don't match!";
        return false;
    }

}

function validateForm(){
    if(val_email() && val_pass() && check_pass()){
        return true;
    }else{
        return false;
    }
}