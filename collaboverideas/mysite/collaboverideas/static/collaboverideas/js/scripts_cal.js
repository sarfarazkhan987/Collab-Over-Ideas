$(document).ready(function() {
    $("#meet-save").click(function() {
       var curr=new Date();
         var mintime=curr.toTimeString().substring(0, 5)
var selectedDate = new Date($("#meet-hidden-date").val());

         if(selectedDate.getDate() == curr.getDate() &&
 selectedDate.getFullYear() == curr.getFullYear() && selectedDate.getMonth() == curr.getMonth()){
                     $("#meet-start-time").attr({
                                  // substitute your own
                            "min" : mintime
                         });
                     $("#meet-end-time").attr({
                           // substitute your own
                     "min" : $('#meet-start-time').val()
                     });
}
    //    console.log("save: " + $("#meet-subject").val() + ", " + $("#meet-notes").val() + ", " + $("#meet-location").val() + ", " + $("#meet-start-time").val() + ", " + $("#meet-end-time").val() + ", " + $("#meet-hidden-date").val());
        $.ajax({
            url: $("meta[name='manage_meetings_url']").attr("content"),
            data: {
                "action": "add_meeting",
                "meeting_id": $("#fresh-meeting").text(),
                "note": $("#meet-notes").val(),
                "location": $("#meet-location").val(),
                "start_time": $("#meet-start-time").val(),
                "end_time": $("#meet-end-time").val(),
                "invitee_ids": JSON.stringify($("#meet-members").val())
            },
            dataType: "json",
            success: function(data) {
                console.log(data);
            }
        });
        console.log($("#meet-members").val());
    });
    var date = new Date;
    var d = date.getDate();
    var m = date.getMonth();
    var y = date.getFullYear();
    var obj = {};
    $("#external-events div.external-event").each(function() {
        var eventObject = {
            title: $.trim($(this).text())
        };
        $(this).data("eventObject", eventObject);
        $(this).draggable({
            zIndex: 999,
            revert: true,
            revertDuration: 0
        });
    });
    var calendar = $("#calendar").fullCalendar({
        "timezone": "local",
        dayClick: function(date, jsEvent, view) {
            console.log("day-clicked");
            $("#meet-hidden-date").val($(this).attr("data-date"));
        },
        eventRender: function(event, element) {
            element.find(".fc-event-inner").bind("click", function(e) {
                if (e.which == 1) {
                    var event_id = $(this).closest(".fc-event").prop("id").split("_")[2];
                    $.ajax({
                        url: $("meta[name='manage_meetings_url']").attr("content"),
                        data: {
                            "action": "get_meeting",
                            "meeting_id": event_id
                        },
                        dataType: "json",
                        success: function(data) {
                            console.log(data);
                            $("#view-scheduler").text("Scheduler: " + data.meeting.scheduler_name);
                            $("#view-subject").text("Subject: " + data.meeting.subject);
                            if (data.meeting.note) {
                                $("#view-notes").text(data.meeting.note);
                            } else {
                                $("#view-notes").text("-");
                            }
                            if (data.meeting.start_time) {
                                $("#view-start-time").text(data.meeting.start_time);
                            } else {
                                $("#view-start-time").text("-");
                            }
                            if (data.meeting.end_time) {
                                $("#view-end-time").text(data.meeting.end_time);
                            } else {
                                $("#view-end-time").text("-");
                            }
                            if (data.meeting.location) {
                                $("#view-location").text(data.meeting.location);
                            } else {
                                $("#view-location").text("-");
                            }
                            var usersLength = data.meeting.invitees.length;
                            var members = [];
                            for (var i = 0; i < usersLength; i++) {
                                var user = data.meeting.invitees[i];
                                members.push(user.firstname);
                            }
                            $("#view-invitees").text(members.join(", "));
                            $("#viewModal").modal("show");
                        }
                    });
                }
            });
            element.append('<span id="del-' + event._id + '" class="fa fa-trash fa-md closeon" style="float: right; margin-top:1px;"></span>');
            element.append('<span id="edit-' + event._id + '" class="fa fa-pencil fa-md meet-edit" style="float: right; margin-top:1px; margin-right: 8px;"></span>');
            element.find(".closeon").click(function() {
                var th = $(this);
                bootbox.confirm("Are you sure you want to delete?", function(result) {
                    if (result) {
                        $.ajax({
                            url: $("meta[name='manage_meetings_url']").attr("content"),
                            data: {
                                "action": "delete_meeting",
                                "meeting_id": th.prop("id").split("-")[1]
                            },
                            dataType: "json",
                            success: function(data) {
                                console.log(data);
                            }
                        });
                        $("#calendar").fullCalendar("removeEvents", event._id);
                    }
                });
            });
            element.find(".meet-edit").click(function() {
                var event_id = $(this).prop("id").split("-")[1];
                $.ajax({
                    url: $("meta[name='manage_meetings_url']").attr("content"),
                    data: {
                        "action": "get_meeting",
                        "meeting_id": event_id
                    },
                    dataType: "json",
                    success: function(data) {
                        console.log(data);
                        $("#meet-scheduler").text("Scheduler: " + data.meeting.scheduler_name);
                        $("#edit-subject").val(data.meeting.subject);
                        $("#edit-notes").val(data.meeting.note);
                        $("#edit-start-time").val(data.meeting.start_time);
                        $("#edit-end-time").val(data.meeting.end_time);
                        $("#edit-location").val(data.meeting.location);
                        $("#edit-members").html("");
                        var usersLength = data.meeting.invitees.length;
                        for (var i = 0; i < usersLength; i++) {
                            var user = data.meeting.invitees[i];
                            if (user.user_flag == 1) {
                                $("#edit-members").append("" + '<option selected="selected" value="' + user.user_id + '">' + user.firstname + "</option>");
                            } else {
                                $("#edit-members").append("" + '<option value="' + user.user_id + '">' + user.firstname + "</option>");
                            }
                        }
                    }
                });
                $("#edit-subject").val("");
                $("#edit-notes").val("");
                $("#edit-start-time").val("");
                $("#edit-end-time").val("");
                $("#edit-location").val("");
                $("#edit-members option:selected").each(function() {
                    $(this).prop("selected", false);
                });
                $("#updateModal").modal("show");
                $("#update").off("click").click(function() {
                    console.log($("#edit-subject").val());
                    $.ajax({
                        url: $("meta[name='manage_meetings_url']").attr("content"),
                        data: {
                            "subject": $("#edit-subject").val(),
                            "action": "edit_meeting",
                            "meeting_id": event_id,
                            "note": $("#edit-notes").val(),
                            "location": $("#edit-location").val(),
                            "start_time": $("#edit-start-time").val(),
                            "end_time": $("#edit-end-time").val(),
                            "invitee_ids": JSON.stringify($("#edit-members").val())
                        },
                        dataType: "json",
                        success: function(data) {
                            console.log(data);
                            var evento = $("#calendar").fullCalendar("clientEvents", event_id)[0];
                            evento.title = $("#edit-subject").val();
                            $("#calendar").fullCalendar("updateEvent", evento);
                            $("#update").off("click");
                        }
                    });
                });
            });
        },
        eventAfterRender: function(event, element, view) {
            $(element).attr("id", "event_id_" + event._id);
        },
        header: {
            left: "title",
            center: "agendaDay,agendaWeek,month",
            right: "prev,next today"
        },
        editable: true,
        firstDay: 1,
        selectable: true,
        defaultView: "month",
        axisFormat: "h:mm",
        columnFormat: {
            month: "ddd",
            week: "ddd d",
            day: "dddd M/d",
            agendaDay: "dddd d"
        },
        titleFormat: {
            month: "MMMM yyyy",
            week: "MMMM yyyy",
            day: "MMMM yyyy"
        },
        allDaySlot: false,
        selectHelper: true,
        select: function(start, end, allDay) {
            var today = new Date();
            var selectedDate = new Date($("#meet-hidden-date").val());
/*
(selectedDate.getDate() != today.getDate() &&
 selectedDate.getFullYear() != today.getFullYear() && selectedDate.getMonth() != today.getMonth())
*/
             if(  selectedDate > today || (selectedDate.getDate() == today.getDate() &&
 selectedDate.getFullYear() == today.getFullYear() && selectedDate.getMonth() == today.getMonth()) ){
            bootbox.prompt({
                size: "small",
                title: "Enter Meeting Subject",
                callback: function(title) {
                    if (title ) {
                        $.ajax({
                            url: $("meta[name='manage_meetings_url']").attr("content"),
                            data: {
                                "action": "add_subject",
                                "subject": title,
                                "meeting_date": $("#meet-hidden-date").val()
                            },
                            dataType: "json",
                            success: function(data) {
                                console.log(data);
                                $("#fresh-meeting").text(data.id);
                                obj = {
                                    id: data.id,
                                    title: title,
                                    start: start,
                                    end: end,
                                    allDay: allDay
                                };
                                calendar.fullCalendar("renderEvent", obj, true);
                                calendar.fullCalendar("unselect");
                            }
                        });
                        $("#meet-subject").val(title);
                        $("#meet-notes").val("");
                        $("#meet-start-time").val("");
                        $("#meet-end-time").val("");
                        $("#meet-location").val("");
                        $("#meet-members option:selected").each(function() {
                            $(this).prop("selected", false);
                        });
                        $("#myModal").modal("show");
                    }
                }
            });
            }
            else {
bootbox.alert("You can't schedule an event in past date.");
                return;
            }
        },
        droppable: true,
        drop: function(date, allDay) {
            var originalEventObject = $(this).data("eventObject");
            var copiedEventObject = $.extend({}, originalEventObject);
            copiedEventObject.start = date;
            copiedEventObject.allDay = allDay;
            $("#calendar").fullCalendar("renderEvent", copiedEventObject, true);
            if ($("#drop-remove").is(":checked")) {
                $(this).remove();
            }
        }
    });
    $.ajax({
        url: $("meta[name='manage_meetings_url']").attr("content"),
        data: {
            "action": "get_meetings"
        },
        dataType: "json",
        success: function(data) {
            console.log(data);
            for (var i = 0, size = data.meetings.length; i < size; i++) {
                var item = data.meetings[i];
                var date = new Date(item.meeting_date);
                var d = date.getDate();
                var m = date.getMonth();
                var y = date.getFullYear();
                obj = {
                    id: item.meeting_id,
                    title: item.subject,
                    start: new Date(y, m, d)
                };
                calendar.fullCalendar("renderEvent", obj, true);
                calendar.fullCalendar("unselect");
            }
        }
    });
});