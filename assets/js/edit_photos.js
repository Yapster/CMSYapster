$(document).ready(function() {
    $(".picture_profile").click(function(){
        alert($(this).attr('id'));
        $.ajax({
            data : {
                new_photo: $(this).attr('id')
            },
            type : "POST",
            success: function(newData){
            }
        });
    });
});