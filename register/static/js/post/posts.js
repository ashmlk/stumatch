$(document).ready(function () {

  var greySpinnerMed = `<div class="d-flex justify-content-center grey-spinner-md">
                          <div class="spinner-border text-muted-jc spinner-border-sm" role="status">
                            <span class="sr-only">Loading...</span>
                          </div>
                        </div>`

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  var csrftoken = getCookie("csrftoken");

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  }
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    },
  });


  $("#id_content").keyup(function() {
    if(this.value.length > 0 && this.value != "Default value") {
      $('#sub-etal').attr("disabled", false);
      $('#sub-etal').prop('disabled', false);
    } else {
      $('#sub-etal').attr("disabled", true);
      $('#sub-etal').prop('disabled', true);
    }
  });

  if ($(".darkmode--activated").length) {
    $("emoji-picker").removeClass("light").addClass("dark");
  }

  $(".emoji-dropup-menu").on("click", function (e) {
    e.stopPropagation();
  });

  $(document).on("click.bs.dropdown", ".emoji-dropdown", (e) => {
    e.stopPropagation();
  });

  document
    .querySelector("emoji-picker")
    .addEventListener("emoji-click", (e) => {
      let emoji = e.detail["unicode"];
      $("#id_content").val($("#id_content").val() + "" + emoji);
    });

  var tribute = new Tribute({
    values: function (text, cb) {
      getUsernames(text, (users) => cb(users));
    },
    lookup: "username",
    fillAttr: "username",
    selectClass: "tributehighlight",
    noMatchTemplate: function (item) {
      return '<span style:"visibility: hidden;"></span>';
    },
    menuItemTemplate: function (item) {
      return `<div class="p-1">
            <div class="d-flex align-items-center">
              <div class="mx-1 mr-2">
                <img class="rounded-circle" height="30px" width="30px" src="${item.original.image}"/>
              </div>
              <div class="name mx-1">
                <div class="user-username-font d-flex align-items-center">
                  ${item.original.username}
                </div>							
              </div>
            </div>
          </div>`;
    },
    selectTemplate: function (item) {
      return "@" + item.original.username;
    },
  });

  var tributeHashTag = new Tribute({
    trigger: "#",
    values: function (text, cb) {
      getHashtags(text, (tags) => cb(tags));
    },
    lookup: "name",
    fillAttr: "name",
    selectClass: "tributehighlight",
    noMatchTemplate: function (item) {
      return '<span style:"visibility: hidden;"></span>';
    },
    menuItemTemplate: function (item) {
      return (
        '<div class="p-2"><div class="d-flex"><div class="name mx-1"><div class="h6">#' +
        item.original.name +
        "</div></div></div></div>"
      );
    },
    selectTemplate: function (item) {
      return "#" + item.original.name;
    },
  });

  function getUsernames(text, cb) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/get/user/mentions?q=" + text, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onload = function () {
      var data = JSON.parse(xhr.responseText);
      if (xhr.readyState === 4 && xhr.status == "200") {
        cb(data);
      } else if (xhr.status === 403) {
        cb([]);
      }
    };
    xhr.send(null);
  }

  function getHashtags(text, cb) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/taggit/?query=" + text, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onload = function () {
      var data = JSON.parse(xhr.responseText).tags;
      console.log(data);
      if (xhr.readyState === 4 && xhr.status == "200") {
        cb(data);
      } else if (xhr.status === 403) {
        cb([]);
      }
    };
    xhr.send(null);
  }

  $(".post-comment-textarea").highlightWithinTextarea({
    highlight: /(?:(?<mention>@))([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)/gi,
  });

  tribute.attach(document.getElementsByClassName('post-comment-textarea'));

  $(document).on("click", ".create-post-btn", function (e) {
    e.stopImmediatePropagation();
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: "get",
      dataType: "json",
      beforeSend: function () {
        $("#modal-post").modal("show");
      },
      success: function (data) {
        $("#modal-post .modal-content").html(data.html_form);
        let postSubmitButton = $('#sub-etal');
        let lenContent = $("#id_content").value;
        if(lenContent == undefined){
          $(postSubmitButton).attr("disabled", true);
          $(postSubmitButton).prop('disabled', true);
        }
        tributeHashTag.attach(document.getElementById("id_content"));
        tribute.attach(document.getElementById("id_content"));
        $("#id_content").highlightWithinTextarea({
          highlight: /(?:(?<mention>@)|(?<hash>#))([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)/gi,
        });
      },
    });
    return false;
  });

  $("#modal-post").on("submit", ".post-create-form", function (e) {
    e.preventDefault();
    e.stopImmediatePropagation();
    var form = new FormData(this);
    $.ajax({
      url: $(this).attr("data-url"),
      type: $(this).attr("method"),
      data: form,
      cache: false,
      processData: false,
      contentType: false,
      dataType: "json",
      success: function (data) {
        if (data.form_is_valid) {
          $("#modal-post").modal("hide");
          $("#_np2u").prepend(data.post);
        } else {
          $("#modal-post .modal-content").html(data.html_form);
        }
      },
    });
    return false;
  });

  $(document).on("click", ".likeBtn", function (e) {
    var btn = $(this);
    e.preventDefault();
    e.stopImmediatePropagation();
    $.ajax({
      type: "POST",
      url: $(this).attr("data-url"),
      dataType: "json",
      data: {
        csrfmiddlewaretoken: getCookie("csrftoken"),
      },
      success: function (data) {
        data.likescount > 0
          ? $(btn)
              .closest(".post-details-view")
              .find(".post-counts")
              .find(".like-count-ctr")
              .html(`<span class="like-count small text-muted-jc ml-1 underline-text post-show-liked-by"  data-url="/post/${data.guid_url}/liked_by/">${data.likescount} Likes </span>`)
          : $(btn)
              .closest(".post-details-view")
              .find(".post-counts")
              .find(".like-count-ctr")
              .html("");
        if ($(btn).find("span").hasClass("is-liked")) {
          // user has unliked post
          $(btn).html(`<span class="not-liked text-muted-jc" >
					<svg  width="20" height="20" viewBox="0 0 16 16" class="bi bi-heart" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
					  <path fill-rule="evenodd" d="M8 2.748l-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/>
					</svg>
				  </span> `);
        } else {
          // user has liked post
          $(btn).html(`<span class="is-liked text-red-jc" > 
					<svg width="20"  height="20" viewBox="0 0 16 16" class="bi bi-heart-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
					  <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/>
					</svg> 
				  </span>`);
        }
      },
      error: function (rs, e) {
        console.log(rs.responeText);
      },
    });
  });

  $(document).on("click", ".post-dropdown-options-btn", function (e) {
    let bookmarkBtn = (actionBtns = null);
    let optionBtn = $(this);
    let dropdownMenu = $(this).siblings(".dropdown-menu");
    $.ajax({
      type: "GET",
      url: $(this).attr("data-url"),
      dataType: "json",
      success: function (data) {
        if (data.has_bookmarked) {
          bookmarkBtn = `<button class="small dropdown-item post-bookmark-btn no-outline" type="button" data-url="/post/${data.guid_url}/bookmark/" >
					<svg class="bi mr-1 bi-bookmark-fill" width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
					  <path fill-rule="evenodd" d="M3 3a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v12l-5-3-5 3V3z"/>
					</svg>Bookmark</button>`;
        } else if (data.has_bookmarked === false) {
          bookmarkBtn = `<button class="small dropdown-item post-bookmark-btn no-outline" type="button" data-url="/post/${data.guid_url}/bookmark/" >
					<svg class="bi mr-1 bi-bookmark" width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
					<path fill-rule="evenodd" d="M8 12l5 3V3a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v12l5-3zm-4 1.234l4-2.4 4 2.4V3a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1v10.234z"/>
				  </svg>Bookmark</button>`;
        }
        $(dropdownMenu).append(bookmarkBtn);
        if (data.user_is_author) {
          actionBtns = `<button class="small dropdown-item show-form-update"
					data-url="${data.post_edit_url}"><svg class="bi mr-1 bi-pencil-square"
					  width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor"
					  xmlns="http://www.w3.org/2000/svg">
					  <path
						d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456l-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z" />
					  <path fill-rule="evenodd"
						d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z" />
					</svg>Edit</button>
					<button class="small dropdown-item show-form-delete"
					data-url="${data.post_delete_url}"><svg class="bi mr-1 bi-trash" width="1em"
					  height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
					  <path
						d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z" />
					  <path fill-rule="evenodd"
						d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4L4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z" />
					</svg>Delete</button>`;
        } else {
          actionBtns = `<button class="small dropdown-item show-report-form"
					data-url="${data.report_by_user_url}?t=p&hid=${data.post_hashid}"><svg
					  width="1em" height="1em" viewBox="0 0 16 16" class="bi mr-1 bi-flag" fill="currentColor"
					  xmlns="http://www.w3.org/2000/svg">
					  <path fill-rule="evenodd" d="M3.5 1a.5.5 0 0 1 .5.5v13a.5.5 0 0 1-1 0v-13a.5.5 0 0 1 .5-.5z" />
					  <path fill-rule="evenodd"
						d="M3.762 2.558C4.735 1.909 5.348 1.5 6.5 1.5c.653 0 1.139.325 1.495.562l.032.022c.391.26.646.416.973.416.168 0 .356-.042.587-.126a8.89 8.89 0 0 0 .593-.25c.058-.027.117-.053.18-.08.57-.255 1.278-.544 2.14-.544a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-.5.5c-.638 0-1.18.21-1.734.457l-.159.07c-.22.1-.453.205-.678.287A2.719 2.719 0 0 1 9 9.5c-.653 0-1.139-.325-1.495-.562l-.032-.022c-.391-.26-.646-.416-.973-.416-.833 0-1.218.246-2.223.916a.5.5 0 1 1-.515-.858C4.735 7.909 5.348 7.5 6.5 7.5c.653 0 1.139.325 1.495.562l.032.022c.391.26.646.416.973.416.168 0 .356-.042.587-.126.187-.068.376-.153.593-.25.058-.027.117-.053.18-.08.456-.204 1-.43 1.64-.512V2.543c-.433.074-.83.234-1.234.414l-.159.07c-.22.1-.453.205-.678.287A2.719 2.719 0 0 1 9 3.5c-.653 0-1.139-.325-1.495-.562l-.032-.022c-.391-.26-.646-.416-.973-.416-.833 0-1.218.246-2.223.916a.5.5 0 0 1-.554-.832l.04-.026z" />
					</svg>Report</button>`;
        }
        $(dropdownMenu).append(actionBtns);
      },
      error: function (rs, e) {
        console.log(rs.responeText);
      },
    });
  });

  let postActionBtn = null;

  $(document).on("click", ".show-form-delete", function (e) {
    e.stopImmediatePropagation();
    postActionBtn = $(this);
    $.ajax({
      url: postActionBtn.attr("data-url"),
      type: "get",
      dataType: "json",
      beforeSend: function () {
        $("#modal-post-delete").modal("show");
      },
      success: function (data) {
        $("#modal-post-delete .modal-content").html(data.html_form);
      },
    });
  });

  $("#modal-post-delete").on("submit", ".delete-form", function (e) {
    e.preventDefault();
    e.stopImmediatePropagation();
    var form = new FormData(this);
    $.ajax({
      url: $(this).attr("data-url"),
      type: $(this).attr("method"),
      data: form,
      cache: false,
      processData: false,
      contentType: false,
      dataType: "json",
      success: function (data) {
        if (data.form_is_valid) {
          $("#modal-post-delete").modal("hide");
          $("body").removeClass("modal-open");
          $(".modal-backdrop").remove();
          $(postActionBtn).closest(".post-ctr").remove();
        }
      },
    });
  });

  $(document).on("click", ".show-form-update", function (e) {
    e.stopImmediatePropagation();
    postActionBtn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: "get",
      dataType: "json",
      beforeSend: function () {
        $("#modal-post-update").modal("show");
      },
      success: function (data) {
        $("#modal-post-update .modal-content").html(data.html_form);
      },
    });
  });

  $("#modal-post-update").on("submit", ".update-form", function (e) {
    e.preventDefault();
    e.stopImmediatePropagation();
    var form = new FormData(this);
    $.ajax({
      url: $(this).attr("data-url"),
      type: $(this).attr("method"),
      data: form,
      cache: false,
      processData: false,
      contentType: false,
      dataType: "json",
      success: function (data) {
        if (data.form_is_valid) {
          $("#modal-post-update").modal("hide");
          $(postActionBtn).closest(".post-ctr").html(data.post);
        }
      },
    });
  });

  $(document).on('click', '.post-bookmark-btn', function (e) {
    e.preventDefault();
    e.stopImmediatePropagation();
    let bookmarkBtn = $(this);
    $.ajax({
      url: $(this).attr("data-url"),
      type: 'POST',
      data: {
        csrfmiddlewaretoken: getCookie("csrftoken")
      },
      dataType: "json",
      success: function (data) {
        if(data.is_bookmarked){
          $(bookmarkBtn).html(`<svg class="bi mr-1 bi-bookmark-fill" width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
          <path fill-rule="evenodd" d="M3 3a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v12l-5-3-5 3V3z"/>
        </svg>Bookmark`)
        } else {
          $(bookmarkBtn).html(`<svg class="bi mr-1 bi-bookmark" width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
					<path fill-rule="evenodd" d="M8 12l5 3V3a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v12l5-3zm-4 1.234l4-2.4 4 2.4V3a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1v10.234z"/>
				  </svg>Bookmark`)
        }
      },
    });
  })

  let commentGetUrl = null;
  if($('#post-comments-single-view').length){
    getComments(url=$('#post-comments-single-view').attr('data-url'))
  }


  $(document).on('click', '.view-more-comments-btn', function (){
    getComments(url=$(this).attr('data-url'));
    $(this).closest('div').remove();
  })


  $(".post-comment-textarea").keyup(function() {
    let commentSubmitButton = $(this).closest('.comment-textarea').siblings('.post-comment-submit-ctr').find('button')
    if(this.value.length > 0 && (this.value != "Add a comment..." || this.value != "Write your reply...")) {
      $(commentSubmitButton).attr("disabled", false);
    } else {
      $(commentSubmitButton).attr("disabled", true);
    }
  });


  $(document).on("change", '.post-comment-textarea', function (){
    resize(this);
  })

  $(document).on("cut paste drop keydown", '.post-comment-textarea', function (){
    delayedResize(this);
  })

  $(document).on('click', '.scroll-to-comment-box', function (){
    try {
      scrollToCommentBox()
    } catch (error) {
      return true;
    }
  })

  $(document).on("click", ".post-comment-like-btn", function (e) {
    let commentLikeBtn = $(this);
    e.preventDefault();
    $.ajax({
        type:"POST",
        dataType: 'json',
        url: $(this).attr("data-url"),     
        data: {
          csrfmiddlewaretoken: getCookie("csrftoken")
        },
        success: function (data) {
          $(commentLikeBtn).find('.like-count').html(`${data.like_count}`);
            if(data.is_liked){
              $(commentLikeBtn).find('.text-muted-jc').removeClass('text-muted-jc').addClass('text-red-jc');
            } else {
              $(commentLikeBtn).find('.text-red-jc').removeClass('text-red-jc').addClass('text-muted-jc');
            }
        },
        error: function(rs, e){
            console.log(rs.responeText);
        },
    });
  });

  $(document).on("click", ".dropdown .post-comment-dropdown-options-btn", function (e) {
    let commentOptionBtn = $(this);
    if(!$(commentOptionBtn).hasClass('options-shown')){
      $.ajax({
        type:"GET",
        dataType: 'json',
        url: $(this).attr("data-url"),     
        success: function (data) {
          let dropdownMenu = $(commentOptionBtn).siblings('.dropdown-menu');
          let actionBtns = '';
          if(data.viewer_can_delete){
              actionBtns = `<button class="small dropdown-item post-comment-delete-btn no-outline"
              data-url="${data.comment_delete_url}"><svg class="bi mr-1 bi-trash" width="1em"
                height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <path
                d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z" />
                <path fill-rule="evenodd"
                d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4L4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z" />
              </svg>Delete</button>`;
            }
          if(data.viewer_can_report){
            actionBtns += `<button class="small dropdown-item show-report-form  no-outline"
            data-url="${data.report_by_user_url}?t=cmnt&hid=${data.comment_hashed_id}"><svg
              width="1em" height="1em" viewBox="0 0 16 16" class="bi mr-1 bi-flag" fill="currentColor"
              xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" d="M3.5 1a.5.5 0 0 1 .5.5v13a.5.5 0 0 1-1 0v-13a.5.5 0 0 1 .5-.5z" />
              <path fill-rule="evenodd"
              d="M3.762 2.558C4.735 1.909 5.348 1.5 6.5 1.5c.653 0 1.139.325 1.495.562l.032.022c.391.26.646.416.973.416.168 0 .356-.042.587-.126a8.89 8.89 0 0 0 .593-.25c.058-.027.117-.053.18-.08.57-.255 1.278-.544 2.14-.544a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-.5.5c-.638 0-1.18.21-1.734.457l-.159.07c-.22.1-.453.205-.678.287A2.719 2.719 0 0 1 9 9.5c-.653 0-1.139-.325-1.495-.562l-.032-.022c-.391-.26-.646-.416-.973-.416-.833 0-1.218.246-2.223.916a.5.5 0 1 1-.515-.858C4.735 7.909 5.348 7.5 6.5 7.5c.653 0 1.139.325 1.495.562l.032.022c.391.26.646.416.973.416.168 0 .356-.042.587-.126.187-.068.376-.153.593-.25.058-.027.117-.053.18-.08.456-.204 1-.43 1.64-.512V2.543c-.433.074-.83.234-1.234.414l-.159.07c-.22.1-.453.205-.678.287A2.719 2.719 0 0 1 9 3.5c-.653 0-1.139-.325-1.495-.562l-.032-.022c-.391-.26-.646-.416-.973-.416-.833 0-1.218.246-2.223.916a.5.5 0 0 1-.554-.832l.04-.026z" />
            </svg>Report</button>`
          }
          $(dropdownMenu).prepend(actionBtns)
        },
        error: function(rs, e){
            console.log(rs.responeText);
        },
      });
      $(commentOptionBtn).addClass('options-shown');
    } else {
      console.log('return true')
      return true;
    }
    
  });

  document.addEventListener('scroll', function (event) {
    try {
      if (event.target.classList.contains('scroll-infinite-link')) { // or any other filtering condition        
          let el = event.target;
          let toTrigger = $('.'+$(el).attr('data-trigger'))
          if($(el).scrollTop() >= $(el)[0].scrollHeight - $(el)[0].offsetHeight - 60) {
            $(toTrigger).click();
        }
      }
    } catch (error) {
        return true;
    }
  }, true);

  if($('#post-detail').length > 0){
    var topOfOthDiv = $('#post-detail').find('.comment-textarea').offset().top;
    $(window).scroll(function() {
        if($(window).scrollTop() > topOfOthDiv) { 
            $('.scroll-to-comment-box').css({'visibility':'visible'}); 
        } else {
          console.log('sefuhwe')
          $('.scroll-to-comment-box').css({'visibility':'hidden'});
        }
    });
  }

  
  $(".post-comments-display").on('DOMNodeRemoved', function(e) {
    if(!$(this).siblings('.comment-box').hasClass('post-details-single-view')){
      if($(this).find('.comment-object').length < 2){
        $(this).siblings('.comment-box').removeClass('border-bottom');
      }
    } else {
      if($(this).find('.comment-object').length < 2){
        if(e.target.classList.contains('comment-object')){
          let emptyMessageContainer = `<div class="show-empty-message-ctr">
          <div class="d-flex justify-content-center pt-2 my-2">
              <div>
                  <h6>No comments to show</h6>
              </div>
            </div>
          </div>`
          $(this).append(emptyMessageContainer);
        }  
      }
    }
  });

  $(".post-comments-display").on('DOMNodeInserted', function(e) {
    try {
      if(e.target.classList.contains('comment-object')){
        if($(this).siblings('.comment-box').hasClass('post-details-single-view')){
          if($(this).find('.comment-object').length + 1 > 0){
            $(this).find('.show-empty-message-ctr').remove();
          }
        }
      } else if(e.target.classList.contains('show-empty-message-ctr')){
        $(this).find('.comment-list-actions').remove();
      }
    } catch (error) {
        return true;
    }
  });

  let commentCurrentlyOnAction = null;

  $(document).on("click", ".post-comment-delete-btn", function (e) {
    commentCurrentlyOnAction = $(this).closest('.comment-object')
    e.preventDefault();
    e.stopImmediatePropagation();
    $.ajax({
      url: $(this).attr("data-url"),
      type: "get",
      dataType: "json",
      beforeSend: function () {
        $("#modal-comment-delete").modal("show");
      },
      success: function (data) {
        $("#modal-comment-delete .modal-content").html(data.html_form);
      },
    });
  });

  $(document).on("submit", ".comment-delete-form", function (e) {
    e.preventDefault();
    e.stopImmediatePropagation();
    var form = new FormData(this);
    $.ajax({
      url: $(this).attr("data-url"),
      type: $(this).attr("method"),
      data: form,
      cache: false,
      processData: false,
      contentType: false,
      dataType: "json",
      success: function (data) {
        if (data.form_is_valid) {
          $("#modal-comment-delete").modal("hide");
          $("body").removeClass("modal-open");
          $(".modal-backdrop").remove();
          if(data.post_comment_count < 1){
            (commentCurrentlyOnAction).closest('.post-ctr').find('.post-counts').find('.comment-count-ctr').html('');
            $(commentCurrentlyOnAction).remove();
          } else {
            let newCount = null;      
            $('#post-detail').length != 0 ? newCount = `${data.post_comment_count} Comments` : newCount = `View ${data.post_comment_count} comments`;
            let commentCounts = $(commentCurrentlyOnAction).closest('.post-ctr').find('.post-counts');
            if($(commentCounts).find('.comment-count').length > 0){
              $(commentCounts).find('.comment-count').html(newCount);
            } else {
              $(commentCounts).find('.comment-count-ctr').html(`<a class="comment-count small ml-1 text-muted-jc" href="/post/${data.post_guid_url}/">${newCount}</a>`)
            }
            swapCommentViewerButton(comment=commentCurrentlyOnAction, replyCount=data['comment_reply_count']);
            $(commentCurrentlyOnAction).remove();
          }
        }
      },
    });
  });

  $(document).on('click', '.post-cancel-reply-btn', function(e){
    let commentBox = $(this).closest('.post-comment-reply-ctr').siblings('.comment-box');
    $(commentBox).find('textarea').attr('placeholder','Add a comment...');
    $(commentBox).find('form').removeAttr('data-isreply');
    $(commentBox).find('form').removeAttr('data-parent-id');
    $(this).closest('.post-comment-reply-ctr').remove();
  })

  // the parent comment box when user want to reply
  let parentCommentBox = null; 
  $(document).on('click', '.post-comment-reply-btn', function (){
      parentCommentBox = $(this).closest('.comment-actions').closest('.comment-ctr').find('.comment-replies');
      let commentBox = $(this).closest('.post-comments-display').siblings('.comment-box');
      let parentId = $(this).attr('data-parent-id');
      let parentAuthor = $(this).attr('data-parent-author');
      $(commentBox).siblings('.post-comment-reply-ctr').remove();
      let replyingToBox = `<div class="post-comment-reply-ctr my-1 py-1 pt-2 border-top">
          <div class="d-flex justify-content-between align-items-center px-2">
            <div class="replying-info font-auto-sm ">
              Replying to <span class="font-weight-bold-jc">${parentAuthor}</span>
            </div>
            <div class="cancel-reply-crt">
              <button class="post-cancel-reply-btn btn btn-sm text-dark">
                <span>
                  &times
                </span>
              </button>
            </div>
          </div>
        </div>`
      $(commentBox).find('textarea').attr('placeholder','Write your reply...');
      $(commentBox).find('form').attr("data-parent-id",parentId);
      $(commentBox).find('form').attr("data-isreply",true);
      $(replyingToBox).insertBefore(commentBox);
      scrollToCommentBox();
  });

  $(document).on('click', '.post-view-comment-replies-btn', function(){
    getComments(url=$(this).attr("data-url"), container=$(this).closest('.comment-replies'));
    if(!$(this).closest('.view-replies-btn-ctr').siblings('.view-replies-btn-ctr').length){
      let replyContainerInitBtn = $(this);
      let currentRepliesCountText = $(replyContainerInitBtn).find('.replies-count-text').text();
      $(replyContainerInitBtn).attr('data-reply-count', currentRepliesCountText);
      $(replyContainerInitBtn).removeClass('post-view-comment-replies-btn').addClass('post-toggle-replies-btn');
      $(replyContainerInitBtn).find('.replies-count-text').html('Hide replies');
    } else {
      $(this).closest('.view-replies-btn-ctr').remove();
    }

  })

  $(document).on('click', '.post-toggle-replies-btn', function(){
    let repliesContainer = $(this).closest('.comment-replies');
    let tempDataText = $(this).find('.replies-count-text').text();
    $(this).find('.replies-count-text').text($(this).attr('data-reply-count'));
    $(this).attr('data-reply-count', tempDataText);
    $(repliesContainer).find('.comment-object').toggle();
    $(repliesContainer).find('.view-replies-btn-ctr.more').toggle();
  })


  $(document).on('click', '.comment-button-ctr', function (e){
    e.stopImmediatePropagation();
    e.preventDefault();
    $(this).closest('.post-details-view').siblings('.comment-box').toggle();
  })
  $(document).on("keyup", ".post-comment-textarea", function (e){
    if (e.keyCode === 13 && !e.shiftKey) { 
      if($(this).value != undefined){
        $(this).closest('form').submit();  
      }              
      } else {
          autosize(this);
      }
  })

  $(document).on('submit','.post-comment-inline-form', function(e){
    e.preventDefault();
    e.stopImmediatePropagation();
    let isReply = $(this).attr('data-isreply');
    if(isReply == "true"){
      postComment(commentBox=undefined, form=$(this), isReply="true", parent_comment_id=$(this).attr('data-parent-id'));
    } else {
      postComment(commentBox=undefined, form=$(this));
    }
  });

  $(document).on("click", ".post-show-liked-by", function (e) {
    e.preventDefault();
    e.stopPropagation();
    $.ajax({
      url: $(this).attr("data-url"),
      type: "GET",
      dataType: "json",
      beforeSend: function () {
        $("#modal-post-list").modal("show");
      },
      success: function (data) {
        $("#modal-post-list .modal-content").html(data.html);
      },
    });
  });

  $(document).on("click", ".post-data-infinite-link", function (e) {
    var btn = $(this);
    e.preventDefault();
    e.stopImmediatePropagation();
    $.ajax({
      url: $(btn).attr("data-url"),
      type: "GET",
      dataType: "json",
      beforeSend: function () {
        $(btn).closest(".modal-infinite").append(greySpinnerMed);
      },
      success: function (data) {
        $(btn).closest(".modal-infinite").find('.grey-spinner-md').remove();
        $(btn).closest(".modal-infinite").find('.list-ctr').append(data.list);
        $(btn).closest('.scroll-infinite-link')[0].scrollTop -= 100
        if(data['has_next']){
          $(btn).attr("data-url",`/post/${data['guid_url']}/liked_by/?page=${data['next_page_number']}`);
        } else {
          $(btn).remove();
        }
        
      },
      error: function (rs, e) {
        console.log(rs.responeText);
      },
    });
  });

  function resize (textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight+'px';
  }

  function delayedResize (textarea) {
    window.setTimeout(resize(textarea), 0);
  }

  function scrollToCommentBox() {
    $('html,body').animate({
      scrollTop: $("#comment-box-jc").offset().top - 150},
    'slow');
  }

  function createViewRepliesButton(id, repliesCount, pageNumber){
    let repliesCountReplacement = repliesCountContainer = null;
    pageNumber == undefined ? pageNumber = '' : true
    repliesCount == undefined ? repliesCountReplacement = " more " : repliesCountReplacement = ' '
    repliesCount != undefined ? repliesCountContainer = `<span class="replies-count-container">(${repliesCount})</span>` : repliesCountContainer = '';
    let repliesButton = `<div class="mt-1 view-replies-btn-ctr ${repliesCountReplacement}">
                          <button class="btn btn-sm no-outline post-view-comment-replies-btn" data-url="/post/comment/${id}/replies${pageNumber}" type="button">
                            <span class="d-flex align-items-center text-muted-jc font-weight-bold-jc underline-text">
                              <span class="horizontal-line-sm border-top border-bottom"></span>
                              <span class="font-auto-xl replies-count-text">View${repliesCountReplacement}replies ${repliesCountContainer}</span>
                            </span>
                          </button>
                        </div>`
    return repliesButton
  }

  function swapCommentViewerButton(comment, replyCount){
    let commentReplyViewerBtn = $(comment).siblings('.view-replies-btn-ctr:not(.more)');
    if(commentReplyViewerBtn.length){
      if(replyCount == 0){ // if there aren't any replies - remove show/more replies button
        $(comment).siblings('.view-replies-btn-ctr').remove();
      } else if($(commentReplyViewerBtn).find('.replies-count-text').text() == 'Hide replies'){
        $(commentReplyViewerBtn).find('button').attr('data-reply-count',`View replies (${replyCount})`);
      } else {
        $(commentReplyViewerBtn).find('.replies-count-text').text(`View replies (${replyCount})`)
      }
    } 
  }

  function createCommentObj(comment, isReply){
    let likedClass = viewRepliesButton = null;  
    comment.viewer_has_liked ? likedClass = "text-red-jc" : likedClass = "text-muted-jc";
    comment.has_replies ? viewRepliesButton = createViewRepliesButton(comment.hashed_id, comment.replies_count) : viewRepliesButton = '';
    let commentObj = `
          <div class="comment-object my-1 is-reply-${isReply}">
            <div class="comment-ctr d-flex">
              <div class="user-image mr-1">
                <div class="commentor-image">
                  <img class="rounded-circle" src="${comment.name_image_url}" width="30px" height="30px">
                </div>
              </div>
              <div class="w-100 comment-content">
                <div class="d-flex justify-content-between comment-items">
                  <div class="d-flex comment-user-body">  
                    <span class="commenter-username mx-1">
                      <a href="/u/${comment.name_username}/" class="text-dark">
                        <span class="commenter-username-font">
                          ${comment.name_username}
                          </span>                      
                      </a>
                      <span class="comment-body">
                        <span class="font-auto-sm">
                          ${comment.body}
                        </span>
                      </span>
                    </span>
                  </div>
                  <div class="comment-options-ctr">
                      <div class="dropdown comment-dropdown-options mr-1">
                        <button class="btn btn-sm post-comment-dropdown-options-btn px-0 float-left" data-url="/post/comment/${comment.hashed_id}/options/" type="button" id="d_li" data-toggle="dropdown" aria-haspopup="true"
                          aria-expanded="false">
                          <i class="fas fa-ellipsis-h text-muted-jc"></i>
                        </button>
                        <div class="dropdown-menu dropdown-menu-right mt-1" aria-labelledby="d_li"></div>
                      </div>
                  </div>
                </div>
                <div>
                  <div class="comment-actions">
                    <div class="d-flex align-items-center">
                      <div class="comment-time font-auto-xl ml-1 d-flex align-items-bottom">
                        <span class="btn p-0 no-outline border-0 no-click">
                          <span class="font-auto-xl text-muted-jc">
                            ${comment.timestamp}
                          </span>                
                        </span>
                      </div>
                      <div class="separator-comments mx-1">
                        <span class="text-muted font-auto-xl">
                          ·
                        </span>
                      </div>
                      <div class="comment-like font-auto-sm">
                        <div class="comment-like-action-ctr">
                          <button class="p-0 post-comment-like-btn btn btn-sm no-outline" data-url="/post/comment/${comment.hashed_id}/like/">
                            <span class="${likedClass}">
                              <span class="like-count font-auto-xl">
                                ${comment.like_count}
                              </span>
                              <span class="like-btn-text font-auto-xl">
                                <span class="font-weight-bold-jc fade-text">
                                  Like
                                </span>              
                              </span>
                            </span>
                          </button>
                        </div>
                      </div>
                      <div class="separator-comments mx-1">
                        <span class="text-muted font-auto-xl">
                          ·
                        </span>
                      </div>
                      <div class="comment-reply font-auto-sm mr-2 p-0">
                        <div class="comment-reply-action-ctr">
                          <button class="p-0 post-comment-reply-btn btn btn-sm no-outline" data-parent-id="${comment.hashed_id}" data-parent-author=${comment.name_username} data-isreply="true">
                            <span class="reply-btn-text font-auto-xl text-muted-jc font-weight-bold-jc fade-text">
                              Reply
                            </span>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="comment-replies">
                    ${viewRepliesButton}
                </div>
              </div>
            </div>
          </div>
          `
          return commentObj;
  }
  

  function getComments(url, container) {
    let parentContainer = isReply = null;
    url === undefined ? commentGetUrl = $('#post-comments-single-view').attr('data-url') : commentGetUrl = url;
    container === undefined ? parentContainer = $('#post-comments-single-view') : parentContainer = $(container);
    parentContainer.hasClass('comment-replies') ? isReply = true : isReply = false;
    $.ajax({
      url: commentGetUrl,
      type: "get",
      dataType: "json",
      beforeSend: function () {
        $(parentContainer).append(greySpinnerMed);
      },
      success: function (data) {      
        $(parentContainer).find('.grey-spinner-md').remove();    
        let nextPageButton = null;
        let comments = data['comments']
        if(!comments.length < 1){
          for(i in comments){
            let comment = comments[i]
            let commentObj = createCommentObj(comment,isReply)
            $(parentContainer).append(commentObj)
          }
          if(!isReply){
            if(data.has_next) {
              let nextPageUrl = url.split('?')[0] + `?page=${data['page_number']+1}`
              nextPageButton = `<div class="my-1 comment-list-actions"><button data-url="${nextPageUrl}" class="btn no-outline p-0 btn-sm small text-dark font-weight-bold-jc view-more-comments-btn">
              <span class="underline-text" style="font-size:12px !important;">Load more comments</span></button>
              <span>.</span><button class="btn btn-sm no-outline p-0 mx-1 small text-dark font-weight-bold-jc scroll-to-comment-box" >
              <span class="underline-text" style="font-size:12px !important;">Write a comment</span></button></div>` 
            } else {
              nextPageButton = `<div class="comment-list-actions my-1"><button class="btn btn-sm no-outline p-0 mx-1 small text-dark font-weight-bold-jc scroll-to-comment-box" >
              <span class="underline-text" style="font-size:12px !important;">Write a comment</span></button></div>` 
            }
          } else {
            if(data.has_next){
              let nextPageNumber = `?page=${data['page_number']+1}`
              nextPageButton = createViewRepliesButton(id=data['parent_hashed_id'], repliesCount=undefined,pageNumber=nextPageNumber)
            }
          }
          $(parentContainer).append(nextPageButton)
        } else {
          let emptyMessageContainer = `<div class="show-empty-message-ctr">
          <div class="d-flex justify-content-center pt-2 my-2">
              <div>
                  <h6>No comments to show</h6>
              </div>
            </div>
          </div>`
        $(parentContainer).append(emptyMessageContainer);
        }

      },
    });
  }

  function postComment(commentBox, form, isReply, parent_comment_id){
    let commentForm = postCommentBox = formData = null;
    if(form === undefined){
      commentForm = $(commentBox).closest('.post-comment-inline-form');
      postCommentBox = $(commentBox).closest('.comment-box').siblings('.post-comments-display');
    } else {
      commentForm = $(form);
      postCommentBox = $(form).closest('.comment-box').siblings('.post-comments-display');
    }
    formData = $(commentForm).serializeArray();
    if(isReply == "true"){
      formData.push({name:"isReply", value:"true"});
      formData.push({name:"parent_comment_id", value:parent_comment_id});
    }
    $.ajax({
      url: $(commentForm).attr('data-url'),
      type: 'POST',
      data: formData,
      dataType: 'json',
      success: function(data) {
        let commentObj = createCommentObj(data.comment)
        $(postCommentBox).siblings('.comment-box').addClass('border-bottom');
        $(postCommentBox).siblings('.comment-box').find('textarea').val('');
        if(isReply == "true"){
          $('.post-cancel-reply-btn').click();
          let firstReply = $(parentCommentBox).find('.view-replies-btn-ctr:first');
          if(firstReply.length){
            $(commentObj).insertAfter(firstReply);
          } else{
            $(parentCommentBox).prepend(commentObj)
          }
        }else {
          let firstComment = $(postCommentBox).find('.comment-object:first');
          firstComment.length ? $(commentObj).insertBefore(firstComment) : $(postCommentBox).prepend(commentObj);
          let newCount = null;
          $('#post-detail').length != 0 ? newCount = `${data.post_comment_count} Comments` : newCount = `View ${data.post_comment_count} comments`;
          let commentCounts = $(postCommentBox).siblings('.post-details-view').find('.post-counts');
          if($(commentCounts).find('.comment-count').length > 0){
            $(commentCounts).find('.comment-count').html(newCount);
          } else {
            $(commentCounts).find('.comment-count-ctr').html(`<a class="comment-count small ml-1 text-muted-jc" href="/post/${data.post_guid_url}/">${newCount}</a>`)
          }
        }

      },
      error: function(rs, e){
          console.log(e)
        },
    });
  }

  function autosize(commentTextArea) {
    try {
      setTimeout(function(){
          let rows = $(commentTextArea).val().split("\n");
          $(commentTextArea).prop('rows', rows.length);
        },0);
    } catch (error) {
      return true;
    }
  }

});

/*
 * Takes user to a posts main page when clicking on content
 */
$(document).on("click", ".post-details-view", function () {
  var url = $(this).attr("data-url");
  document.location.href = url;
});

/*
 * Prevents the action of parent div in post container which takes user to post detail page
 */
$(document).on("click", ".p_ico", function (event) {
  event.stopPropagation();
});



$(document).ready(function () {
  
  $(".post-ctr").on("click", ".show-comments", function (e) {
    e.preventDefault();
    $.ajax({
      url: $(this).data("url"),
      type: "get",
      dataType: "json",
      success: function (data) {
        $("#modal-post-list .modal-content").html(data.html);
        $("#modal-post-list").modal("show");
      },
    });
  });
});

$(document).ready(function () {
  $(".post-ctr textarea").keyup(function (e) {
    var rows = $(this).val().split("\n");
    $(this).prop("rows", rows.length);
  });
  $(".post-ctr").on("click", "#post-comment-button-viewer", function () {
    $("textarea").val("");
    $("#post-comment-form-div").fadeIn();
  });
  if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
  }
});


$(document).ready(function (e) {
  $(".bookmarked-link").on("click", function (e) {
    e.preventDefault();
    e.stopImmediatePropagation();
    window.location = $(this).attr("data-url");
    return false;
  });
});

$(document).on("click", ".etbm_btnall", function (e) {
  var btn = $(this);
  e.preventDefault();
  e.stopImmediatePropagation();
  $.ajax({
    type: "POST",
    url: $(this).attr("data-url"),
    dataType: "json",
    data: $(this).closest("form").serialize(),
    success: function (data) {
      $(btn).closest(".bm_allctr").html(data.html_form);
    },
    error: function (rs, e) {
      console.log(rs.responeText);
    },
  });
});

$(document).ready(function () {
  var btn;
  $(".flw-tag-ctr").on("click", ".f-tag-btn", function (e) {
    btn = $(this);
    e.preventDefault();
    $.ajax({
      type: "POST",
      url: $(this).attr("data-url"),
      dataType: "json",
      data: $(btn).closest("form").serialize(),
      success: function (data) {
        $(btn).closest(".flw-tag-ctr").html(data.html_form);
      },
      error: function (rs, e) {
        console.log(rs.responeText);
      },
    });
  });
});

$(document).ready(function (e) {
  var blogrdltbtn;
  $(document).on("click", ".blogrdlt", function (e) {
    e.preventDefault();
    e.stopImmediatePropagation();
    blogrdltbtn = $(this);
    $.ajax({
      url: blogrdltbtn.attr("data-url"),
      type: "get",
      dataType: "json",
      beforeSend: function () {
        $("#modal-post-delete").modal("show");
      },
      success: function (data) {
        $("#modal-post-delete .modal-content").html(data.html_form);
      },
    });
  });
  $("#modal-post-delete").on("submit", ".blog-reply-delete-form", function (e) {
    e.preventDefault();
    e.stopImmediatePropagation();
    var form = $(this).serialize();
    $.ajax({
      url: $(this).attr("data-url"),
      type: $(this).attr("method"),
      data: form,
      dataType: "json",
      success: function (data) {
        if (data.form_is_valid) {
          $("#modal-post-delete").modal("hide");
          $("body").removeClass("modal-open");
          $(".modal-backdrop").remove();
          $(blogrdltbtn).closest(".blog-reply-card-ctr").remove();
          $(document).find(".blog-reply-count").html(data.reply_count);
        }
      },
    });
  });
});
$(document).ready(function () {
  $(".live_notify_badge").ready(function () {
    if ($(".live_notify_badge").first().text() == 0) {
      $(".live_notify_badge").hide();
    }
  });
  $(".live_notify_badge").on("DOMSubtreeModified", function () {
    if ($(".live_notify_badge").first().text() != 0) {
      $("#live-notif-c").show();
      $(".live_notify_badge").show();
    } else {
      $(".live_notify_badge").hide();
    }
  });
});
