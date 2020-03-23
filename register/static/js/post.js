$(document).ready(function(){
    $(function () {
        $(".create-post-btn").click(function () {
          $.ajax({
            url: '/home/post/create',
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
              $("#modal-post").modal("show");
            },
            success: function (data) {
              $("#modal-post .modal-content").html(data.html_form);
            }
          });
        }); 
    });

    $("#modal-post").on("submit", ". post-create-form", function () {
        var form = $(this);
        $.ajax({
          url: form.attr("action"),
          data: form.serialize(),
          type: form.attr("method"),
          dataType: 'json',
          success: function (data) {
            if (data.form_is_valid) {
                $('#post-list div').html(data.posts);
                $('#modal-post').modal('hide');
            }
            else {
              $("#modal-post .modal-content").html(data.html_form);
            }
          }
        });
        return false;
      });
});