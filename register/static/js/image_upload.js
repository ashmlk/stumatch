$(document).ready(function(){
  $("#id_image").css({"margin-left":"-9999px"});
  $('input[type="file"]').attr("accept",".png, .jpg, .jpeg");
    $("#upload-image").click(function(){
      $("#id_file").click();  
    });
    $("#id_file").on("change", function () {
      var files_length = document.getElementById('id_file').files.length;
      if(files_length>4){
        alert('You can only upload a maximum of 4 images')
      }
      else {
        for(var i=0;i<files_length;i++){
          var pic = '<div class="d-flex justify-content-center flex-column ml-1">';
          pic += '<img id="' + i + '" src="' + URL.createObjectURL(event.target.files[i]) + '" style="width:7em;height:7em;" class="upload_image_to_div">';
          pic += '<button class="btn btn-sm btn-outline-danger mb-5 removeButton">Remove</button>';
          pic += '</div>';
          $("#uploaded").append(pic).fadeIn(4000);
          $(".removeButton").on("click", function(){
            $(this).closest('div').remove();
            document.getElementById("id_image").value = "";
         });
        }
      }
    }) 
  });




