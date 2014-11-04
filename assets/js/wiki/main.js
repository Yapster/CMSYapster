function toggle_advanced() {
    $("#advanced_search_bar").slideToggle();
}

$(document).ready(function() {
//    $('.more_details_user').slideToggle("slow");
    $(".drop_down").click(function(){
        $(this).parent().next().slideToggle("slow");
    });
    $(".bookmark_toggle").click(function(){
        $(".bookmark_toggle").toggle();
    });
    $(".fav").click(function(){
        $("#bookmark_window").slideToggle("show");
        $("#fade").show();
    });
    $(".unfav").click(function(){
        $.ajax({
            data : {
                page_id : $('#page_id').val()
            },
            url : "/wiki/del_favorite/",
            type : "POST",
            success: function(newData){
                location.reload();
            }
        });
    });
    $("#close_bookmark_window").click(function(){
        $("#bookmark_window").slideToggle("slow");
        $("#fade").hide();
    });
    $("#submit_favorite").click(function(){
        $.ajax({
            data : {
                new_folder : $('#new_folder').val(),
                page_id : $('#page_id').val(),
                folder_id : $('#folder_id').val()
            },
            url : "/wiki/save_favorite/",
            type : "POST",
            success: function(newData){
                location.reload();
            }
        });
    });
    $("#slide_up").click(function(){
        $(this).toggleClass("select_slide");
        $(this).parent().next().slideToggle("slow");
        $(this).parent().next().next().slideToggle("slow");
    });
    $(".title_section").click(function(){
        $(this).parent().next().slideToggle("slow");
    });
    $(".input_form").change(function(){
        $(this).addClass("to_save");
    });

    $("#publish_article").click(function(){
        var obj = {};
        $(".to_save").each(function(){
            obj[$(this).attr('id')] = $(this).val();
        });
        $.ajax({
            data : {
                title: $("#title").val(),
                description: $("#main_section_text").val(),
                save_article: true,
                params : obj
            },
            url : "/wiki/" + $(this).val() + "/edit/",
            type : "POST",
            success: function(newData){

            }
        });
    });

    $("#edit_button").click(function(){
        $(".delete_box").toggleClass("hide");
        $(".edition_button").toggleClass("hide");
    });

    $(".edition_button").click(function(){
    });
});