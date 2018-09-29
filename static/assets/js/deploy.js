/**
 * Created by liyil on 2018/9/22.
 */

var ResultRefreshObj;

function postTask() {
    var cmd_text = $("#cmd_input").val().trim();
    var selected_host_ids = [];
    $("[tag='host-select']:checked").each(function () {
        selected_host_ids.push($(this).val());
    });
    if (selected_host_ids.length == 0) {
        layer.alert('必须选择主机！', {
            icon: 2,
            skin: 'layer-ext-moon'
        });
        return false;
    }
    if (cmd_text.length == 0) {
        layer.alert('必须输入要执行的命令！', {
            icon: 2,
            skin: 'layer-ext-moon'
        });
        return false;
    }

    var uid = $("input[name='userid']").val();
    var task_arguments = {
        'selected_hosts': selected_host_ids,
        'task_type': 'cmd',
        'cmd': cmd_text,
        'uid': uid
    };

    var csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    $.ajaxSetup({
        data: {csrfmiddlewaretoken: csrftoken}
    });

    //禁用提交按钮
    $("#task_submit_btn").addClass("disabled");
    $("#task_result_container").empty();//清空之前的任务结

    $.ajax({
        url: 'deploy-cmd.html',
        type: 'POST',
        data: task_arguments,
        dataType: 'JSON',
        traditional: true,
        success: function (callback) {
            $.each(callback.selected_hosts, function (index, ele) {
                var li_ele = "<li log_id='" + ele['id'] + "' style='list-style-type: none;'>--------------Host:" + ele.host_to_remote_user__remote_user__username + "(" + ele.host_to_remote_user__host__ip_address + ")--------------<span tag='log_status'></span></li>";
                li_ele += "<pre>waiting for result</pre>";
                $("#task_result_container").append(li_ele);
            });
            //start to get result ....
            ResultRefreshObj = setInterval(function () {
                GetTaskResult(callback.task_id);
            }, 2000)
        }
    });

}


function GetTaskResult(task_id) {
    //
    $.getJSON("task-result.html", {'task_id': task_id}, function (callback) {
        var all_task_done = true;
        $.each(callback, function (index, ele) {
            var li_ele = $("li[log_id=" + ele['id'] + "]");
            li_ele.children().first().text(ele['status']);
            li_ele.next().text(ele['result']);

            if (ele['status'] == 0) {
                all_task_done = false; //有任务没完成
            }

        });

        if (all_task_done) {
            clearInterval(ResultRefreshObj);
            $("#task_submit_btn").removeClass("disabled");
            console.log("-------all task done---------");
        }

    });//end getJSOn
}


