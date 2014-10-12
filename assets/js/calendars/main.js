$(function()
{
    $("#datepicker").datepicker(
        {
            onSelect: function()
            {
                $.ajax({
                    type : "POST",
                    data : {
                        date: $(this).val()
                    },
                    url : "/calendar/week/",
                    success: function(newData){
                        if (newData) {
                            $('#calendar').html(newData).show("slow");
                        }
                    }
                });
            }
        }
    );
});

function change_display(IdInput)
{
    var offset = $(IdInput).val();
    var url = $(IdInput).attr('name');
    $.ajax({
        type : "POST",
        data : {
            offset: offset
        },
        url : "/calendar/" + url +"/",
        success: function(newData){
            if (newData) {
                $('#calendar').html(newData).show("slow");
            }
        }
    });
}

function see_details(offset, type_calendar)
{
    $.ajax({
        data : {
            offset: offset,
            type_calendar: type_calendar
        },
        url : "/calendar/" + type_calendar +"/",
        type : "POST",
        success: function(newData){
            if (newData) {
                $('#calendar').html(newData).show("slow");
            }
        }
    });
}

function hide_events()
{
    $('.inactive_cal').each(function(index) {
        var class_to_hide = $(this).attr('id');
        $('.' + class_to_hide).addClass('inactive_event');
    })
}

function toggle_calendar(calendarId)
{
    $('#color_' + calendarId).toggleClass("inactive_color");
    $('#calendar_' + calendarId).toggleClass("inactive_cal");
    $('.calendar_' + calendarId).toggleClass("inactive_event");
    hide_events();
}

function display_event(eventId)
{
    $.ajax({
        data : {
            id_event: eventId
        },
        url : "/calendar/details_event/",
        type : "POST",
        success: function(newData){
            if (newData) {
                if ($('#details_event').is(':visible'))
                {
                    $('#details_event').html(newData);
                }
                else
                {
                    $('#details_event').html(newData).show("slow");
                }
            }
        }
    });
}

function change_display_button(buttonId)
{
    $.ajax({
        data : {
            type_calendar: buttonId
        },
        url : "/calendar/" + buttonId +"/",
        type : "POST",
        success: function(newData){
            if (newData) {
                $('#calendar').html(newData).show("slow");
            }
            $(".button_form").removeClass('select');
            $("#button_" + buttonId).addClass('select');
        }
    });
}


function toggle_events(idCal)
{
    $('.' + idCal).toggleClass('inactive_event');
}

function new_calendar() {
    $("#form_new_calendar").slideToggle("slow");
}


function add_calendar(){
    var name = $('#name_new_calendar').val();
    var is_public = $('#is_public_new_calendar').is(':checked');
    alert(name);
    alert(is_public);
    $.ajax({
        data : {
            name: name,
            public: is_public
        },
        url : "/calendar/",
        type : "POST",
        success: function(newData){
            location.reload();
        },
        error : function(newData){
            $("#errors").html("Calendar can't have an empty name or already existing name");
        }
    });}

$(document).ready(function() {
//    $("#button_year").click(function(e) {
//        $.ajax({
//            data: {
//                form: $("#form_search").serialize()
//            },
//            url : "/post/search/results/",
//            type : "POST",
//            success: function(newData){
//
//            }
//        })
//    });

    $("#submit_button").click(function(e){
        event.preventDefault(e);
        $.ajax({
            data: {
                form: $("#form_search").serialize()
            },
            url : "/post/search/results/",
            type : "POST",
            success: function(newData){

            }
        })
    });
});