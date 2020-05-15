$(document).ready(function () {
    $('.like-count').css({"display":"none"});
    var lc = $(".input-like-count").val();
    $('.like-count-d').text(lc);
    $('.show-likes').on("click", function (e) {
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
    $('.show-comments').on("click", function (e) {
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