/**
 * Created by liyil on 2018/9/3.
 */



    $(function () {
        bindDel();
        bindDelConfirm();
        bindEdit();
        bindEditConfirm();
        bindPersonal();
        bindPersonalConfirm();
    });


    function bindDel() {
        $('#userInfoId').on('click', '.del-row', function () {
            $('#userDelModal').modal('show');
            //获取当前行的ID
            var rowId = $(this).parent().parent().attr('nid');
            var deltitle = $(this).parent().attr('delusername');
            $('#delText').text(deltitle);
            $('#delNid').val(rowId);
        })
    }

    function bindDelConfirm() {
        $('#delConfirm').click(function () {
            var rowId = $('#delNid').val();
            $.ajax({
                url: 'del-user.html',
                type: 'GET',
                data: {'nid': rowId},
                success: function (arg) {
                    var dict = JSON.parse(arg);
                    if (dict.status) {
                        $('#userDelModal').modal('hide');
                        window.location.reload()
                    }
                }
            })
        })
    }

    function bindEdit() {
        $('#userInfoId').on('click', '.edit-row', function () {
            $('#userEditModal').modal('show');
            //获取当前行的所有数据
            //将数据赋值到对应的对话框的指定位置
            $(this).parent().prevAll().each(function () {
                var v = $(this).text();
                var n = $(this).attr('na');
                if (n == 'role_id') {
                    var rid = $(this).attr('rid');
                    $('#userEditModal select[name="role_id"]').val(rid)
                } else if (n == 'sex') {
                    if (v == '男') {
                        $('#userEditModal :radio[value="1"]').prop('checked', true);
                    } else {
                        $('#userEditModal :radio[value="0"]').prop('checked', true);
                    }
                } else {
                    $("#userEditModal input[name='" + n + "']").val(v)
                }
            })
        })
    }

    function bindEditConfirm() {
        $('#btnEditSave').click(function () {
            var postData = {};
            $('#userEditModal').find('input,select').each(function () {
                var v = $(this).val();
                var n = $(this).attr('name');
                if (n == 'sex') {
                    if ($(this).prop('checked')) {
                        postData[n] = v;
                    }
                } else {
                    postData[n] = v;
                }
            });

            $.ajax({
                url: 'edit-user.html',
                type: 'POST',
                data: postData,
                dataType: 'JSON',
                success: function (arg) {
                    if (arg.status) {
                        window.location.reload()
                    } else {
                        alert(arg.message)
                    }
                }
            })
        })
    }

    function bindPersonal() {
        $('#personalInfoid').on('click',function(){
            $('#personalInfoModal').modal('show');
        });
    }

    function bindPersonalConfirm(){
        $('#btnUserInfoSave').click(function(){
            var postData = {};
            $('#personalInfoModal').find('input').each(function (){
                var v = $(this).val();
                var n = $(this).attr('name');
                postData[n] = v;
            });

            $.ajax({
                url: 'personal-info.html',
                type: 'POST',
                data: postData,
                dataType: 'JSON',
                success: function (arg) {
                    if (arg.status) {
                        window.location.reload()
                    } else {
                        $('#pwdErrorMsg').text(arg.message);
                    }
                }
            })

        })
    }
