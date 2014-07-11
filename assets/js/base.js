/**
 * Created by Chris on 26/06/14.
 */

function activate_messenger()
{
    $("#conversations").slideToggle("slow");
    $("#conversation").slideToggle("slow");
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
                url : "/home/",
                type : "POST",
                success: function(newData){
                    $('#messages').html(newData);
                }
            });
            $('#message').val('');
            return false;
        }
    });
    $("span.chater").click(function() {
        $('.on').toggleClass("on");
        $(this).toggleClass("on");
    });
    $("div.chat_user").click(function(e){
        $(this).toggleClass("selected");
        event.preventDefault(e);
    });
    $("#new_chat").click(function(e) {
        var data = [];
        $(".chat_user.selected").each(function () {
            data.push($(this).text());
        });
    });
    setInterval(function() {
        if ($("#conversations").is(":visible"))
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
                        url : "/home/",
                        type : "POST",
                        success : function(newData)
                        {
                            $('#messages').html(newData);
                        }
                    });
            }
            return false;
        }
        return false;
    }, 2000);
    navigation_bar();
    scroll_down();
});