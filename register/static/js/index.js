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

  $('.buzz-comment-container').ready(function () {
    $('.bzrvmuim').initial({
      charCount: 2, 
      textColor: '#ffffff',
      seed: 12,
      fontSize: 40,
      fontWeight: 400,
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
  
  $(window).scroll(function() {
    if ($(window).scrollTop() > 80) {
        $('.cp-cntr-h').show();
    } else {
      $('.cp-cntr-h').hide();
      }
  });

  $(function () {
    $('[data-tooltip="tooltip"]').tooltip()
    $('[data-tooltip="tooltip"]').click(function () {
      $('[data-tooltip="tooltip"]').tooltip("hide");
   });
});