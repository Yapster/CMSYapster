/**
For all Reports page
 */

function take_in_charge(reportId)
{
    alert("wouow");
    $.ajax({
        data : {
            reportId : reportId,
            typePost : 'take_in_charge'
        },
        url : "/reports/post/take_in_charge/",
        type : "POST",
        success: function(newData){
            location.reload();
        }
    });
}

function toggle_unselected(typeId)
{
    $('#' + typeId + '_square').toggleClass("unselected");
    $('#' + typeId + '_text').toggleClass("unselected");
    $('#' + typeId + '_button').toggleClass("selected");
    $('.' + typeId + '_report').each(function(index) {
        $(this).toggleClass('inactive_report');
    });
}

$(document).ready(function() {
    $(".report_first_raw").click(function(){
        $(this).next().slideToggle("slow");
        $.ajax({
            data : {
                userId : $(this).find('.user_id').text()
            },
            url : "/lists/user/",
            type : "POST",
            context: this,
            success: function(newData){
                $(this).next().find('.user_details').html(newData);
            }
        });
    });
});