$(function() {
  var kanbanCol = $(".panel-body");
  kanbanCol.css("max-height", window.innerHeight - 150 + "px");
  var kanbanColCount = parseInt(kanbanCol.length);
  $(".container-fluid").css("min-width", kanbanColCount * 350 + "px");
  $("#add_label").click(function() {
    var text = document.getElementById("lbl_data").value.trim();
    $("#lbl_data").val("");
    if (text == "") {
      return;
    }
    var x = document.getElementById("tsk_label");
    var option = document.createElement("option");
    option.text = text;
    $.ajax({url:$("meta[name='manage_tasks_url']").attr("content"), data:{"action":"add_label", "name":text}, dataType:"json", success:function(data) {
      console.log(data);
      if (data.added == 0) {
        return;
      }
      option.setAttribute("value", "label-" + data.added);
      x.add(option);
    }});
  });

    $("#edit-add_label").click(function() {
    var text = document.getElementById("edit-lbl_data").value.trim();
    $("#edit-lbl_data").val("");
    if (text == "") {
    console.log('empty')
      return;
    }
    var x = document.getElementById("edit-tsk_label");
    var option = document.createElement("option");
    option.text = text;
    $.ajax({url:$("meta[name='manage_tasks_url']").attr("content"), data:{"action":"add_label", "name":text}, dataType:"json", success:function(data) {
      console.log(data);
      if (data.added == 0) {
        return;
      }
      option.setAttribute("value", "label-" + data.added);
      x.add(option);
    }});
  });
  draggableInit();
  $(".panel-heading").click(function() {
    var $panelBody = $(this).parent().children(".panel-body");
    $panelBody.slideToggle();
  });
  $(document).on("click", ".del_task", function(event) {
    var th = $(this);
    bootbox.confirm("Are you sure you want to delete?", function(result) {
      if (result) {
        th.closest("article").remove();
        var task_id = th.closest("article").attr("id").split("-")[1];
        $.ajax({url:$("meta[name='manage_tasks_url']").attr("content"), data:{"action":"delete", "task_id":task_id}, dataType:"json", success:function(data) {
          console.log(data);
        }});
      }
    });
  });
  $(".addtask").click(function() {
    $("#add-list-id").val($(this).closest(".panel").attr("id").split("-")[1]);
    $("#myModal").modal("show");
  });
  $(document).on("click", ".edit_task", function(event) {
    $("#edit-add-list-id").val($(this).closest(".panel").attr("id").split("-")[1]);
    $("#edit-task-id").val($(this).closest("article").attr("id").split("-")[1]);
    $("#edit-task-modal").modal("show");
    var task_id = $(this).closest("article").attr("id").split("-")[1];
    $.ajax({url:$("meta[name='manage_tasks_url']").attr("content"), data:{"action":"get_task", "task_id":task_id}, dataType:"json", success:function(data) {
      console.log(data);
      $("#edit-task-title").val(data.task.task_name);
      $("#edit-task-desc").val(data.task.task_description);
      $("#edit-d-date").val(data.task.due_date);
      $("#edit-task-members").html("");
      $("#edit-tsk_label").html("");
      var usersLength = data.task.users_list.length;
      for (var i = 0; i < usersLength; i++) {
        var user = data.task.users_list[i];
        if (user.user_flag == 1) {
          $("#edit-task-members").append("" + '<option selected="selected" value="' + user.user_id + '">' + user.firstname + "</option>");
        } else {
          $("#edit-task-members").append("" + '<option value="' + user.user_id + '">' + user.firstname + "</option>");
        }
      }
      var labelsLength = data.task.labels_list.length;
      for (var i = 0; i < labelsLength; i++) {
        var label = data.task.labels_list[i];
        if (label.label_flag == 1) {
          $("#edit-tsk_label").append("" + '<option selected="selected" value="' + label.label_id + '">' + label.label_name + "</option>");
        } else {
          $("#edit-tsk_label").append("" + '<option value="' + label.label_id + '">' + label.label_name + "</option>");
        }
      }
    }});
  });
  $("#d-date").click(function() {
    var members = [];
  });
  $("#task-save").click(function() {
    var title = document.getElementById("task-title").value.trim();
    var desc = document.getElementById("task-desc").value.trim();
    var members = [];
    $("#task-members option:selected").each(function() {
      var $this = $(this);
      if ($this.length) {
        var selText = $this.text();
        members.push(selText);
      }
    });
    var labels = [];
    $("#tsk_label option:selected").each(function() {
      var $this = $(this);
      if ($this.length) {
        var selText = $this.text();
        labels.push(selText);
      }
    });
    var duedate = $("#d-date").val().trim();
    var monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    var d = new Date(duedate);
    var printDate = monthNames[d.getMonth()] + " " + d.getDate() + "," + " " + d.getFullYear();
    if (title == "" || desc == "" || members.length == 0 || labels.length == 0 || duedate == "") {
      return;
    }
    $.ajax({url:$("meta[name='manage_tasks_url']").attr("content"), data:{"action":"add_task", "list_id":$("#add-list-id").val(), "task_name":title, "task_description":desc, "due_date":duedate, "user_ids":JSON.stringify($("#task-members").val()), "label_ids":JSON.stringify($("#tsk_label").val())}, dataType:"json", success:function(data) {
      console.log(data);
      var id_for_below = $("#list-" + $("#add-list-id").val()).find(".kanban-centered").attr("id");
      document.getElementById(id_for_below).innerHTML += "<article class='kanban-entry grab' id='task-" + data.added + "' draggable='true'>" + " <div class='kanban-entry-inner'>" + "<div class='kanban-label'>" + '<i  class="fa fa-trash fake-link del_task" style="float: right;"></i>' + '<i class="fa fa-pencil fake-link edit_task" style="float: right; margin-right: 7px;"></i>' + "<h2><strong>" + title + "</strong></h2>" + '<p><span class="card-desc">' + desc + "</span></p>" + '<p><strong>Members</strong><br><span class="card-members">' + 
      members.join(", ") + "</span></p>" + '<p><strong>Labels</strong><br><span class="card-labels">' + labels.join(", ") + "</span></p>" + '<p><strong>Due Date</strong><br><span class="card-date">' + printDate + "</span></p>" + "</div>" + "</div>" + "</article>";
      $("#myModal").modal("hide");
      $("#d-date").val("");
      $("#task-title").val("");
      $("#task-desc").val("");
      $("#d-date").val("");
    }});
    $("#task-members option:selected").each(function() {
      $(this).prop("selected", false);
    });
    $("#tsk_label option:selected").each(function() {
      $(this).prop("selected", false);
    });
  });
  $("#edit-task-save").click(function(e) {
    e.preventDefault();
    var title = document.getElementById("edit-task-title").value.trim();
    var desc = document.getElementById("edit-task-desc").value.trim();
    var members = [];
    $("#edit-task-members option:selected").each(function() {
      var $this = $(this);
      if ($this.length) {
        var selText = $this.text();
        members.push(selText);
      }
    });
    var labels = [];
    $("#edit-tsk_label option:selected").each(function() {
      var $this = $(this);
      if ($this.length) {
        var selText = $this.text();
        labels.push(selText);
      }
    });
    var duedate = $("#edit-d-date").val().trim();
    console.log($("#task-" + $("#edit-task-id").val()));
    if (title == "" || desc == "" || members.length == 0 || labels.length == 0 || duedate == "") {
      return;
    }
    $.ajax({url:$("meta[name='manage_tasks_url']").attr("content"), data:{"action":"edit_task", "task_id":$("#edit-task-id").val(), "task_name":title, "task_description":desc, "due_date":duedate, "user_ids":JSON.stringify($("#edit-task-members").val()), "label_ids":JSON.stringify($("#edit-tsk_label").val())}, dataType:"json", success:function(data) {
      console.log(data);
      $("#edit-task-modal").modal("hide");
      var art = $("#task-" + $("#edit-task-id").val());
      art.find("h2 strong").text(title);
      art.find(".card-desc").text(desc);
      art.find(".card-members").text(members.join(", "));
      art.find(".card-labels").text(labels.join(", "));
      var monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        var d = new Date(duedate);
        var printDate = monthNames[d.getMonth()] + " " + d.getDate() + "," + " " + d.getFullYear();
      art.find(".card-date").text(printDate);
    }});
  });
});
function draggableInit() {
  var sourceId;
  $(document).on("dragstart", "[draggable=true]", function(event) {
    sourceId = $(this).parent().attr("id");
    event.originalEvent.dataTransfer.setData("text/plain", event.target.getAttribute("id"));
    console.log("done");
  });
  $(document).on("dragover", ".panel-body", function(event) {
    event.preventDefault();
  });
  $(document).on("drop", ".panel-body", function(event) {
    var children = $(this).children();
    var targetId = children.attr("id");
    if (sourceId != targetId) {
      var elementId = event.originalEvent.dataTransfer.getData("text/plain");
      var list_id = $(this).parent().attr("id").split("-")[1];
      $.ajax({url:$("meta[name='manage_tasks_url']").attr("content"), data:{"action":"reassign", "list_id":list_id, "task_id":event.originalEvent.dataTransfer.getData("text/plain").split("-")[1]}, dataType:"json", success:function(data) {
        console.log(data);
      }});
      console.log($(this).parent().attr("id"));
      $("#processing-modal").modal("toggle");
      setTimeout(function() {
        var element = document.getElementById(elementId);
        children.prepend(element);
        $("#processing-modal").modal("toggle");
      }, 1000);
    }
    event.preventDefault();
  });
}
;