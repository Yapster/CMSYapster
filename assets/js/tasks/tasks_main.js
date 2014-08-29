$(function()
{

});

function hide_tasks()
{
    $('.inactive_cal').each(function(index) {
        var class_to_hide = $(this).attr('id');
        $('.' + class_to_hide).addClass('inactive_event');
    })
}

function toggle_categories(categoryId)
{
    $('#color_' + categoryId).toggleClass("inactive_color");
    $('#calendar_' + categoryId).toggleClass("inactive_cal");
    $('.calendar_' + categoryId).toggleClass("inactive_event");
    hide_tasks();
}

function set_task(taskId, typeTask)
{
    $.ajax(
        {
            data :
            {
                taskId : taskId,
                typeTask : typeTask
            },
            url : "/tasks/update_task/",
            type : "POST",
            success : function(newData)
            {
                // Reset The task
            }
        });
}

function init()
{
    $(".draggable").each(function(index) {
        $(this).draggable({
            revert: 'invalid',
            snap: '#cols',
            snapMode: 'inner',
            containment : '#cols'
        });
    });
    $(".droppable").droppable({
        drop: function( event, ui ) {
            ui.helper.css('top','');
            ui.helper.css('left','');
            $(this).find('.container_tasks').prepend(ui.helper);
            set_task(ui.draggable.attr('id'), $(this).attr('id'));
        }
    });

}

function display_date(idDiv)
{
    $("#" + idDiv).slideToggle("slow");
}

function display_details()
{
    $("#update_messager").slideToggle("slow");
}

function send_note(userId, taskId)
{
    alert($('textarea#input_note_' + taskId).val());
    $.ajax(
        {
            data :
            {
                userId : userId,
                note_text : $('textarea#input_note_' + taskId).val(),
                taskId: taskId
            },
            url : "/tasks/new_note/",
            type : "POST",
            success : function(newData)
            {
                $('textarea#input_note_' + taskId).val('');
                $(".submitdiv #" + taskId).after().html(newData);
            }
        });
}

function save_members(idMembersDiv, taskId)
{
    var members = [];
    $('#'+ idMembersDiv + " .member.select").each( function(){
        members.push($(this).attr('id'));
    });
    $.ajax(
        {
            data :
            {
                members : members,
                taskId: taskId
            },
            url : "/tasks/save_members/",
            type : "POST",
            success : function(newData)
            {
            }
        });
}

$(document).ready(function() {
    init();
    $( ".details_task_pop" ).dialog({ autoOpen: false });

    $( ".details_task_icone" ).click(function() {
        $("#pop_up_" + $(this).attr('id')).dialog( "open" );
    });

    $(".title_task").click(function(e){
        $(this).next().next().slideToggle("slow");
    });

    $("span.member").click(function(e){
        $(this).toggleClass('select');
    });

});