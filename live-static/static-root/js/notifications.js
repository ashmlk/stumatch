$(document).ready(function () {
  function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
    });

    $(document).on('click', '.noti_asread', function (e){
      e.preventDefault();
      var btn = $(this);
      $.ajax({
          type: "POST",
          url: $(btn).attr('data-url'),
          dataType:"json",
          data: {
            csrfmiddlewaretoken: getCookie('csrftoken')
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
            csrfmiddlewaretoken: getCookie('csrftoken')
          },
          success: function(data) {
            if(data.single_notification_delete){
              $(btn).closest('li').remove();
            }
          }
      });
    });

    $(document).on('click', '.accept-reject-btn', function (){
      $(this).closest('.notifications-item').find('.noti_delete').click();
    })

  })