/**
 * Created by liyil on 2018/8/30.
 */
function inputPwdMd5() {
    var password_input = document.getElementById('pwd');
    var password_md5 = document.getElementById('pwd_md5');
    // set password
    password_md5.value =  hex_md5(password_input.value);
    return true;
}