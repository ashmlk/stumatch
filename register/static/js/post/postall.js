$(document).ready(function(){

	/*
	$(document).ajaxSend(function (event, jqxhr, settings) {
		jqxhr.setRequestHeader("X-CSRFToken", '{{ csrf_token }}');
	});
	*/

	$(document).on('click', '.create-post-btn', function (e){
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
	})

	
	$('#modal-post').on("submit",".post-create-form", function (e){
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
	})
	
	
});

/* 
* Opens form for deleting a post 
*/
$(document).ready(function (e) {
	var veid = null;
	var btn;
	$(document).on("click",".show-form-delete", function (e) {
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
	$(document).on("click",".show-form-update", function (e) {
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
    $(document).on("click", ".likeBtn", function (e) {
        var btn = $(this)
        e.preventDefault();
        e.stopImmediatePropagation();
        var tk = $(this).attr("data-token");
        $.ajax({
            type: "POST",
            url: $(this).attr("data-url"),
            dataType: 'json',
            data: $(btn).closest('form').serialize(),
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
	/*
    $('.post-ctr').on("click", ".reply-btn",function () {
        $("#modal-comment-reply textarea").attr("placeholder","Add your reply")
		    $("#modal-comment-reply textarea").addClass("comment-reply-adjust")
			  var c_id = $(this).data('id');
			  $("#c-get-id").val(c_id);
			  $('textarea').val('');
			  $("#modal-comment-reply").modal("show");
			  });
	*/
	$('.post-ctr').on('click','.view-replies',function (e) {
			e.stopImmediatePropagation();
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

$(document).ready(function(){
	$(document).on('submit','.post-comment-form', function (e) {
		e.preventDefault();
		e.stopImmediatePropagation();
		var form = $(this).serialize();
		$.ajax({
		  url: $(this).attr('data-url'),
		  type: 'POST',
		  data: form,
		  dataType: 'json',
		  success: function(data) {
			var i = parseInt($('#cc_n').text());
			i++;
			$('#cc_n').text(i)
			$('#panc_q').prepend(data.comment)
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
		var uuid = $(this).attr('data-target')
		$.ajax({
		  url: $(this).attr('data-url'),
		  type: 'POST',  
		  data: form,
		  dataType: 'json',
		  success: function(data) {
			$('#c-'+uuid).find('.rp_container_new').prepend(data.reply)
			var r_c = parseInt($(document).find('.cr_rb_'+uuid).attr('data-value'));
			r_c++;
			var new_text = "Replies  "+r_c;
			$(document).find('.cr_rb_'+uuid).attr('text',new_text);
			$(document).find('.cr_rb_'+uuid).attr('data-value',r_c);
			$('textarea').val('');
		  },
		  error: function(rs, e){
					console.log(rs.responeText);
				},
		})
	  });
});
$(document).ready(function (e) {
    var form_c_like;
    $(document).on("submit", ".post-comment-like-form", function (e) {
        form_c_like = $(this)
        e.stopImmediatePropagation();
        e.preventDefault();
        $.ajax({
            type:"POST",
            dataType: 'json',
            url: $(this).attr("data-url"),     
            data: $(this).serialize(),
            success: function (data) {
                var k = $(form_c_like).closest('.clcntr').html(data.comment)
            },
            error: function(rs, e){
                console.log(rs.responeText);
            },
        });
    });
})
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
	$(document).on("click", ".blog_likeBtn", function (e) {
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
	$(document).on("click", ".blogreply_likeBtn", function (e) {
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
	$(document).on("submit", '.blog-reply-form', function (e) {		
		e.preventDefault();
		e.stopImmediatePropagation();
		var form = $(this).serialize();
		$.ajax({
			type: "POST",
			url: $(this).attr("data-url"),
			dataType: 'json',
			data: form,
			success: function (data){	
				$(document).find('.blog-reply-count').html(data.reply_count);				
				$(document).find('.blog-replies-list').prepend(data.new_reply);
				$(document).find('#id_content').val('');	
			},
			error: function(rs, e){
				console.log(rs.responeText);
				},
			});
		});
})

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

$(document).ready(function () {
	var btn;
	$('.flw-tag-ctr').on("click", ".f-tag-btn", function (e) {
		btn = $(this)
		e.preventDefault();
		$.ajax({
			type: "POST",
			url: $(this).attr("data-url"),
			dataType: 'json',
			data: $(btn).closest('form').serialize(),
			success: function (data){
			$(btn).closest('.flw-tag-ctr').html(data.html_form)
			},
			error: function(rs, e){
				console.log(rs.responeText);
			},
		});
	});
})
$(document).ready(function () {
	$(document).on('click', '.post-comment-infinite-link', function (e){
	  var btn = $(this);
	  e.preventDefault();
	  e.stopImmediatePropagation();
	  $.ajax({
		url:  $(btn).attr('data-url'),
		type: "GET",
		dataType: 'json',
		success: function (data){
		  $(btn).closest('.modal-infinite').append(data.list);
		  $(btn).remove();
		},
		error: function(rs, e){
		  console.log(rs.responeText);
		},
	  })
	})
  })

  $(document).ready(function (e) {
	var blogrdltbtn;
	$(document).on("click",".blogrdlt", function (e) {
	  e.preventDefault();
	  e.stopImmediatePropagation();
	  blogrdltbtn = $(this);
	  $.ajax({
		url: blogrdltbtn.attr("data-url"),
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
	$('#modal-post-delete').on("submit",".blog-reply-delete-form",function (e){
	  e.preventDefault();
	  e.stopImmediatePropagation();
	  var form = $(this).serialize();
	  $.ajax({
		  url: $(this).attr('data-url'),
		  type: $(this).attr('method'),
		  data: form,
		  dataType: 'json',
		  success: function(data){
			if(data.form_is_valid){
			$('#modal-post-delete').modal('hide');
			$('body').removeClass('modal-open');
			$('.modal-backdrop').remove();  
			$(blogrdltbtn).closest('.blog-reply-card-ctr').remove();
			$(document).find('.blog-reply-count').html(data.reply_count);
			} 
		  }
	  })
	});
  });

  