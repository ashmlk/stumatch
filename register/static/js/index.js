$(document).ready(function () {  

    var path = window.location.href;
    var p = window.location.pathname;

    $('#add-tagstp').click(function() {
      $('#div_id_tags').show();
    })

    $('.dropdown').each(function () {
      $(this).find("button").addClass('no-border')
    })

    $('#_pol3 a').each(function() {
      if (this.href === path) {
      $(this).closest('div').addClass('menu-link-active');
      }
    });

    $(".menu-link").on("click", function() {
      location.href = $(this).children("a").attr("href");
    });

    $('.mnpglk').on('click', function () {
      window.location = $(this).attr('data-url');
      return false;
    })
    
    $('.mnpglk').each(function() {
      var l = $(this).attr('data-url')
      if (l === p) {
      $(this).addClass('mnpglk-active');
      }
    });
  });


  var infinite = new Waypoint.Infinite({
    element: $('.infinite-container')[0],
    onBeforePageLoad: function () {
      $('.loading').show();
    },
    onAfterPageLoad: function ($items) {
      $('.loading').hide();
    }
  });

  $(function () {
    $('[data-tooltip="tooltip"]').tooltip()
    $('[data-tooltip="tooltip"]').click(function () {
      $('[data-tooltip="tooltip"]').tooltip("hide");
   });
});

$(document).ready(function () {
  var search_terms = $('#search-term-e').attr('data-value');
  if(search_terms) {
    var terms = search_terms.split(/\+s/);
    $(".search-ctr-marked").mark(terms, {
        "element": "span",
        "className": "highlight"
    });
  }

})

$(document).ready(function () {
  $(".search-btn").on('click', function () {
      var target_form = $(this).attr('data-target')
      $('#'+target_form).submit()
  });
  var target_btn = $('#lister-page').attr("data-target");
  $(".search-btn").each(function () {
      if($(this).attr('data-target') == target_btn){
          $(this).addClass('search-btn-active');
      }
  });
});
$(document).ready(function () {
  var parent = $("#menureform");
  var divs = parent.children();
  while (divs.length) {
      parent.append(divs.splice(Math.floor(Math.random() * divs.length), 1)[0]);
  }
});


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

  $('.mngpl').on('click', function () {
      window.location = $(this).find('a').attr('href');
  })
})
$(document).ready(function () {
  $('.main-top-nav .nav-goto-holder').on('click', function () {
      window.location = $(this).attr('data-url');
      return false;
  })
})
$(document).ready(function () {
  $('[data-tooltip="tooltip"]').tooltip()
  $('[data-tooltip="tooltip"]').click(function () {
      $('[data-tooltip="tooltip"]').tooltip("hide");
  });

})

$(document).ready(function (e) {

  $(document).on("click",".show-report-form", function (e) {
    var reportbtn = $(this)
    $.ajax({
      url: reportbtn.attr("data-url"),
      type: 'get',
      dataType:'json',
      beforeSend: function(){
        $('#modal-report').modal('show');
      },
      success: function(data){
        $('#modal-report .modal-content').html(data.html_form);
      }
    });
  });

  $('#modal-report').on("submit",".report-form",function (e){
    e.preventDefault();
    e.stopImmediatePropagation();
    var form = $(this).serialize();
    $.ajax({
      url: $(this).attr('data-url'),
      type: $(this).attr('method'),
      data: form,
      dataType: 'json',
      success: function(data){
        if(data.user_valid){
          $('.modal-body').html('<p class="text-center"><strong>Thanks for notifying us.</strong></p><p class="text-muted text-center">Your report has successfully been submitted.</p>');
          $('.modal-footer').html('<button type="button" class="mx-1 btn btn-secondary no-border no-outline text-center" data-dismiss="modal" style="border-radius: 20px;">Close</button>')
          setTimeout(function() {
          $('#modal-report').modal('hide');
          $('body').removeClass('modal-open');
          $('.modal-backdrop').remove();  
          }, 2620);
        } 
      }
    })
  });

  $(document).on('click','.add-uni-btn', function () {
    var addunibtn = $(this)
    $.ajax({
      url: addunibtn.attr("data-url"),
      type: 'get',
      dataType:'json',
      beforeSend: function(){
        $('#modal-report').modal('show');
      },
      success: function(data){
        $('#modal-report .modal-content').html(data.html_form);
      }
    });
  })

  $('#modal-report').on("submit",".add-uni-form",function (e){
    e.preventDefault();
    e.stopImmediatePropagation();
    var form = $(this).serialize();
    var success_url = $(this).attr('data-success-url');
    $.ajax({
      url: $(this).attr('data-url'),
      type: $(this).attr('method'),
      data: form,
      dataType: 'json',
      success: function(data){
        if(data.form_valid){
          $('#modal-report').modal('hide');
          $('body').removeClass('modal-open');
          $('.modal-backdrop').remove();  
          alert(success_url)
          location.href = success_url;
        } else {
            $('.modal-body').html('<p class="text-center">There was an error with your request</p>');
            $('.modal-footer').html('<button type="button" class="mx-1 btn btn-secondary no-border no-outline text-center" data-dismiss="modal" style="border-radius: 20px;">Close</button>')
            setTimeout(function() {
            $('#modal-report').modal('hide');
            $('body').removeClass('modal-open');
            $('.modal-backdrop').remove();  
            }, 1720);
          }
      },
  });
})
  
});