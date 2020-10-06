const OG_IMG_SRC = $('.edit-pro-all .img-create-post').attr('src');
const OG_REMOVE_BTN =  $("#remrevctr button");

const USER_ID = $('#uidnameinput').val();

$(document).ready(function () {

      $(document).on("click","#rmvproimg", function (e) {
          e.preventDefault();
          var btn = $(this);
          $.ajax({
              url: btn.attr("data-url"),
              type: 'get',
              dataType:'json',
              data: $(this).closest('form').serialize(),
              beforeSend: function(){
                  $('#modal-profile').modal('show');
              },
              success: function(data){
                  $('#modal-profile .modal-content').html(data.html_form);
              }
          });
      });
      
      $('#modal-profile').on("submit",".remove-user-image-form",function (e){
          e.preventDefault();
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
                  location.href = data.new_url           
              }
          })
      });

      $('.field-change-btn').on('click', function () {
        var content_id = "id_" + $(this).attr('data-contenteditable')
        var field = document.getElementById(content_id)
        $(field).removeAttr('disabled');

      })
    
    $('.easy-autocomplete').ready( function () {
      $('div.easy-autocomplete').removeAttr('style')
      $('div').removeClass('easy-autocomplete');
    })

    $('.menu-link').on('click', function () {
      window.location = $(this).attr('data-url');
    })

    $(document).on('change','.profile-privacy-form input[type="radio"]', function (){
      var form = $(this).closest('form')
      $.ajax({
              url: form.attr("data-url"),
              type: 'POST',
              dataType:'json',
              data: $(this).closest('form').serialize(),
              success: function(data){
                  
                if(data.update_ranking){
                  $('#ranking-form-ctr').html(data.ranking_form)
                }
                  
              },
        });
    })
    $(document).on('change','.search-securtiy-form input[type="radio"]', function (){
      var form = $(this).closest('form')
      $.ajax({
              url: form.attr("data-url"),
              type: 'POST',
              dataType:'json',
              data: $(this).closest('form').serialize(),
              success: function(data){
                  
                if(data.update_search_settings){
                  $('#st-form-ctr').html(data.search_settings_form)
                }
                  
              },
        });
    })

    $(document).on('change','.notifications-settings-form input[type="radio"]', function (){
      var form = $(this).closest('form')
      $.ajax({
              url: form.attr("data-url"),
              type: 'POST',
              dataType:'json',
              data: $(this).closest('form').serialize(),
              success: function(data){
                  
                if(data.update_notifications_settings){
                  $('#ns-form-ctr').html(data.notifications_form)
                }
                  
              },
        });
    })

  })