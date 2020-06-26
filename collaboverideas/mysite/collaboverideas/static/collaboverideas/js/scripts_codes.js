$(function() {
  $(".list-group-item > .show-menu").on("click", function(event) {
    event.preventDefault();
    $(this).closest("li").toggleClass("open");
  });
});
$(document).ready(function() {
  $("#editing-lang").change(function() {
    var editor = ace.edit("editor");
    editor.getSession().setMode("ace/mode/" + this.value);
    var reditor = ace.edit("read_editor");
    reditor.setOptions({readOnly:true, highlightActiveLine:false, highlightGutterLine:false});
    reditor.renderer.$cursorLayer.element.style.opacity = 0;
    reditor.textInput.getElement().disabled = true;
  });
  var textarea = $('textarea[name="code-content"]');
  editor.getSession().on("change", function() {
    textarea.val(editor.getSession().getValue());
  });
  $(".view-code").click(function(e) {
    e.preventDefault();
    var code_id = $(this).attr("id").split("-");
    $.ajax({url:$("meta[name='view_code_url']").attr("content"), data:{"code_id":code_id[1]}, dataType:"json", success:function(data) {
      var editor = ace.edit("read_editor");
      editor.setValue(data.code, -1);
      $("#code-title").text(data.name);
      $("#code-author").text("Author: " + data.author);
      editor.getSession().setMode("ace/mode/" + data.language.toLowerCase());
    }, complete:function() {
    }});
  });
  $(".edit-code").click(function(e) {
    e.preventDefault();
    var code_id = $(this).attr("id").split("-");
    $("#code-id-edit").val(code_id[1]);
    $.ajax({url:$("meta[name='view_code_url']").attr("content"), data:{"code_id":code_id[1]}, dataType:"json", success:function(data) {
      var editor = ace.edit("editor");
      editor.setValue(data.code, -1);
      $("#code-name").val(data.name);
      editor.getSession().setMode("ace/mode/" + data.language.toLowerCase());
      $('#editing-lang option[value="' + data.language.toLowerCase() + '"]').prop("selected", true);
    }, complete:function() {
    }});
  });
  $("#add-new-code").click(function(e) {
    var code_id = $(this).attr("id").split("-");
    var editor = ace.edit("editor");
    editor.setValue("", -1);
    $("#code-id-edit").val("");
    $("#code-name").val("");
    editor.getSession().setMode("ace/mode/" + "java");
  });
  $(".delete-code").click(function(e) {
    e.preventDefault();
    var th = $(this);
    bootbox.confirm("Are you sure you want to delete?", function(result) {
      if (result) {
        th.closest(".panel-white").remove();
        var code_id = th.attr("id").split("-");
        $.ajax({url:$("meta[name='delete_code_url']").attr("content"), data:{"codeid":code_id[1]}, dataType:"json", success:function(data) {
        }, complete:function() {
        }});
      }
    });
  });
});