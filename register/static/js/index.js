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