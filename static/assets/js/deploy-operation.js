/**
 * Created by liyil on 2018/9/21.
 */


$(function () {
    initMenu();
    cmdMenu();
    getAppToHosts();
    selectSureBtn();
    deployOk();
});


Array.prototype.indexOf = function (val) {
    for (var i = 0; i < this.length; i++) {
        if (this[i] == val) return i;
    }
    return -1;
};

Array.prototype.remove = function (val) {
    var index = this.indexOf(val);
    if (index > -1) {
        this.splice(index, 1);
    }
};

function initMenu() {
    $('#deployMenuId').on('click', function () {
        if ($('#deployMenuId').hasClass('notExpand')) {
            $('#deployMenuId').removeClass('notExpand');
            $('#deployMenuId').addClass('expand');
            $('#deployMenuId').children('i:eq(0)').removeAttr("style");
            $('#deployMenuId').children('i:eq(0)').attr('style', 'transform: rotate(-180deg);');
            $('#deployMenuId').next().addClass('show');
            $('#deployMenuId').next().removeAttr("style");
            $('#deployMenuId').next().attr('style', 'overflow: hidden; display: block;');
        } else {
            $('#deployMenuId').removeClass('expand');
            $('#deployMenuId').addClass('notExpand');
            $('#deployMenuId').children('i:eq(0)').removeAttr("style");
            $('#deployMenuId').children('i:eq(0)').attr('style', 'transform: rotate(0deg);');
            $('#deployMenuId').next().removeClass('show');
            $('#deployMenuId').next().removeAttr("style");
            $('#deployMenuId').next().attr('style', 'overflow: hidden; display: none;');
        }
    })
}


function cmdMenu() {
    $('#cmdMenuId').on('click', '.group-list-show', function () {
        if ($(this).hasClass('notExpand')) {
            $(this).removeClass('notExpand');
            $(this).addClass('expand');
            $(this).children('i:eq(0)').removeAttr("style");
            $(this).children('i:eq(0)').attr('style', 'transform: rotate(-180deg);');
            $(this).next().addClass('show');
            $(this).next().removeAttr("style");
            $(this).next().attr('style', 'overflow: hidden; display: block;');
        } else {
            $(this).removeClass('expand');
            $(this).addClass('notExpand');
            $(this).children('i:eq(0)').removeAttr("style");
            $(this).children('i:eq(0)').attr('style', 'transform: rotate(0deg);');
            $(this).next().removeClass('show');
            $(this).next().removeAttr("style");
            $(this).next().attr('style', 'overflow: hidden; display: none;');
        }
    })
}


function getAppToHosts() {
    $('#app_list_id').on('click', function () {
        var app_id = $('#app_list_id option:selected').val();
        //console.log(app_id)
        var csrftoken = $("input[name='csrfmiddlewaretoken']").val();
        $.ajaxSetup({data: {csrfmiddlewaretoken: csrftoken}});
        $.ajax({
            url: 'deploy-batch.html',
            type: 'POST',
            data: {'app_id': app_id},
            dataType: 'JSON',
            traditional: true,
            success: function (callback) {
                if (callback.status) {
                    var host_data = callback.data;
                    var select_tag = '<option value="0">请选择</option>';
                    $('#select_host_id').empty();
                    $('#select_host_id').append(select_tag);
                    if (host_data == 0) {
                        $('#select_host_id').removeAttr('multiple');
                    } else {
                        $('#select_host_id').attr('multiple', 'multiple');
                    }
                    $.each(host_data, function (i, value) {
                        var option = document.createElement('option');
                        $(option).attr('value', value.id);
                        $(option).text(value.h__remote_user__username + '@' + value.h__host__ip_address);
                        $('#select_host_id').append(option)
                    })
                }


            }
        })
    })
}


function selectSureBtn() {
    $('#deployBodyId').on('click', '.select-sure-btn', function () {
        var deployData = {};
        $('#deployBodyId').find('select').each(function () {
            var v = $(this).val();
            var n = $(this).attr('name');
            if (n == "app_list" && v == 0) {
                layer.alert('应用模块未选择！', {
                    icon: 2,
                    skin: 'layer-ext-moon'
                });
                return false;
            }
            if (n == "version" && v == 0) {
                layer.alert('版本未选择！', {
                    icon: 2,
                    skin: 'layer-ext-moon'
                });
                return false;
            }
            if (n == "host_list" && v[0] == 0 && v.length == 1) {

                layer.alert('主机未选择！', {
                    icon: 2,
                    skin: 'layer-ext-moon'
                });
                return false;
            }
            if (v.constructor == Array) {
                v.remove('0')
            }
            deployData[n] = v;
        });

        var d = deployData;
        if (d && d.hasOwnProperty('app_list') && d.hasOwnProperty('version') && d.hasOwnProperty('host_list') ) {
            var app_name = $('#app_list_id option:selected').text();
            var app_version = $('#version_id option:selected').text();
            var host_list = [];
            $('#select_host_id option:selected').each(function () {
                var v = $(this).text();
                if (v == '请选择') {
                    return
                }
                host_list.push(v);
            });
            var host_list_str = host_list.join(',');
            var result = '模块名称: ' + app_name + '<br/>' + '版本号: ' + app_version + '<br/>' + '主机: ' + host_list_str;
            $.each(d, function (k, v) {
                $('#select_sure_result').attr(k, v);
            });
            $('#select_sure_result').html(result);
            $('.select-sure-btn').attr('disabled', 'disabled');
            $('.deploy-ok-btn').removeAttr('disabled');
        }else {
            return false;
        }
    })
}


function deployOk() {
    $('#deployBodyId').on('click', '.deploy-ok-btn', function () {
        var postData = {};
        postData['version'] = $('#select_sure_result').attr('version');
        postData['host_list'] = $('#select_sure_result').attr('host_list');
        postData['app_list'] = $('#select_sure_result').attr('app_list');
        console.log(postData)
        var csrftoken = $("input[name='csrfmiddlewaretoken']").val();
        $.ajaxSetup({data: {csrfmiddlewaretoken: csrftoken}});
        $.ajax({
            url: 'deploy-run.html',
            type: 'POST',
            data: postData,
            dataType: 'JSON',
            traditional: true,
            success: function (callback) {
                $('.deploy-ok-btn').attr('disabled', 'disabled');
                $('#get_result_id').text(callback.message)
            }
        })
    })
}


