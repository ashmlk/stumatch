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
    var btn;
    $(document).on("click", '.btn-all-status', function (e) {
        btn = $(this)
        e.preventDefault();
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
    $('#modal-profile').on("submit",".block-user-form",function (e){
        e.preventDefault();
        e.stopImmediatePropagation();
        var form = new FormData(this);
        $.ajax({
            url: $(this).attr('data-url'),
            type: $(this).attr('method'),
            data: form,
            cache: false,
            processData: false,
            contentType: false,
            dataType: 'json',
            success: function(data){
                $('#modal-profile').modal('hide');
                $('body').removeClass('modal-open');
                $('.modal-backdrop').remove();                    
            }
        })
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