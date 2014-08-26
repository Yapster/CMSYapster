/**
 * Created by Chris on 22/08/14.
 */

$(document).ready(function() {
    $("span.show_pix").click(function(e) {
        $(this).next('#upload_pix').slideDown('slow');
    });
    $("#add_new_user").change(function(){
        $(this).next().slideToggle("slow");
    });
});