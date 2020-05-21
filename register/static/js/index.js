$(document).ready(function () {    
    var path = window.location.href;
    $('#_pol3 a').each(function() {
      if (this.href === path) {
      $(this).closest('div').addClass('menu-link-active');
      }
    });
    $(".menu-link").on("click", function() {
      location.href = $(this).children("a").attr("href");
    });
  });

  $('.mnpglk').on('click', function () {
    window.location = $(this).attr('data-url');
    return false;
  })

  $('.mnpglk').each(function() {
    if ($(this).attr('data-url') === path) {
    $(this).addClass('mnpglk-active');
    }
  });

  $('.buzz-comment-container').ready(function () {
    $('.bzrvmuim').initial({
      charCount: 2, 
      textColor: '#ffffff',
      seed: 12,
      fontSize: 40,
      fontWeight: 400,
    });
  })
  $(function () {
    $('[data-tooltip="tooltip"]').tooltip()
    $('[data-tooltip="tooltip"]').click(function () {
      $('[data-tooltip="tooltip"]').tooltip("hide");
   });
});