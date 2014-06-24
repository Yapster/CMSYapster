/**
 * Created by Chris on 23/06/14.
 */

function visibility(thingId)
{
    var targetElement;

    targetElement = document.getElementById(thingId);
    if (targetElement.style.display == "none")
    {
        targetElement.style.display = "";
    }
    else
    {
        targetElement.style.display = "none";
    }
}

$(document).ready(function() {
    $("#btn_send_message").click(function() {
        var input_string = $("#message").val();
        alert(input_string);
        $.ajax({
            data : {
                message : input_string
            },
            url : "/home/",
            type : "POST",
            success : function(json) {
                alert(json.messages);
            },
            error : function(xhr,errmsg,err) {
                alert("Message not sent");
            }
        });
        return false;
    });
});

