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

function display_details()
{
    $("#update_messager").slideToggle("slow");
}

$(document).ready(function() {
    init();
    $(".header_task").click(function(e){
        $(this).next().slideToggle("slow");
    });
});