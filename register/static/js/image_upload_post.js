$(document).ready(function(){
    $("#show-image-upload-inputs").click(function(){
      $("#image-upload-div").toggle();
    });
  });


function open_input (input_id) {
    $("#" + input_id).trigger("click");
}

function ap_img_to_div(div_id,input_id) {
  $("#" + input_id).change(function () {
    $("#" + div_id).removeClass("add-image");
    $("#" + div_id).addClass("remove-image");
    var reader = new FileReader();
    reader.onload = function img_load_to_div(e) {
      var pic = '<img src="' + e.target.result + '" style="width:7em;height:7em;" class="upload_image_to_div">'
      $("#" + div_id).empty().append(pic).fadeIn(4000);
    }
    reader.readAsDataURL(this.files[0]);
  });
}
