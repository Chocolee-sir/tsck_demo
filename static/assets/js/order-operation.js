/**
 * Created by liyil on 2018/9/8.
 */


$(function () {
    bindCreateOrder();
    bindCreateOrderConfirm();
    bindOrderDel();
    bindOrderDelConfirm();
    bindOrderEdit();
    bindOrderEditConfirm();
});


function bindCreateOrder(){
    $('#createOrderId').on('click', function(){
        $("#createOrderErrorMsg").empty();
        $('#createOrderModal').modal('show');
    })
}


function bindCreateOrderConfirm(){
    $('#btnCreateOrderSave').click(function () {
        var postData = {};
        $('#createOrderModal').find('input,select,textarea').each(function () {
            var v = $(this).val();
            var n = $(this).attr('name');
            postData[n] = v;
        });

        $.ajax({
                url: 'create-order.html',
                type: 'POST',
                data: postData,
                dataType: 'JSON',
                success: function (arg) {
                    if (arg.status) {
                        window.location.reload()
                    } else {
                        $('#createOrderErrorMsg').text(arg.message);
                    }
                }
        })
    })
}


function bindOrderDel(){
    $('#orderInfoId').on('click', '.dev-order-del-row', function(){
        var rowId = $(this).parent().parent().attr('nid');
        $('#argvNid').val(rowId);
        $.ajax({
              url: 'get-detail.html',
              type: 'GET',
              data: {'nid': rowId},
              dataType: 'json',
              success: function (arg){
                  if(arg.status){
                      $('#argvModal').modal('show');
                      $('#argvSureId').addClass('btn-danger');
                      $('#argvCancelId').css('display','inline-block');
                      $('#argvTitle').text('确定删除这条工单信息?');
                      $('#argvText').html(arg.title);
                  }
             }
        })
    })
}


function bindOrderDelConfirm(){
    $('#argvSureId').click(function(){
        var rowId = $('#argvNid').val();
        $.ajax({
              url: 'del-order.html',
              type: 'GET',
              data: {'nid': rowId},
              success: function (arg) {
                  var dict = JSON.parse(arg);
                  if (dict.status) {
                      window.location.reload()
                  }
              }
        })
    })
}


function bindOrderEdit(){
    $('#orderInfoId').on('click', '.dev-order-edit-row', function(){
        $('#editOrderModal').modal('show');
        $(this).parent().prevAll().each(function (){
            var v = $(this).text();
            var n = $(this).attr('na');
            if (n == 'project_name'){
                var pid = $(this).attr('pid');
                $('#editOrderModal select[name="project_name"]').val(pid);
            }else if (n == 'env'){
                var eid = $(this).attr('eid');
                $('#editOrderModal select[name="env_label"]').val(eid);
            }else {
                $("#editOrderModal input[name='" + n + "']").val(v);
                $("#editOrderModal textarea[name='" + n + "']").val(v);
            }
        })

    })
}


function bindOrderEditConfirm() {
        $('#btnEditOrderSave').click(function () {
            var postData = {};
            $('#editOrderModal').find('input,select,textarea').each(function () {
                var v = $(this).val();
                var n = $(this).attr('name');
                postData[n] = v;
            });

            $.ajax({
                url: 'edit-order.html',
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