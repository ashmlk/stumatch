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
$(document).ready(function () {
          
  var options = {
      url: function(q) {
        return '/home/search/get?q=' + q + "&format=json";
      },
      getValue: "search_term",
      requestDelay: 100,
      adjustWidth: true,
      template: {
      type: "description",
      fields: {
          description: "context"
          },
      },
      list: {
          maxNumberOfElements: 10,
          showAnimation: {
          type: "slide", //normal|slide|fade
          time: 200,
          callback: function() {}
          },
          hideAnimation: {
          type: "slide", //normal|slide|fade
          time: 200,
          callback: function() {}
          },
          match: {
              enabled: true
          }
      },
  theme: "round"
  };
  $("#searchetal").easyAutocomplete(options);s
})
$(document).ready(function () {
  var search_terms = $('#search-term-e').attr('data-value');
  var terms = search_terms.split(/\+s/);
  $(".search-ctr-marked").mark(terms, {
      "element": "span",
      "className": "highlight"
  });

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