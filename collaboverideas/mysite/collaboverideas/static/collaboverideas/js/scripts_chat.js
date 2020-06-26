function notifyMe(title, message) {
  if (Notification.permission !== "granted") {
    Notification.requestPermission();
  } else {
    var notification = new Notification(title, {icon:"../../../static/collaboverideas/images/chat.png", body:message, isClickable:false});
    setTimeout(notification.close.bind(notification), 4000);
  }
}
function check_messages() {
  $.ajax({url:$("meta[name='check_new_messages_url']").attr("content"), data:null, dataType:"json", success:function(data) {
    var list = data[data.length - 1];
    if (list.length != 0 && !$("#msg_box_group").is(":visible")) {
      var cspan = $("#count-group").text();
      if (cspan == "") {
        $("#count-group").text(list.length);
        if (list.length != 1) {
          notifyMe("New Message", "You have received " + list.length + " new team messages");
        } else {
          notifyMe("New Message", "You have received a new team message");
        }
        Cookies.set("count-group", list.length);
      } else {
        var sum = parseInt(cspan) + list.length;
        if (sum != 1) {
          notifyMe("New Message", "You have received " + sum + " new team messages");
        } else {
          notifyMe("New Message", "You have received a new team message");
        }
        Cookies.set("count-group", sum);
        $("#count-group").text("" + sum);
      }
    }
    for (var i = 0, size = list.length; i < size; i++) {
      var item = list[i];
      $('<div class="msg_a"><span class="text-primary"><b>' + item.firstname + "</b></span><br>" + item.message_body + "</div>").insertBefore("#msg_body_group > .msg_push");
    }
    $("#msg_body_group").scrollTop($("#msg_body_group")[0].scrollHeight);
    var p_list = data[0];
    var total = 0;
    var open = true;
    console.log('len: ' + p_list.length)
    for (var i = 0; i < p_list.length; i++) {
      var item = p_list[i];
      console.log('here');
      if (!$("#msg_box_" + item.sender).is(":visible")) {
        open = false;
        total += item.messages.length;
        var cspan = $("#count-" + item.sender).text();
        if (cspan == "") {
          $("#count-" + item.sender).text(item.messages.length);
          Cookies.set("count-" + item.sender, item.messages.length);
        } else {
          var sum = parseInt(cspan) + item.messages.length;
          Cookies.set("count-" + item.sender, sum);
          $("#count-" + item.sender).text("" + sum);
        }
      }
      for (var j = 0, size = item.messages.length; j < size; j++) {
        msg = item.messages[j];
        $('<div class="msg_a">' + msg + "</div>").insertBefore("#msg_body_" + item.sender + " > .msg_push");
        if ($("#msg_box_" + item.sender).is(":visible")) {
          $("#msg_body_" + item.sender).scrollTop($("#msg_body_" + item.sender)[0].scrollHeight);
        }
      }
    }
    if (!open && total != 0) {
    console.log(total);
      if (total != 1) {
        notifyMe("New Message", "You have received " + total + " new private messages");
//           notifyMe("New Message", "You have received a new private message");
      } else {
        notifyMe("New Message", "You have received a new private message");
      }
    }
  }});
}
$(document).ready(function() {
  check_messages();
  if (Notification.permission !== "granted") {
    Notification.requestPermission();
  }
  $("#count-group").text(Cookies.get("count-group"));
  $("#myProfileDrop").click(function() {
    console.log("open");
    $(this).closest(".dropdown").addClass("open");
    $("#myTeamDrop").closest(".dropdown").removeClass("open");
    return false;
  });
  $("#myTeamDrop").click(function() {
    $(this).closest(".dropdown").addClass("open");
    $("#myProfileDrop").closest(".dropdown").removeClass("open");
    return false;
  });
  setInterval(check_messages, 3000);
  $(".msg_head").not("#msg_head_group").click(function() {
    $("#msg_wrap_" + $(this).attr("id").split("_")[2]).slideToggle("slow");
  });
  $("#msg_head_group").click(function() {
    $("#msg_wrap_group").slideToggle("slow");
  });
  $(".close").click(function() {
    flag = true;
    group_flag = true;
    $(this).closest(".msg_box").hide("fast");
  });
  $(".user").click(function() {
    var chat_with = $(this).attr("id");
    Cookies.remove("count-" + chat_with);
    $("#count-" + chat_with).text("");
    $(".msg_wrap").not($("#msg_wrap_" + chat_with)).not($("#msg_wrap_group")).each(function() {
      $(this).hide();
    });
    $(".msg_box").not($("#msg_box_" + chat_with)).not($("#msg_box_group")).each(function() {
      $(this).hide();
    });
    $("#msg_wrap_" + chat_with).show("normal");
    $("#msg_box_" + chat_with).show("normal");
    $("#msg_body_" + chat_with).scrollTop($("#msg_body_" + chat_with)[0].scrollHeight);
  });
  $("#group_chat_button").click(function() {
    Cookies.remove("count-group");
    $("#count-group").text("");
    $("#msg_wrap_group").show("normal");
    $("#msg_box_group").show("normal");
    $("#msg_body_group").scrollTop($("#msg_body_group")[0].scrollHeight);
  });
  $("#chat_area_group").keypress(function(e) {
    if (e.keyCode == 13) {
      e.preventDefault();
      var msg = $(this).val();
      if (msg != "") {
        $('<div class="msg_b">' + msg + "</div>").insertBefore("#msg_body_group > .msg_push");
        $.ajax({url:$("meta[name='send_url']").attr("content"), data:{"type":"group", "message_body":msg}, dataType:"json", success:function(data) {
          console.log(data);
        }});
      }
      $(this).val("");
      $("#msg_body_group").scrollTop($("#msg_body_group")[0].scrollHeight);
    }
  });
  $(".chat_area").keypress(function(e) {
    if (e.keyCode == 13) {
      e.preventDefault();
      var msg = $(this).val();
      if (msg != "") {
        chat_with = $(this).attr("id").split("_")[2];
        $('<div class="msg_b">' + msg + "</div>").insertBefore("#msg_body_" + chat_with + " > .msg_push");
        $.ajax({url:$("meta[name='send_url']").attr("content"), data:{"type":"private", "recipient":chat_with, "message_body":msg}, dataType:"json", success:function(data) {
          console.log(data);
        }});
      }
      $(this).val("");
      $("#msg_body_" + chat_with).scrollTop($("#msg_body_" + chat_with)[0].scrollHeight);
    }
  });
});