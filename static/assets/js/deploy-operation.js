/**
 * Created by liyil on 2018/9/21.
 */


$(function () {
    initMenu();
    cmdMenu();
});


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

