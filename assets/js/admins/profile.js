$(document).ready(function() {
    $("#go_connect").click(function(){
        $("#go_connect").slideToggle("slow");
        $("#input_connect").slideToggle("slow");
    });
    $("#cancel_button").click(function(){
        alert("tamere")
        $("#input_connect").slideToggle("slow");
        $("#go_connect").slideToggle("slow");
    });
});