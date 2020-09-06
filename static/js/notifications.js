$(document).ready(function () {
    $(document).on('click', '.noti_asread', function (e){
      e.preventDefault();
      var btn = $(this);
      $.ajax({
          type: "POST",
          url: $(btn).attr('data-url'),
          dataType:"json",
          data: {
              csrfmiddlewaretoken: '{{ csrf_token }}'
          },
          success: function(data) {
            if(data.single_notification_marked){
              $(btn).closest('li').remove();
            }
          }
      });
    });

    $(document).on('click', '.noti_delete', function (e){
      e.preventDefault();
      var btn = $(this);
      $.ajax({
          type: "POST",
          url: $(btn).attr('data-url'),
          dataType:"json",
          data: {
              csrfmiddlewaretoken: '{{ csrf_token }}'
          },
          success: function(data) {
            if(data.single_notification_delete){
              $(btn).closest('li').remove();
            }
          }
      });
    });

  })