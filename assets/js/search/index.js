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

    $("#submit_button").click(function(e){
        event.preventDefault(e);
        $.ajax({
            data: {
                form: $("#form_search").serialize()
            },
            url : "/post/search/results/",
            type : "POST",
            success: function(newData){
                 if ($('#results').is(':visible'))
                {
                    $('#results').html(newData);
                }
                else
                {
                    $('#results').html(newData).show("slow");
                }
            }
        })
    });
});