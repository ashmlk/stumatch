$(document).ready(function () {
  
    $(document).on('click', '#myCroppieBtn', function () {
      $('.edit-pro-all #id_image').click();
    })
    
    var image_crop = $('#image_demo').croppie({
      viewport: {
        width: 320,
        height: 320,
        type: 'circle'
      },
      boundary: {
        width: 500, 
        height: 500,
      }
    });
    /// catching up the cover_image change event and binding the image into my croppie. Then show the modal.
    $(document).on('change','#id_image', function () {
      var reader = new FileReader();
      reader.onload = function (event) {
        image_crop.croppie('bind', {
          url: event.target.result,
        });
      }
      reader.readAsDataURL(this.files[0]);
      $('#uploadimageModal').modal('show');
    });
    var hid = $('#uidnameinput').val();
    var update_link = '/update/profile/image/' + hid + '/'
    $(document).on('click','.crop_image', function (e) {
      var formData = new FormData();
      image_crop.croppie('result', { type: 'blob', format: 'png' }).then(function (blob) {
        formData.append('cropped_image', blob);
        ajaxFormPost(formData, update_link); /// Calling my ajax function with my blob data passed to it
      });
      $('#uploadimageModal').modal('hide');
    });
    /// Ajax Function
    function ajaxFormPost(formData, actionURL) {
      $.ajax({
        url: actionURL,
        type: 'POST',
        data: formData,
        cache: false,
        async: true,
        processData: false,
        contentType: false,
        timeout: 5000,
        success: function (data) {
            location.href = data.new_url
        },
      });
    }
  })