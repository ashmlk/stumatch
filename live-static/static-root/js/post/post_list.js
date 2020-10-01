$(document).ready(function () {
    $('.post-ctr').on("click",'.show-likes', function (e) {
      e.preventDefault();
      $.ajax({
            url: $(this).data("url"),
            type: 'get',
            dataType: 'json',
            success: function(data) {
              $('#modal-post-list .modal-content').html(data.html);
              $('#modal-post-list').modal('show');
            }
      });
    });
    $('.post-ctr').on("click", '.show-comments',function (e) {
      e.preventDefault();
      $.ajax({
            url: $(this).data("url"),
            type: 'get',
            dataType: 'json',
            success: function(data) {
              $('#modal-post-list .modal-content').html(data.html);
              $('#modal-post-list').modal('show');
            }
      });
    });
  });