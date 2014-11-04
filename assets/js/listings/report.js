//For single Report page

function display_new_input(divId)
{
    if (divId == "#new_note")
    {
        var other = "#new_answer";
    }
    else
    {
        var other = "#new_note";
    }
    if ($(other).is(':visible'))
    {
        $(other).slideToggle("slow");
    }
    $(divId).slideToggle("slow");
}

function take_in_charge(reportId)
{
    $.ajax({
        data : {
            typePost: 'take_in_charge',
            reportId : reportId
        },
        url : "/reports/post/take_in_charge/",
        type : "POST",
        success: function(newData){
            location.reload();
        }
    });
}

$(document).ready(function() {
//    $('.more_details_user').slideToggle("slow");
    $(".tab").click(function(){
        if (!$(this).hasClass("selected"))
        {
            ($('.tab').toggleClass('selected'));
            $('#new_answer').toggleClass("is_visible");
            $('#new_note').toggleClass("is_visible");
            $('#new_note_button').toggleClass("is_visible");
            $('#new_answer_button').toggleClass("is_visible");
        }
    });
    $(".note_first_raw").click(function(){
        $(this).next().slideToggle("slow");
    });
    $("#note_tab").click(function(){
        if ($("#email_tab.selected"))
        {
            $(other).slideToggle("slow");
        }
    });
    $('#checkbox_is_active').change(function(){
        if ($(this).is(':checked'))
        {
            $.ajax({
                data : {
                    typePost: 'checked',
                    reportId : $('#report_id').text()
                },
                url : "/reports/post/checked/",
                type : "POST",
                success: function(newData){
                    location.reload();
                }
            });
        }
        else
        {
            $.ajax({
                data : {
                    typePost: 'unchecked',
                    reportId : $('#report_id').text()
                },
                url : "/reports/post/checked/",
                type : "POST",
                success: function(newData){
                    location.reload();
                }
            });
        }
    });
});