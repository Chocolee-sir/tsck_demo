/**
 * Created by liyil on 2018/9/13.
 */


$(function () {
    assetsInit();
});


String.prototype.format = function (kwargs) {

    var ret = this.replace(/\{(\w+)\}/g, function (km, m) {
        return kwargs[m];
    });
    return ret;
};


function assetsInit() {
    $.ajax({
        url: 'assets-json.html',
        type: 'GET',
        dataType: 'JSON',
        success: function (result) {
            initGlobalData(result.global_dict);
            initHeader(result.table_config);
            initBody(result.table_config, result.data_list);
        }
    })
}


function initHeader(table_config) {
    var tr = document.createElement('tr');
    $.each(table_config, function (k, item) {
        if (item.display) {
            var th = document.createElement('th');
            th.innerHTML = item.title;
            $(tr).append(th);
        }
    });
    $('#table_th').append(tr);
}


function initBody(table_config, data_list) {
    $('#table_tb').empty();
    for (var i = 0; i < data_list.length; i++) {
        var row = data_list[i];
        // row = {'cabinet_num': '12B', 'cabinet_order': '1', 'id': 1},
        var tr = document.createElement('tr');
        tr.setAttribute('row-id', row['id']);
        $.each(table_config, function (i, colConfig) {
            if (colConfig.display) {
                var td = document.createElement('td');
                /* 生成文本信息 */
                var kwargs = {};
                $.each(colConfig.text.kwargs, function (key, value) {

                    if (value.substring(0, 2) == '@@') {
                        var globalName = value.substring(2, value.length); // 全局变量的名称
                        var currentId = row[colConfig.q]; // 获取的数据库中存储的数字类型值
                        var t = getTextFromGlobalById(globalName, currentId);
                        kwargs[key] = t;
                    }
                    else if (value[0] == '@') {
                        kwargs[key] = row[value.substring(1, value.length)]; //cabinet_num
                    } else {
                        kwargs[key] = value;
                    }
                });
                var temp = colConfig.text.content.format(kwargs);
                td.innerHTML = temp;


                /* 属性colConfig.attrs = {'edit-enable': 'true','edit-type': 'select'}  */
                $.each(colConfig.attrs, function (kk, vv) {
                    if (vv[0] == '@') {
                        td.setAttribute(kk, row[vv.substring(1, vv.length)]);
                    } else {
                        td.setAttribute(kk, vv);
                    }
                });

                $(tr).append(td);
            }
        });

        $('#table_tb').append(tr);
    }

}

function initGlobalData(global_dict) {
    $.each(global_dict, function (k, v) {
        // k = "device_type_choices"
        // v= [[0,'xx'],[1,'xxx']]
        window[k] = v;
    })
}

function getTextFromGlobalById(globalName, currentId) {
    // globalName = "device_type_choices"
    // currentId = 1
    var ret = null;
    $.each(window[globalName], function (k, item) {
        if (item[0] == currentId) {
            ret = item[1];
            return
        }
    });
    return ret;
}