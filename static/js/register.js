function check_email() {
    if (email_form.value.indexOf("@") == -1) {
        _email.innerHTML = "Use correct e-mail";
    } else {
        _email.innerHTML = "";
    }
}

function check_surname() {
    var x = "АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЬьЫыЪъЭэЮюЯя";
    var k = false;
    var str = surname_form.value;
    for (let i = 0; i < str.length; i++) {
        if (x.indexOf(str[i]) == -1) {
            k = true;
        }
    }
    if (k) {
        _surname.innerHTML = "Use correct surname";
    } else {
        _surname.innerHTML = "";
    }
}

function check_name() {
    var x = "АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЬьЫыЪъЭэЮюЯя";
    var k = false;
    var str = name_form.value;
    for (let i = 0; i < str.length; i++) {
        if (x.indexOf(str[i]) == -1) {
            k = true;
        }
    }
    if (k) {
        _name.innerHTML = "Use correct name";
    } else {
        _name.innerHTML = "";
    }
}

function check_second_name() {
    var x = "АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЬьЫыЪъЭэЮюЯя";
    var k = false;
    var str = second_name_form.value;
    for (let i = 0; i < str.length; i++) {
        if (x.indexOf(str[i]) == -1) {
            k = true;
        }
    }
    if (k) {
        _second_name.innerHTML = "Use correct second name";
    } else {
        _second_name.innerHTML = "";
    }
}

function check_psw() {
    if (password_form.value != password_repeat_form.value) {
        _password.innerHTML = "Passwords does not match";
    } else {
        _password.innerHTML = "";
    }
}