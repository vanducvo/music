
function showalert(message) {
        $('#submitbutton').attr("disabled", true);
        $('#alert_placeholder').append('<div id="alertdiv"  class="alert alert-danger" role="alert" align="center"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')
                    setTimeout(function() {
                    $("#alertdiv").remove(); $('#submitbutton').attr("disabled", false);
                    }, 5000);
                                                    
}
function validateForm() {
    var format = /[ !@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/;
    var remail = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    var fname = document.forms["signupform"]["fname"].value;
    var lname = document.forms["signupform"]["lname"].value;
    var gender = document.forms["signupform"]["gender"].value;
    var role = document.forms["signupform"]["role"].value;
    var email = document.forms["signupform"]["email"].value;
    var username = document.forms["signupform"]["username"].value;
    var password = document.forms["signupform"]["password"].value;
    if (fname == "Nhập Tên" || format.test(fname)) {
        showalert("Tên không hợp lệ");
        return false;
    }
    if (lname == "Nhập Tên" || format.test(lname)) {
        showalert("Họ không hợp lệ");
        return false;
    }
    if (gender == "") {
        showalert("Chọn giới tính");
        return false;
    }
    if (role == "") {
        showalert("Chọn Loại Người Dùng");
        return false;
    }
    if (!remail.test(email)) {
        showalert("Email không hợp lệ");
        return false;
    }
    if (!/^[A-Za-z][A-Za-z0-9]+$/.test(username)) {
        showalert("Username bắt đầu bằng chữ \nvà không có ký tự đặt biệt");
        return false;
    }
    if(!/.{5}.+/.test(password)){
        showalert("Mật khẩu có ít nhất 6 ký tự");
        return false;
    }
    return true;
}

            $(document).on('submit', '#signupformid', function(e){
                e.preventDefault();
            if(validateForm()==true){
            $.ajax({
                        type: 'POST',
                        url: '/signup/',
                        data: {
                                fname: $('#fnameid').val(),
                                lname: $('#lnameid').val(),
                                gender: $('#genderid').val(),
                                role: $('#roleid').val(),
                                email: $('#emailid').val(),
                                username: $('#usernameid').val(),
                                password: $('#passwordid').val(),
                                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                        },
                        success:function(){
                            $('#submitbutton').attr("disabled", true);
                            $('#alert_placeholder').append('<div id="alertdiv"  class="alert alert-success" role="alert" align="center"><a class="close" data-dismiss="alert">×</a><span>Đăng Kí Thành Công</span></div>')
                            setTimeout(function() {
                            $("#alertdiv").remove();
                            }, 5000);
                        },
                        error:function(xhr, ajaxOptions, thrownError){
                            switch(xhr.status){
                                case 417:
                                        showalert("UserName Đã Tồn Tại");
                                        break;
                                case 418:
                                        showalert("Email Đã Tồn Tại");
                                        break;
                            }
                            
                        }
            });
        }
        });