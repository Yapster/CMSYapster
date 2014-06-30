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
    alert('#' + thingId);
    $('#' + thingId).slideDown("slow");
}

$(document).ready(function() {
    $("#message").keypress(function(e) {
        if (e.which == 13) {
            var input_string = $("#message").val();
            var data = [];
            $(".on").each(function(){
                data.push($(this).text());
            });
            $.ajax({
                data : {
                    message : input_string,
                    chaters : data
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
    $("p.chater").click(function() {
        $(this).toggleClass("on");
    });
    $("a.tab_option").click(function(e){
        $("a.selected").toggleClass("selected");
        $(this).addClass("selected");
        event.preventDefault(e);
    });
    setInterval(function() {
        if ($("#conversations").is(":visible"))
        {
            var data = [];
            $(".on").each(function(){
                data.push($(this).text());
            });
            $.ajax({
                data : {
                    refresh : true,
                    chaters : data
                },
                url : "/home/",
                type : "POST",
                success : function(newData){
                    $('#messages').html(newData);
                }
            });
            return false;
        }
        return false;
    }, 1000);
});