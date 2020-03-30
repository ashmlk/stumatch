$(document).ready(function(){

    $(".js-upload-images").click(function () {
      $("#fileupload").click();
    });
  
    $("#fileupload").fileupload({
      change : function (e, data) {
        if(data.files.length >= 4){
            alert("Sorry, you can only upload up to 4 images")
            return false;
        }
      },
      dataType: 'json',
      sequentialUploads: true,  
      start: function (e)  { 
        $("#modal-progress").show();
      },
      stop: function (e) {  
        $("#modal-progress").hide();
      },
      progressall: function (e, data) {  
        var progress = parseInt(data.loaded / data.total * 100, 10);
        var strProgress = progress + "%";
        $(".progress-bar").css({"width": strProgress});
        $(".progress-bar").text(strProgress);
      },
      done: function (e, data) {
        if (data.result.is_valid) {
          $("#image_list tbody").prepend(
            "<tr><td><a href='" + data.result.url + "'>" + data.result.name + "</a></td></tr>"
          )
        }
      }
    });
});