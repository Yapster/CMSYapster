function load_stats()
{
    $.ajax({
        url : "/get/home_stats/",
        type : "POST",
        success: function(newData)
        {
            $("#stats_home").html(newData).delay(800).slideToggle("slow");
        }
    });
}

$(document).ready(function()
{
    load_stats();
});