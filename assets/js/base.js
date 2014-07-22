/**
 * Created by Chris on 26/06/14.
 */

function activate_messenger()
{
    $("#update_messager").slideToggle("slow");
    $("#message_line").slideToggle("slow");
}

function display_inactive(thingId) {
    $('#' + thingId).slideToggle("slow");

}

function navigation_bar()
{
    var path = window.location.pathname;
    path = decodeURIComponent(path);
    $(".text_icone").each(function () {
        var href = $(this).attr('href');
        if (path.substring(0, href.length) === href) {
            $(this).addClass('selected_icone');
            $(this).next().addClass('selected_icone');
        }
    });
    return false;
}

function side_bar()
{
    var path = window.location.pathname;
    $(".left_tab").each(function () {
        var href = $(this).attr('href');
        if (path.substring(0, href.length) === href) {
            $(this).addClass('selected_tab');
        }
    });
    return false;
}

function scroll_down()
{
    $('#conversation').animate({scrollTop: $("#conversation").prop("scrollHeight")}, 0);
    return false;
}

$(document).ready(function() {

    $("#message").keypress(function(e) {
        if (e.which == 13) {
            var input_string = $("#message").val();
            var data = $(".chater.on #conversation_id").val();
            $.ajax({
                data : {
                    message : input_string,
                    conversation : data
                },
                url : "/post/messenger/",
                type : "POST",
                success: function(newData){
                    $('#update_messager').html(newData);
                }
            });
            $('#message').val('');
            return false;
        }
    });
    $("#new_chat").click(function(e) {
        var data = [];
        var conversation = $(".chater.on #conversation_id").val();
        $(".chat_user.selected").each(function () {
            data.push($(this).text());
        });
        if (data != "")
        {
            $.ajax({
                data : {
                    chaters : data,
                    conversation : conversation
                },
                url : "/post/messenger/",
                type : "POST",
                success: function(newData){
                    $('#update_messager').html(newData);
                }
            });
            $('#message').val('');
            display_inactive('new_conversation');
        }
        return false;
    });
    setInterval(function() {
        if ($("#update_messager").is(":visible"))
        {
            var data = $(".chater.on #conversation_id").val();
            if (typeof data != 'undefined')
            {
                $.ajax(
                    {
                        data :
                        {
                            refresh : true,
                            conversation : data
                        },
                        url : "/post/messenger/",
                        type : "POST",
                        success : function(newData)
                        {
                            $('#update_messager').html(newData);
                        }
                    });
            }
            return false;
        }
        return false;
    }, 2000);
    $("span.chater").click(function(e) {
        $('.on').toggleClass("on");
        $(this).toggleClass("on");
        event.preventDefault(e);
        return false;
    });
    $("div.chat_user").click(function(e){
        $(this).toggleClass("selected");
        event.preventDefault(e);
        return false;
    });
    $("#more_conversations").click(function(e){
        $(".hide_conversation").slideToggle("slow");
    });
    $("#conversations").hover(function(e)
    {
        $("#more_conversations").slideToggle("slow");
        return false;
    });
    $(".tab_option").click(function(e){
        $('.selected.tab_green').toggleClass("selected");
        $(this).children("span").toggleClass("selected");
        event.preventDefault(e);
        return false;
    });
    navigation_bar();
    scroll_down();
    side_bar();
});