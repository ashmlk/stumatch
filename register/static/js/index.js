window.onunload = function () {
  for (var key in sessionStorage) {
    if (key.indexOf('profile-info-') !== -1)
        sessionStorage.removeItem(key);
  }
}
$(document).ready(function () {  
    var path = window.location.href;
    var p = window.location.pathname;
    var full_compass = `<svg xmlns="http://www.w3.org/2000/svg" width="21" height="21" fill="currentColor" class="bi bi-compass-fill" viewBox="0 0 16 16">
            <circle cx="8" cy="8" r="8"/>
            <path fill="#ffffff" d="m6.94,7.44l4.95,-2.83l-2.83,4.95l-4.949,2.83l2.828,-4.95l0.001,0z" id="svg_2"/>
          </svg>`
    var full_house = `<svg width="22" height="24" xmlns="http://www.w3.org/2000/svg" class="bi bi-house-door">
          <g><rect x="-1" y="-1" width="24" height="26" id="canvas_background" fill="none"/></g>
          <g><path stroke="null" d="m8.89424,20.70579l0,-4.69411c0,-0.32812 0.35096,-0.66293 0.70192,-0.66293l2.80768,0c0.35096,0 0.70192,0.33482 0.70192,0.66963l0,4.68741a0.70192,0.66963 0 0 0 0.70192,
          0.66963l5.61537,0a0.70192,0.66963 0 0 0 0.70192,-0.66963l0,-9.37482a0.70192,0.66963 0 0 0 -0.20496,-0.4741l-1.9008,-1.81202l-2.80768,-2.67852l-3.71456,-3.54502a0.70192,0.66963 0 0 0 -0.99392,0l-8.42305,
          8.03556a0.70192,0.66963 0 0 0 -0.20496,0.4741l0,9.37482a0.70192,0.66963 0 0 0 0.70192,0.66963l5.61537,0a0.70192,0.66963 0 0 0 0.70192,-0.66963l-0.00001,0z"/></g>
         </svg>`
    var full_bell = '<svg style="transform: rotate(30deg)" width="21" height="21"  viewBox="0 0 16 16" class="bi bi-bell-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg">'+
         '<path d="M8 16a2 2 0 0 0 2-2H6a2 2 0 0 0 2 2zm.995-14.901a1 1 0 1 0-1.99 0A5.002 5.002 0 0 0 3 6c0 1.098-.5 6-2 7h14c-1.5-1-2-5.902-2-7 0-2.42-1.72-4.44-4.005-4.901z"/></svg>'

    if($('#body_home_page').length){
      $('.navbar-nav li.nav-home-link').find('a').html(full_house);
    }
    if($('#body_post_page').length){
      $('.navbar-nav li.nav-post-link').find('a').html(full_compass);
    }


    $('.navbar-nav li a').each(function(){
      var $this = $(this);
      if($this.attr('href').indexOf(p) !== -1){
          var icon = $this.find('svg');
          if($(icon).hasClass("bi-house-door")){
            $(this).html(full_house);
          }
          else if($(icon).hasClass("bi-bell")){
            $(this).html(full_bell);
          }
          else if($(icon).hasClass("bi-compass")){

            $(this).html(full_compass);            
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

    var timer, timerRemove;

    $(document).on("mouseenter",".user-display-info", function() {
      let offset = $(this).offset();
      let height = $(this).height();
      let width = $(this).width();
      let id = $(this).attr('data-user-id');
      if (timer) clearTimeout(timer);
      timer = setTimeout(function() {
          getUserInfo(id, offset, height, width)
      }, 1000);


    });

    $(document).on("mouseleave",".user-display-info", function() {
      if($(document).find('.profile-info-div:hover').length < 1){
        if (timer) clearTimeout(timer);
        timerRemove = setTimeout(function() {
          $(document).find('.profile-info-div').remove();
        }, 400);
      }
    });

    $(document).on("mouseleave",".profile-info-div", function() {
      if($(document).find('.user-display-info:hover').length < 1){
        if (timer) clearTimeout(timer);
        timerRemove = setTimeout(function() {
          $(document).find('.profile-info-div').remove();
        }, 400);
      }
 
    });

    function createProfileInfo(user){
      let schoolInfo = mutual_course_info = mutual_friends_info = '';
      if(user.university.length > 0 || user.program.length > 0){
        let divider = '';
        if(user.university.length > 0 && user.program.length > 0){
          divider = '<span class="text-dark">·</span>';
        }
        schoolInfo = `<div class="profile-school-info font-auto-sm">
                      <span class="text-dark">
                        ${user.university}
                      </span>
                      ${divider}
                      <span class="text-dark">
                        ${user.program}
                      </span>
                    </div>`
      }
      if(user.mutual_friends_info.count > 0){
        let mutual_friends_context = 'Friends with ';
        let mutual_friends_count = user.mutual_friends_info.count;
        mutual_friends_context += user.mutual_friends_info.usernames[0]
        if(mutual_friends_count > 1){
          mutual_friends_context += `, and ${user.mutual_friends_info.count - 1} others`
        }
        mutual_friends_info = `<span class="font-auto-xs">${mutual_friends_context}</span>`
      }
      if(user.mutual_course_info.count > 0){
        let mutual_course_context = 'You both take ';
        let mutual_course_count = user.mutual_course_info.count;
        mutual_course_context +=  user.mutual_course_info.codes[0]
        if(mutual_course_count > 1){
          mutual_course_context += ', and ' + mutual_course_count - 1 + ' more'
        }
        mutual_course_info = `<span class="font-auto-xs">${mutual_course_context}</span>`
      }
      let profileInfoContainer = `<div class="request-info-profile bg-white border border-r">
                                    <div class="profile-info px-2">
                                      <div class="d-flex align-items-top">
                                        <div class="profile-image pt-3" style="display: inline-block;">
                                          <img class="rounded-circle user-photo-lg" src="${user.profile_image_url}">
                                        </div>
                                        <div class="px-3 pt-3">
                                          <div class="profile-username">
                                            <div style="line-height:8px;">
                                              <a class="text-dark" href="${user.profile_absolute_url}">
                                                <span class="user-username-font">${user.username}</span>       
                                              </a>
                                            </div>
                                            <span class="text-muted-jc font-auto-xs">${user.full_name}</span>
                                          </div>
                                          ${schoolInfo}
                                          <div class="mutual-details text-muted-jc ">
                                            <div class="mutual-courses" style="display:block;line-height:8px;">
                                              ${mutual_course_info}
                                            </div>
                                            <div class="mutual-friends">
                                              ${mutual_friends_info}
                                            </div>
                                          </div>
                                        </div>
                                      </div>
                                    </div>
                                    <div class="profile-counts mt-3 mb-2">
                                      <div class="border-top border-bottom px-2 font-auto-sm py-2">
                                        <div class="d-flex align-items-center row">
                                          <div class="col-4 profile-info-count">
                                            <div class="w-100 text-center">
                                              <div class="item-count">
                                                <div>
                                                  <span class="font-weight-bold-jc">
                                                    ${user.course_count}
                                                  </span>
                                                </div>
                                                <div>
                                                  <span class="text-muted-jc">
                                                    courses
                                                  </span>
                                                </div>
                                              </div>
                                            </div>
                                          </div>
                                          <div class="col-4 profile-info-count">
                                            <div class="w-100 text-center">
                                              <div class="item-count">
                                                <div>
                                                  <span class="font-weight-bold-jc">
                                                    ${user.post_count}
                                                  </span>
                                                </div>
                                                <div>
                                                  <span class="text-muted-jc">
                                                    posts
                                                  </span>
                                                </div>
                                              </div>
                                            </div>
                                          </div>
                                          <div class="col-4 profile-info-count">
                                            <div class="w-100 text-center">
                                              <div class="item-count">
                                                <div>
                                                  <span class="font-weight-bold-jc">
                                                    ${user.friend_count}
                                                  </span>
                                                </div>
                                                <div>
                                                  <span class="text-muted-jc">
                                                    friends
                                                  </span>
                                                </div> 
                                              </div>
                                            </div>
                                          </div>
                                        </div>
                                      </div>
                                    </div>
                                    <div class="friendship-container w-100 px-1 mb-2" data-uid="${user.id}">
                                    </div>
                                  </div>`

      return profileInfoContainer;

    }

    function getProfileInfoOnSession(user){
      let profileInfo;
      let sessionStorageProfileInfo = sessionStorage[`profile-info-${user.id}`]; 
      if(sessionStorageProfileInfo === undefined){
        profileInfo = createProfileInfo(user);
        sessionStorage.setItem(`profile-info-${id}`, JSON.stringify(user));
      } else {
        profileInfo = JSON.parse(sessionStorageProfileInfo);
      }
      return profileInfo;
    }

    function getUserInfo(id, offset, height, width){
      var top = offset.top + height + "px";
      var left = offset.left + "px";
      let profileInfo;
      let sessionStorageProfileInfo = sessionStorage.getItem(`profile-info-${id}`); 
      if(sessionStorageProfileInfo === undefined || sessionStorageProfileInfo === null){
        $.ajax({
          url: `/request_info/${id}/`,
          type: "GET",
          dataType: "json",
          success: function (data) {
            $(document).find('.profile-info-div').remove();
            let info = createProfileInfo(data.user);
            sessionStorage.setItem(`profile-info-${data.user.id}`, JSON.stringify(data.user));
            let div = `<div class="profile-info-div" style="left:${left};top:${top};">${info}</div>`;
            $('body').css( {
              'position': 'relative',
            });
            $('body').append($(div));
          },
        });
      } else {
            profileInfo = JSON.parse(sessionStorageProfileInfo);
            let info = createProfileInfo(profileInfo)
            let div = `<div class="profile-info-div" style="left:${left};top:${top};">${info}</div>`;
            $('body').css( {
              'position': 'relative',
            });
            $('body').append($(div));
      }
      
    }
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