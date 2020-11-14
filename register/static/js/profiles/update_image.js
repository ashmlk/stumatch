/*
$(document).ready(function(){$(document).on('click','#myCroppieBtn',function(){$('.edit-pro-all #id_image').click()})
var image_crop=$('#image_demo').croppie({viewport:{width:320,height:320,type:'circle'},boundary:{width:500,height:500,}});$(document).on('change','#id_image',function(){var reader=new FileReader();reader.onload=function(event){image_crop.croppie('bind',{url:event.target.result,})}
reader.readAsDataURL(this.files[0]);$('#uploadimageModal').modal('show')});var hid=$('#uidnameinput').val();var update_link='/update/profile/image/'+hid+'/'
$(document).on('click','.crop_image',function(e){var formData=new FormData();image_crop.croppie('result',{type:'blob',format:'png'}).then(function(blob){formData.append('cropped_image',blob);ajaxFormPost(formData,update_link)});$('#uploadimageModal').modal('hide')});function ajaxFormPost(formData,actionURL){$.ajax({url:actionURL,type:'POST',data:formData,cache:!1,async:!0,processData:!1,contentType:!1,timeout:5000,success:function(data){location.href=data.new_url},})}})
  */

$(document).ready(function (){
  var cropper;
  $(document).on('click', '#myCroppieBtn', function () {
      $('.edit-pro-all #id_image').click();
  })
  $(document).on('change','#id_image',function () {
      var input = document.getElementById('id_image');
      if (input.files && input.files[0]) {
          var reader = new FileReader();
          reader.onload = function (e) {
              if (cropper != null){
                  cropper.destroy();
              }           
              $('#id_image_preview').attr('src', e.target.result);
              initCropper();
          };
          reader.readAsDataURL(input.files[0]);
          setTimeout(initCropper, 1000);
      }
  });
  function initCropper() {
    $('#uploadimageModal').on('shown.bs.modal', function () {                
        if (cropper != null){
            cropper.destroy();
            cropper = null;
        }
        var image = document.getElementById('id_image_preview');
            cropper = new Cropper(image, {
            aspectRatio: 1 / 1,
        });
    }).on('hidden.bs.modal', function () {      
        if (cropper != null){
            cropper.destroy();
            cropper = null;
        }
    }).modal('show');
    $(document).on('click','.crop_image', function (e) {
        cropper.getCroppedCanvas().toBlob(function (blob) {
            var formData = new FormData();
            formData.append('cropped_image ', blob);
            var hid = $('#uidnameinput').val();
            var update_link = '/update/profile/image/' + hid + '/'
            $.ajax({
                url: update_link,
                type: 'POST',
                data: formData,
                cache: false,
                async: true,
                processData: false,
                contentType: false,
                timeout: 2000,
                success: function (data) {
                    location.href = data.new_url
                },
            });
        });
    });
  }
})