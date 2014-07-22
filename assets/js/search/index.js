$(document).ready(function() {
    $("#type_search").change(function() {

        var type_search = $("#type_search option:selected").val();
        if (type_search != 0) {
            $.ajax({
                data : {
                    type_search: type_search
                },
                url : "/post/search/",
                type : "POST",
                success: function(newData){
                    if (newData) {
                        $('#form_fields').html(newData).show("slow");
                    }
                }
            });
        }
    }).trigger( "change" );
});