$(document).ready(function () {  

    var path = window.location.href;
    var p = window.location.pathname;

    $('.navbar-nav li a').each(function(){
      var $this = $(this);
      if($this.attr('href').indexOf(p) !== -1){
          var icon = $this.find('svg');
          if($(icon).hasClass("bi-house-door")){
            var full_house = '<svg width="22" height="22" viewBox="0 0 16 16" class="bi bi-house-door-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg">'+
                              '<path d="M6.5 10.995V14.5a.5.5 0 0 1-.5.5H2a.5.5 0 0 1-.5-.5v-7a.5.5 0 0 1 .146-.354l6-6a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 .146.354v7a.5.5 0 0 1-.5.5h-4a.5.5 0 0 1-.5-.5V11c0-.25-.25-.5-.5-.5H7c-.25 0-.5.25-.5.495z"/>'+
                                '<path fill-rule="evenodd" d="M13 2.5V6l-2-2V2.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5z"/></svg>'
            $(this).html(full_house)
          }
          else if($(icon).hasClass("bi-bell")){
            var full_bell = '<svg style="transform: rotate(30deg)" width="21" height="21"  viewBox="0 0 16 16" class="bi bi-bell-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg">'+
                            '<path d="M8 16a2 2 0 0 0 2-2H6a2 2 0 0 0 2 2zm.995-14.901a1 1 0 1 0-1.99 0A5.002 5.002 0 0 0 3 6c0 1.098-.5 6-2 7h14c-1.5-1-2-5.902-2-7 0-2.42-1.72-4.44-4.005-4.901z"/></svg>'
            $(this).html(full_bell)
          }
          else if($(icon).hasClass("bi-book")){
            var full_course = '<svg width="22" height="22" viewBox="0 0 16 16" class="bi bi-book-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg">'+
                              '<path fill-rule="evenodd" d="M8 1.783C7.015.936 5.587.81 4.287.94c-1.514.153-3.042.672-3.994 1.105A.5.5 0 0 0 0 2.5v11a.5.5 0 0 0.707.455c.882-.4 2.303-.881 3.68-1.02 1.409-.142 2.59.087 3.223.877a.5.5 0 0 0 .78 0c.633-.79 1.814-1.019 3.222-.877 1.378.139 2.8.62 3.681 1.02A.5.5 0 0 0 16 13.5v-11a.5.5 0 0 0-.293-.455c-.952-.433-2.48-.952-3.994-1.105C10.413.809 8.985.936 8 1.783z"/></svg>'
            $(this).html(full_course);            
          }
        }
      })
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