
$(document).ready(function () {
    var search_url = "/search?q="
    $(document).on('keyup','#searchbar_n', function () {
      if($(this).val()){
        var q = $(this).val();
        $.ajax({
          type: "GET",
          url: "/search/results/get?q=" + q,
          dataType: 'json',
          success: function (data){
            if(data.search_user.length > 0){
              $('._rcntrsltctr').find('li').remove();
              $('._rcntrslt').text("Recent Searches")
              $('._rcntrslt').append('<span><button class="float-right btn btn-sm text-primary _rmvsrtus" type="button">Clear All</button></span>')
              for (i in data.search_user) {
                $('._rcntrsltctr').append('<a style="text-decoration:none;" class="text-dark" href="'+search_url+data.search_user[i]+'&o=top">'
                  +'<li class="rounded list-group-item searchable-selectable">'+data.search_user[i]+'<span class="float-right button-group">'   
                  +'<button type="button" data-reference="'+data.search_user[i]+'" class="btn btn-sm _rmvsrtus"><span style="font-size:20px;" class="material-icons">close</span></button>'
              +'</span></li></a>')
              }
            }
            if(data.search_top.length > 0){
              $('._tprsltctr').find('li').remove()
              $('._tprslt').text("Top Searches")
              for(i in data.search_top) {
                $('._tprsltctr').append('<a style="text-decoration:none;" class="text-dark" href="'+search_url+data.search_user[i]+'&o=top"><li class="rounded list-group-item searchable-selectable">'+data.search_top[i]+'</li>')
              }
            }
            if(data.search_user.length <= 0 ) {
              $('._rcntrslt').empty();
              $('._rcntrsltctr').find('li').remove();
            }
            if(data.search_top.length <= 0 ) {
              $('._tprslt').empty();
              $('._tprsltctr').find('li').remove();
            }
            
            $('.search-query-result').show()
          },
          error: function(rs, e){
              console.log(rs.responeText);
          },
      })
      } else {
        $('.search-query-result').hide()
      }
    });
    $(document).on('click', function () {
      $('.search-query-result').hide();
    });
    $(document).on('click','._rmvsrtus', function (e){
      e.preventDefault();
      e.stopImmediatePropagation();
      var btn = $(this)
      var t = $(this).closest('button').attr('data-reference')
      if(t){
        var u = "{% url 'home:remove-search-query' %}?t=" + t;
      } else {
        var u = "{% url 'home:remove-search-query' %}";
      }
      $.ajax({
          type: "POST",
          url: u,
          dataType: 'json',
          data: {
            'csrfmiddlewaretoken':'{{ csrf_token }}'
          },
          success: function (data){
            if(data.indv_search_remove){
              $(btn).closest('li').remove();
            } else if(data.all_search_remove) {
              $('._rcntrsltctr').closest('.usrchctr').empty();
            }
          },
          error: function(rs, e){
              console.log(rs.responeText);
          },
      });
    });

  })