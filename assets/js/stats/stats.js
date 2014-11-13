// Display X users from 'title' stat, raw 'key'
function display_users(key, title)
{
    var list_users = [];
    $("." + key).each(function() {
        list_users.push($(this).val());
    });
    $.ajax({
        data : {
            users: list_users,
            title: title
        },
        url : "/lists/users/",
        type : "POST",
        success: function(newData){
            if (newData) {
                if ($('#more_infos').is(':visible'))
                {
                    $('#more_infos').html(newData);
                }
                else
                {
                    $('#more_infos').html(newData).show("slow");
                }
            }
        }
    });
}

//Display X countries from 'title' stat, raw 'key'
function display_countries(key, title)
{
    var list_countries = [];
    $("." + key).each(function() {
        list_countries.push($(this).val());
    });
    $.ajax({
        data : {
            countries: list_countries,
            title: title
        },
        url : "/lists/countries/",
        type : "POST",
        success: function(newData){
            if (newData) {
                if ($('#more_infos').is(':visible'))
                {
                    $('#more_infos').html(newData);
                }
                else
                {
                    $('#more_infos').html(newData).show("slow");
                }
            }
        }
    });
}

// Display X hashtags from 'title' stat, raw 'key'
function display_hashtags(key, title)
{
    var list_hashtags = [];
    $("." + key).each(function() {
        list_hashtags.push($(this).val());
    });
    $.ajax({
        data : {
            hashtags: list_hashtags,
            title: title
        },
        url : "/lists/hashtags/",
        type : "POST",
        success: function(newData){
            if (newData) {
                if ($('#more_infos').is(':visible'))
                {
                    $('#more_infos').html(newData);
                }
                else
                {
                    $('#more_infos').html(newData).show("slow");
                }
            }
        }
    });
}

function display_yaps(key, title)
{
    var list_yaps = [];
    $("." + key).each(function() {
        list_yaps.push($(this).val());
    });
    $.ajax({
        data : {
            yaps: list_yaps,
            title: title
        },
        url : "/lists/yaps/",
        type : "POST",
        success: function(newData){
            if (newData) {
                if ($('#more_infos').is(':visible'))
                {
                    $('#more_infos').html(newData);
                }
                else
                {
                    $('#more_infos').html(newData).show("slow");
                }
            }
        }
    });
}


// Display one column of stats
function load_col_stats(time, type_time)
{
    $('#' + type_time).html("Loading");
    var time_end, time_start = null;
    $.ajax({
        data : {
            time: time,
            type_stats: $("#type_stats").val(),
            type_time: type_time,
            time_end: time_end,
            time_start: time_start
        },
        url : "/statistics/more_data/",
        type : "POST",
        success: function(newData){
            if (newData) {
                $('#' + type_time).html(newData).show("slow");
            }
        }
    });
}


// Ajax Query for one stat
function spec_stats(time_start, time_end, type_search, name_method, type_stats)
{
    $.ajax({
        data : {
            time_start: time_start,
            time_end: time_end,
            type_search: type_search,
            name_method: name_method,
            type_stats: type_stats
        },
        url : "/statistics/spec_stats/",
        type : "POST",
        success: function(newData){
            if (newData) {

            }
        }
    });
}

$(document).ready(function() {
    // Preload 4 columns of stats
    load_col_stats('0', 'total');
    load_col_stats('1', 'min');
    load_col_stats('60', 'hour');
    load_col_stats('1440', 'day');

    // display state option once #country changed
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

    // Ajax the search and display res in new div #specific search
    $("#location_button").click(function(e) {
        alert($(location).attr('href'));
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
                type_stats: $(location).attr('href'),
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

    // More stats to display
    $("#more_tab").click(function(e) {
        $("#more_col").remove();
        $(".table_stats").append("<div class='col_stats' id='week_col'><div class='tab_icone' id='week_tab'>Week</div><div class='stats_container' id='week'></div></div>");
        $(".table_stats").append("<div class='col_stats' id='month_col'><div class='tab_icone' id='month_tab'>Month</div><div class='stats_container' id='month'></div></div>");
        $(".table_stats").append("<div class='col_stats' id='year_col'><div class='tab_icone' id='year_tab'>Year</div><div class='stats_container' id='year'></div></div>");
        load_col_stats('10080', 'week');
        load_col_stats('43829', 'month');
        load_col_stats('525949', 'year');
    });
});