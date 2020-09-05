$(document).ready(function (e) {
    e.preventDefault();
    var infinite = new Waypoint.Infinite({
        element: $('.infinite-container')[0],
        onBeforePageLoad: function () {
            $('.loading').show();
        },
        onAfterPageLoad: function ($items) {
            $('.loading').hide();
        }
    });
})

$(document).ready(function () {
    var btn;
    $(document).on("click", '.accept-reject-btn', function (e) {
        btn = $(this)
        e.preventDefault();
        e.stopImmediatePropagation();
        $.ajax({
            type: "POST",
            url: $(this).attr("data-url"),
            dataType: 'json',
            data: $(this).closest('form').serialize(),
            success: function (data) {
                $(btn).closest(".friend-status-ctr").html(data.html_form);
            },
            error: function (rs, e) {
                console.log(rs.responeText);
            },
        });
    });
})

$(document).ready(function () {
    $(document).on("submit", '.btn-all-status', function (e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        var frst = $(this)
        var form = $(this).serialize();
        $.ajax({
            type: "POST",
            url: $(this).attr("data-url"),
            dataType: 'json',
            data: form,
            success: function (data) {
                $(frst).closest(".friend-status-ctr").html(data.html_form);
            },
            error: function (rs, e) {
                console.log(rs.responeText);
            },
        });
    });

    ('mngpl').on('click', function () {
        window.location = $(this).find('a').attr('href');
    })
})
$(document).ready(function () {

  $('.pro-menu-link').on('click', function () {
      window.location = $(this).attr('data-url');
  })
  $('.pro-link-goto').on('click', function () {
      if(!($(this).hasClass('form-link-goto'))){
        window.location = $(this).attr('data-url');
      }
      else if($(this).hasClass('form-link-goto')){
          $(this).submit();
      }

  })
  $('.pro-link-goto-active').on('click', function () {
    if(!($(this).hasClass('form-link-goto'))){
        window.location = $(this).attr('data-url');
      }
      else if($(this).hasClass('form-link-goto')){
          $(this).submit();
      }
  })
})

// blocking user modal and form page
$(document).ready(function (e) {
    $(document).on("click",".block-user-btn", function (e) {
        e.stopImmediatePropagation();
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType:'json',
            beforeSend: function(){
                $('#modal-profile').modal('show');
            },
            success: function(data){
                $('#modal-profile .modal-content').html(data.html_form);
            }
        });
    });
});

$(document).ready(function () {

    $('.pro-menu-link').on('click', function () {
        window.location = $(this).attr('data-url');
    })
    $('.pro-link-goto').on('click', function () {
          window.location = $(this).attr('data-url');
    })
    $('.pro-link-goto-active').on('click', function () {
          window.location = $(this).attr('data-url');
    })
})