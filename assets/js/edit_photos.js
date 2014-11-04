$(document).ready(function() {
    $(".picture_profile").click(function(){
        $.ajax({
            data : {
                new_photo: $(this).attr('id')
            },
            type : "POST",
            success: function(newData){
                location.reload();
            }
        });
    });
});