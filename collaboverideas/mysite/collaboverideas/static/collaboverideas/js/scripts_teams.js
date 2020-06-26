$(document).ready(function() {
  $(".accept-invite").click(function() {
    var team_id = $(this).attr("id").split("-")[1];
    console.log(team_id);
    $.ajax({url:$("meta[name='join_team_url']").attr("content"), data:{"team_id":team_id}, dataType:"json", success:function(data) {
      console.log(data);
    }});
    var team_name = $(this).closest("div").text().trim();
    var new_item = $('<a href="?teamid=' + team_id + '" class="list-group-item">' + team_name + "</a>").hide();
    $("#available-teams").append(new_item);
    new_item.show("normal");
    $(this).closest(".invite").hide("normal");
    var curr_count = parseInt($("#count-invites").text());
    var new_count = curr_count - 1;
    if (new_count == 0) {
      $("#count-invites").hide();
    }
    $("#count-invites").text(new_count);
  });
  $(".reject-invite").click(function() {
    var team_id = $(this).attr("id").split("-")[1];
    $.ajax({url:$("meta[name='join_team_url']").attr("content"), data:{"action":"reject_team", "team_id":team_id}, dataType:"json", success:function(data) {
      console.log(data);
    }});
    $(this).closest(".invite").hide("normal");
    var curr_count = parseInt($("#count-invites").text());
    var new_count = curr_count - 1;
    if (new_count == 0) {
      $("#count-invites").hide();
    }
    $("#count-invites").text(new_count);
  });
  $("#add-member").click(function(e) {
    e.preventDefault();
    var members = [];
    $("#members option:selected").each(function() {
      var $this = $(this);
      if ($this.length) {
        var selText = $this.text();
        members.push(selText);
      }
    });
    var emails = [];
    $(".invite-email").each(function() {
      var email = $(this).val();
      if (email != "") {
        emails.push(email);
      }
    });
    console.log(emails);
    var form = $("#add-member-form");
    $("#emails-string").val(JSON.stringify(emails));
    $("#members-string").val(JSON.stringify(members));
    form.submit();
  });
});
$(function() {
  $(document).on("focus", "div.form-group-options div.input-group-option:last-child input", function() {
    var sInputGroupHtml = $(this).parent().html();
    var sInputGroupClasses = $(this).parent().attr("class");
    $(this).parent().parent().append('<div class="' + sInputGroupClasses + '">' + sInputGroupHtml + "</div>");
  });
  $(document).on("click", "div.form-group-options .input-group-addon-remove", function() {
    $(this).parent().remove();
  });
});
$(function() {
  var values = new Array;
  $(document).on("change", ".form-group-multiple-selects .input-group-multiple-select:last-child select", function() {
    var selectsLength = $(this).parent().parent().find(".input-group-multiple-select select").length;
    var optionsLength = $(this).find("option").length - 1;
    if (selectsLength < optionsLength) {
      var sInputGroupHtml = $(this).parent().html();
      var sInputGroupClasses = $(this).parent().attr("class");
      $(this).parent().parent().append('<div class="' + sInputGroupClasses + '">' + sInputGroupHtml + "</div>");
    }
    updateValues($(this).parent().parent());
  });
  $(document).on("change", ".form-group-multiple-selects .input-group-multiple-select:not(:last-child) select", function() {
    updateValues($(this).parent().parent());
  });
  $(document).on("click", ".input-group-addon-remove", function() {
    var oSelectContainer = $(this).parent().parent();
    $(this).parent().remove();
    updateValues(oSelectContainer);
  });
  function updateValues(oSelectContainer) {
    values = new Array;
    $(oSelectContainer).find(".input-group-multiple-select select").each(function() {
      var value = $(this).val();
      if (value != 0 && value != "") {
        values.push(value);
      }
    });
    $(oSelectContainer).find(".input-group-multiple-select select").find("option").each(function() {
      var optionValue = $(this).val();
      var selectValue = $(this).parent().val();
      if (in_array(optionValue, values) != -1 && selectValue != optionValue) {
        $(this).attr("disabled", "disabled");
      } else {
        $(this).removeAttr("disabled");
      }
    });
  }
  function in_array(needle, haystack) {
    var found = 0;
    for (var i = 0, length = haystack.length; i < length; i++) {
      if (haystack[i] == needle) {
        return i;
      }
      found++;
    }
    return -1;
  }
  $(".form-group-multiple-selects").each(function(i, e) {
    updateValues(e);
  });
});