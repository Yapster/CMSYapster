$(document).ready(function() {
    $("#country").change(function() {
        var country = $("#country option:selected").val();
        if (country != 0) {
            $.ajax({
                data : {
                    country: country
                },
                url : "/get/location_option/",
                type : "POST",
                success: function(newData){
                    if (newData) {
                        $('#state_option').html(newData).show("slow");
                    }
                }
            });
        }
    }).trigger( "change" );
    $("#location_button").click(function(e) {
        var city = $("#city").val();
        var country = $("#country").val();
        var gender = $("#gender").val();
        var state = $("#state").val();
        var from_age = $("#from_age").val();
        var to_age = $("#to_age").val();
        $.ajax({
            data : {
                city: city,
                country: country,
                gender : gender,
                state : state,
                from_age: from_age,
                to_age: to_age,
                new_line: true
            },
            url : "/post/specific_search/",
            type : "POST",
            success: function(newData){
                $('#specific_search').html(newData).show("slow");
            }
        });
        return false;
    });
    $(".hide").click(function(e) {
        $.ajax({
            data : {
                more_data: true
            },
            url : "/post/more_data/",
            type : "POST",
            success: function(newData){
                $('#general_stats_table').html(newData);
            }
        });
    });
});