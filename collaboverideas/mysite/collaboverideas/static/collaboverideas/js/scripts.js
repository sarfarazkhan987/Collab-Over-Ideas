$(function() {
  $("#usernameId").change(function() {
    var reg_form = $(this).closest("form");
    $("#loader").show();
    $("#existsError").text("");
    $.ajax({url:reg_form.attr("data-validate-username-url"), data:reg_form.serialize(), dataType:"json", success:function(data) {
      $("#loader").hide();
      console.log(data.is_taken);
      if (data.is_taken) {
        $("#existsError").removeClass("text-active");
        $("#existsError").addClass("text-danger");
        $("#existsError").text(data.error_message);
        $("#usernameId")[0].setCustomValidity("Username is not available");
      } else {
        $("#existsError").removeClass("text-danger");
        $("#existsError").addClass("text-success");
        $("#existsError").text("Username is available");
        $("#usernameId")[0].setCustomValidity("");
      }
    }});
  });
  $("#login-form-link").click(function(e) {
    $("#login-form").delay(100).fadeIn(100);
    $("#register-form").fadeOut(100);
    $("#register-form-link").removeClass("active");
    $(this).addClass("active");
    e.preventDefault();
  });
  $("#register-form-link").click(function(e) {
    $("#register-form").delay(100).fadeIn(100);
    $("#login-form").fadeOut(100);
    $("#login-form-link").removeClass("active");
    $(this).addClass("active");
    e.preventDefault();
  });
});