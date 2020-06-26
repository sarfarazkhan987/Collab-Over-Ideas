function fileSelected() {
  var file = document.getElementById("js-upload-files").files[0];
  console.log(file);
  document.getElementById("fileName").value = file.name;
  document.getElementById("fileType").value = file.type;
  $("#fileNameLabel").text(file.name);
}
function uploadFile() {
  var fd = new FormData;
  fd.append("js-upload-files", document.getElementById("js-upload-files").files[0]);
  var xhr = new XMLHttpRequest;
  xhr.upload.addEventListener("progress", uploadProgress, false);
  xhr.addEventListener("load", uploadComplete, false);
  xhr.addEventListener("error", uploadFailed, false);
  xhr.addEventListener("abort", uploadCanceled, false);
  xhr.send(fd);
}
function uploadProgress(evt) {
  if (evt.lengthComputable) {
    var percentComplete = Math.round(evt.loaded * 100 / evt.total);
    document.getElementById("progressNumber").innerHTML = percentComplete.toString() + "%";
  } else {
    document.getElementById("progressNumber").innerHTML = "unable to compute";
  }
}
function uploadComplete(evt) {
  alert(evt.target.responseText);
}
function uploadFailed(evt) {
  alert("There was an error attempting to upload the file.");
}
function uploadCanceled(evt) {
  alert("The upload has been canceled by the user or the browser dropped the connection.");
}
function downloadFile(urlToSend) {
  var req = new XMLHttpRequest;
  req.open("GET", urlToSend, true);
  req.responseType = "blob";
  req.onload = function(event) {
    var blob = req.response;
    var fileName = req.getResponseHeader("fileName");
    var link = document.createElement("a");
    link.href = window.URL.createObjectURL(blob);
    link.download = fileName;
    link.click();
  };
  req.send();
}
$(document).ready(function() {
  console.log("file ready");
  $(".delete-file").click(function(e) {
    e.preventDefault();
    var th = $(this);
    bootbox.confirm("Are you sure you want to delete?", function(result) {
      if (result) {
        th.closest("div").remove();
        var file_id = th.attr("id").split("-");
        $.ajax({url:$("meta[name='file_delete_url']").attr("content"), data:{"fid":file_id[2]}, dataType:"json", success:function(data) {
          console.log(data);
        }, complete:function() {
        }});
      }
    });
  });
});