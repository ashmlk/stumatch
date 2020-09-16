const OG_IMG_SRC = $('.edit-pro-all .img-create-post').attr('src');
const OG_REMOVE_BTN =  $("#remrevctr button");

const USER_ID = $('#uidnameinput').val();

  $(document).ready(function () {

      $('#chppbtn').on('click', function () {
        $('.edit-pro-all #id_image').click();
      })

      var reader = new FileReader();
      reader.onload = function (e) {
          $('.edit-pro-all .img-create-post').attr('src', e.target.result);
          var btn = "<button type='button' data-url='/update/profile/image/"+ USER_ID+"/' id='submit-img' class='btn no-border no-outline mr-3 edit-profile-clickable text-primary'>Update</button>";
          var revert_btn = "<button type='button' id='revert-og-img' class='btn no-border no-outline mr-3 edit-profile-clickable text-danger'>Revert</button>";
          $('.edit-pro-all #updtimgbtn').append(btn);
          $('.edit-pro-all #remrevctr').html(revert_btn);
      }

      function readURL(input) {
              if (input.files && input.files[0]) {
                  reader.readAsDataURL(input.files[0]);
              }
      }

      $(".edit-pro-all #id_image").change(function(){
          readURL(this);
      });

      $('.edit-pro-all #remrevctr').on('click', function () {
        $('.edit-pro-all .img-create-post').attr('src', OG_IMG_SRC);
        $('.edit-pro-all #remrevctr').html(OG_REMOVE_BTN);
        $('.edit-pro-all #updtimgbtn').empty();
      })

      $(document).on('click','#submit-img', function (e){
          var form = new FormData(this.closest('form'));
          $.ajax({
            url: $(this).attr('data-url'),
            type: "POST",
            data: form,
            cache: false,
            processData: false,
            contentType: false,
            dataType: 'json',
            success: function (data){
                $('.edit-pro-all .pro-img-ctr').html(data.image_updated);
            },
            error: function(rs, e){
                console.log(rs.responeText);
            },
        });
      })

      $(document).on("click","#rmvproimg", function (e) {
          e.stopImmediatePropagation();
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
                  $('.edit-pro-all .pro-img-ctr').html(data.image_updated);
                  $('#modal-profile').modal('hide');
                  $('body').removeClass('modal-open');
                  $('.modal-backdrop').remove();                    
              }
          })
      });

      $('.field-change-btn').on('click', function () {
        var content_id = "id_" + $(this).attr('data-contenteditable')
        var field = document.getElementById(content_id)
        $(field).removeAttr('disabled');

      })

      var options = {
      url: "/static/jsons/world_universities_and_domains.json",
      getValue: "name",
      requestDelay: 200,
      template: {
      type: "description",
      fields: {
          description: "country"
          },
      },
      list: {
          maxNumberOfElements: 7,
          showAnimation: {
          type: "fade", //normal|slide|fade
          time: 300,
          callback: function() {}
          },
          hideAnimation: {
          type: "fade", //normal|slide|fade
          time: 300,
          callback: function() {}
          },
          match: {
              enabled: true
          }
      },
        theme: "square"
      };

    $("#id_university").easyAutocomplete(options);
    
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