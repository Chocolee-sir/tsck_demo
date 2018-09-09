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
    bindOpsShowDetail();
    bindTestShowDetail();
    bindOpsHandleEdit();
    bindOpsHandleEditConfirm();
    bindTextHandleEdit();
    bindTextHandleEditConfirm();
});


function bindTextHandleEdit(){
    $('#testOtherOrderId').on('click', '.test-order-edit-row', function(){
        var rowId = $(this).parent().parent().attr('nid');
        $('#testHandleDataId').val(rowId);
        $("#testHandleOrderErrorMsg").empty();
        $('#testHandleTitle').text('测试处理工单');
        $('#testHandleOrderModal').modal('show');
    })
}


function bindTextHandleEditConfirm(){
    $('#btnTestHandleOrderSave').click(function(){
        var rowId = $('#testHandleDataId').val();
        //console.log(rowId)
        var postData = {};
        $('#testHandleOrderModal').find('input,textarea,select').each(function(){
            var v = $(this).val();
            var n = $(this).attr('name');
            postData[n] = v;
        });
         $.ajax({
                url: 'test-handle-order.html',
                type: 'POST',
                data: postData,
                dataType: 'JSON',
                success: function (arg) {
                    if (arg.status) {
                        window.location.reload()
                    } else {
                        $('#testHandleOrderErrorMsg').text(arg.message);
                    }
                }
        })

    })
}


function bindOpsHandleEdit(){
    $('#otherOrderId').on('click', '.ops-order-edit-row', function(){
        var rowId = $(this).parent().parent().attr('nid');
        $('#handleDataId').val(rowId);
        $("#handleOrderErrorMsg").empty();
        $('#argvHandleTitle').text('运维处理工单');
        $('#handleOrderModal').modal('show');
    })
}


function bindOpsHandleEditConfirm(){
    $('#btnHandleOrderSave').click(function(){
        var rowId = $('#handleDataId').val();
        //console.log(rowId)
        var postData = {};
        $('#handleOrderModal').find('input,textarea').each(function(){
            var v = $(this).val();
            var n = $(this).attr('name');
            postData[n] = v;
        });
         $.ajax({
                url: 'ops-handle-order.html',
                type: 'POST',
                data: postData,
                dataType: 'JSON',
                success: function (arg) {
                    if (arg.status) {
                        window.location.reload()
                    } else {
                        $('#handleOrderErrorMsg').text(arg.message);
                    }
                }
        })

    })
}


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
        $('#deleteOrderNid').val(rowId);
        $.ajax({
              url: 'get-detail.html',
              type: 'GET',
              data: {'nid': rowId},
              dataType: 'json',
              success: function (arg){
                  if(arg.status){
                      $('#deleteOrderModal').modal('show');
                      $('#deleteOrderSureId').addClass('btn-danger');
                      $('#deleteOrderCancelId').css('display','inline-block');
                      $('#deleteOrderTitle').text('确定删除这条工单信息?');
                      $('#deleteOrderText').html(arg.title);
                  }
             }
        })
    })
}


function bindOrderDelConfirm(){
    $('#deleteOrderSureId').click(function(){
        var rowId = $('#deleteOrderNid').val();
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


function bindOpsShowDetail(){
    $('#otherOrderId').on('click', '.show-detail-ok', function(){
        var rowId = $(this).parent().parent().attr('nid');
        var role = 'handler';
        $('#showDetailNid').val(rowId);
        $.ajax({
              url: 'get-detail.html',
              type: 'GET',
              data: {'nid': rowId, 'role': role},
              dataType: 'json',
              success: function (arg){
                  if(arg.status){
                      $('#showDetailModal').modal('show');
                      $('#showDetailTitle').text(arg.title);
                      $('#showDetailText').html(arg.detail);
                  }
             }
        })
    })
}


function bindTestShowDetail(){
    $('#testOtherOrderId').on('click', '.show-detail-ok', function(){
        var rowId = $(this).parent().parent().attr('nid');
        var role = 'handler';
        $('#showDetailNid').val(rowId);
        $.ajax({
              url: 'get-detail.html',
              type: 'GET',
              data: {'nid': rowId, 'role': role},
              dataType: 'json',
              success: function (arg){
                  if(arg.status){
                      $('#showDetailModal').modal('show');
                      $('#showDetailTitle').text(arg.title);
                      $('#showDetailText').html(arg.detail);
                  }
             }
        })
    })
}





