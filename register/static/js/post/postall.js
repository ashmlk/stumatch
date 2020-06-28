$(document).ready(function(){
	$(document).ajaxSend(function (event, jqxhr, settings) {
		jqxhr.setRequestHeader("X-CSRFToken", '{{ csrf_token }}');
	});
	var ShowForm = function(e){
		e.stopImmediatePropagation();
		var btn = $(this);
		$.ajax({
			url: btn.attr("data-url"),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-post').modal('show');
			},
			success: function(data){
				$('#modal-post .modal-content').html(data.html_form);
			}
		});
		return false;
	};
	var SaveForm =  function(e){
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
				if(data.form_is_valid){
					$('#modal-post').modal('hide');
					$('#_np2u').prepend(data.post);
				} else {
					$('#modal-post .modal-content').html(data.html_form)
				}
			}
		})
		return false;
	}
	$('.create-post-btn').click(ShowForm);
	$('#modal-post').on("submit",".post-create-form",SaveForm)

});

/* 
* Opens form for deleting a post 
*/
$(document).ready(function (e) {
	var veid = null;
	var btn;
	$('.post-ctr').on("click",".show-form-delete", function (e) {
		e.stopImmediatePropagation();
        btn = $(this);
        veid = $(this).data("veid");
		$.ajax({
			url: btn.attr("data-url"),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-post-delete').modal('show');
			},
			success: function(data){
				$('#modal-post-delete .modal-content').html(data.html_form);
			}
		});
	});
	$('#modal-post-delete').on("submit",".delete-form",function (e){
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
				if(data.form_is_valid){
					$('#modal-post-delete').modal('hide');
					$('body').removeClass('modal-open');
					$('.modal-backdrop').remove();  
					$(btn).closest('.post-ctr').remove();
					//$('#_pc_'+veid).remove();
				} 
			}
		})
	});
});

/* 
* Opens form for updating a post 
*/
$(document).ready(function (e) {
	var veid = null;
	$('.post-ctr').on("click",".show-form-update", function (e) {
        e.stopImmediatePropagation();
        var btn = $(this);
        veid = $(this).data("veid");
		$.ajax({
			url: btn.attr("data-url"),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-post-update').modal('show');
			},
			success: function(data){
				$('#modal-post-update .modal-content').html(data.html_form);
			}
		});
	});
	$('#modal-post-update').on("submit",".update-form",function (e){
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
				if(data.form_is_valid){
                    $('#modal-post-update').modal('hide');
					$('#_pc_'+veid).html(data.post);
				} 
			}
		})
	});
});

/*
* Takes user to a posts main page when clicking on content
*/
$(document).on('click', '.post-details-view', function () {
    var url = $(this).attr("data-url")
    document.location.href = url 
});

/*
* Prevents the action of parent div in post container which takes user to post detail page
*/
$(document).on('click', '.p_ico', function(event) {
  event.stopPropagation();
});

$(document).ready(function (e) {
    $('.post-ctr').on("click", ".likeBtn", function (e) {
        var btn = $(this)
        e.preventDefault();
        e.stopImmediatePropagation();
        var tk = $(this).attr("data-token");
        $.ajax({
            type: "POST",
            url: $(this).attr("data-url"),
            dataType: 'json',
            data: { 'csrfmiddlewaretoken':tk },
            success: function (data){
                $(btn).closest(".like-section").html(data.post_likes);
                $('#like-count-d').html(data.likescount);
            },
            error: function(rs, e){
                console.log(rs.responeText);
            },
        });
    });
});
$(document).ready(function () {
    $('.post-ctr').on("click", ".reply-btn",function () {
        $("#modal-comment-reply textarea").attr("placeholder","Add your reply")
		    $("#modal-comment-reply textarea").addClass("comment-reply-adjust")
			  var c_id = $(this).data('id');
			  $("#c-get-id").val(c_id);
			  $('textarea').val('');
			  $("#modal-comment-reply").modal("show");
			  });
	$('.post-ctr').on('click','.view-replies',function () {
			  var h = $(this).data('hidden');
			  var curr = $(this).text()
			  var newt = $(this).attr('text')
			  $(this).text(newt)
			  $(this).attr("text",curr)
			  var id = $(this).data('id');
			  if(h == 1){
				$("#c-"+id).show();
				$(this).data('hidden',0);
				} else {
				$("#c-"+id).hide();
				$(this).data('hidden',1);
				}
			});
  });
  $(document).ready(function () {
    $('.post-ctr').on("click",'.show-likes', function (e) {
      e.preventDefault();
      $.ajax({
            url: $(this).data("url"),
            type: 'get',
            dataType: 'json',
            success: function(data) {
              $('#modal-post-list .modal-content').html(data.html);
              $('#modal-post-list').modal('show');
            }
      });
    });
    $('.post-ctr').on("click", '.show-comments',function (e) {
      e.preventDefault();
      $.ajax({
            url: $(this).data("url"),
            type: 'get',
            dataType: 'json',
            success: function(data) {
              $('#modal-post-list .modal-content').html(data.html);
              $('#modal-post-list').modal('show');
            }
      });
    });
  });

  $(document).ready(function(){
	$('.post-ctr textarea').keyup(function (e) {
		var rows = $(this).val().split("\n");
		$(this).prop('rows', rows.length);
	  });
	$('.post-ctr').on("click","#post-comment-button-viewer", function(){
		$('textarea').val('')
		$("#post-comment-form-div").fadeIn();
	  });
	$('.post-ctr').on('submit','.post-comment-form', function (e) {
		e.preventDefault();
		e.stopImmediatePropagation();
		var form = $(this).serialize();
		$.ajax({
		  url: $(this).attr('data-url'),
		  type: 'POST',
		  data: form,
		  dataType: 'json',
		  success: function(data) {
			$("#like-section").html(data.likes);
			$("#post-linked-comments").html(data.comments); 
			$('textarea').val('');
		  },
		  error: function(rs, e){
					console.log(rs.responeText);
				},
		});
	  });
	  $(document).on("submit",'.comment-reply-form',function (e) {
		e.preventDefault();
		e.stopImmediatePropagation();
		var form = $(this).serialize();
		$.ajax({
		  url: $(this).attr('data-url'),
		  type: 'POST',  
		  data: form,
		  dataType: 'json',
		  success: function(data) {
			$('#modal-comment-reply').modal('hide');
			$('body').removeClass('modal-open');
			$('.modal-backdrop').remove();
			$("#like-section").html(data.likes);
			$("#post-linked-comments").html(data.comments);
			$('textarea').val('');
		  },
		  error: function(rs, e){
					console.log(rs.responeText);
				},
		})
	  });

	if ( window.history.replaceState ) {
        window.history.replaceState( null, null, window.location.href );
    }
});
$(document).ready(function () {
    var btn_c_rmv = null;
	$('#cm_all_r').on("click",".show-comment-delete-form", function (e) {
        btn_c_rmv = $(this);
        e.preventDefault();
		e.stopImmediatePropagation();
		$.ajax({
			url: $(this).attr("data-url"),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-comment-delete').modal('show');
			},
			success: function(data){
				$('#modal-comment-delete .modal-content').html(data.html_form);
			}
		});
	});

	$('#modal-comment-delete').on("submit",".comment-delete-form",function (e){
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
				if(data.form_is_valid){
					$('#modal-comment-delete').modal('hide');
					$('body').removeClass('modal-open');
					$('.modal-backdrop').remove();
					if($(btn_c_rmv).attr("data-type")=="reply"){
						$(btn_c_rmv).closest(".reply-box").remove();
						var rp_count = $("#rsrcp").val();
						alert(rp_count)
						rp_count--;
						$("#rsrcp").val(rp_count)
						document.getElementById("srfc").attr("text","Replies (" + rp_count + ")");
					} else {
						$(btn_c_rmv).closest(".comment-box").remove();
						var cm_count = parseInt(document.getElementById("cc_n").innerText);
						cm_count--;
						document.getElementById("cc_n").innerText = cm_count
					}
				} 
			}
		})
	});
});
$(document).ready(function (e) {
    $(document).on("click", ".comment-like-btn", function (e) {
        e.stopImmediatePropagation();
        e.preventDefault();
        var like_count = parseInt($(".comment-like-count", this).text());
        if($(this).find("span").hasClass("text-danger")){
            like_count--;
            $(".comment-input-like-count", this).val(like_count);
            $("span", this).removeClass("text-danger")
            $(".comment-like-count", this).text(like_count);
        } else {
            like_count++;
            $(".comment-input-like-count", this).val(like_count);
            $("span", this).addClass("text-danger")
            $(".comment-like-count", this).text(like_count); 
        }

        $.ajax({
            type:"POST",
            dataType: 'json',
            url: $(this).closest("form").attr("data-url"),     
            data: $(this).closest("form").serialize(),
            success: function (data) {
                if($(this).find("span").hasClass("text-danger")){
                    like_count--;
                    $(".comment-input-like-count", this).val(like_count);
                    $("span", this).removeClass("text-danger")
                    $(".comment-like-count", this).text(like_count);
                } else {
                    like_count++;
                    $(".comment-input-like-count", this).val(like_count);
                    $("span", this).addClass("text-danger")
                    $(".comment-like-count", this).text(like_count); 
                }

            },
            error: function(rs, e){
                console.log(rs.responeText);
            },
        });
    });
});
$(document).ready(function (e) {
	var btn;
	$('#blog-list').on("click",".show-form-delete", function (e) {
	  e.stopImmediatePropagation();
	  btn = $(this);
	  $.ajax({
		url: btn.attr("data-url"),
		type: 'get',
		dataType:'json',
		beforeSend: function(){
		  $('#modal-post-delete').modal('show');
		},
		success: function(data){
		  $('#modal-post-delete .modal-content').html(data.html_form);
		}
	  });
	});
	$('#modal-post-delete').on("submit",".blog-delete-form",function (e){
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
		  if(data.form_is_valid){
			$('#modal-post-delete').modal('hide');
			$('body').removeClass('modal-open');
			$('.modal-backdrop').remove();  
			$(btn).closest('.blog-ctr').remove();
		  } 
		}
	  })
	});
  });
  $(document).ready(function (e) {
	$('.bookmarked-link').on('click', function (e) {
	  e.preventDefault();
	  e.stopImmediatePropagation();
	  window.location = $(this).attr('data-url');
	  return false;
	})
	$('#blog-detail').on("click", ".blog_likeBtn", function (e) {
		var btn = $(this)
		e.preventDefault();
		e.stopImmediatePropagation();
		$.ajax({
			type: "POST",
			url: $(this).attr("data-url"),
			dataType: 'json',
			data: $(this).closest("form").serialize(),
			success: function (data){
				$(btn).closest(".blog-like-section").html(data.blog_likes);
			},
			error: function(rs, e){
				console.log(rs.responeText);
			},
		});
	  });
	  $('.blog-reply-card-ctr ').on("click", ".blogreply_likeBtn", function (e) {
		var btn = $(this)
		e.preventDefault();
		e.stopImmediatePropagation();
		$.ajax({
			type: "POST",
			url: $(this).attr("data-url"),
			dataType: 'json',
			data: $(this).closest("form").serialize(),
			success: function (data){
				$(btn).closest(".blog-reply-like-section").html(data.reply_likes);
			},
			error: function(rs, e){
				console.log(rs.responeText);
			},
		});
	  });
	$(document).on("click", ".etbm_btnall", function (e) {
		  var btn = $(this)
		  e.preventDefault();
		  e.stopImmediatePropagation();
		  $.ajax({
			  type: "POST",
			  url: $(this).attr("data-url"),
			  dataType: 'json',
			  data: $(this).closest("form").serialize(),
			  success: function (data){
				  $(btn).closest(".bm_allctr").html(data.html_form);
			  },
			  error: function(rs, e){
				  console.log(rs.responeText);
			  },
		  });
	  });
	})
