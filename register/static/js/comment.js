$(document).ready(function(){
	$('textarea').keyup(function (e) {
		var rows = $(this).val().split("\n");
		$(this).prop('rows', rows.length);
	  });
	var s = 0;
	var l = 0;
	$("#post-comment-button-viewer").click(function(){
		if(s == 0){
			$('textarea').val('')
			$("#post-comment-form-div").fadeIn();
			s = -1;
		} else {
			$("#post-comment-form-div").fadeOut();
			s = 0;
		}
	  })
	$('.inside-post-detail #likeBtn').on("click", function (e) {
		e.preventDefault();
		if($(".inside-post-detail #likeBtn i").hasClass("fa-thumbs-up")){
			($(".inside-post-detail #likeBtn i").removeClass("fa-thumbs-up"))
			($(".inside-post-detail #likeBtn i").addClass("fa-thumbs-down"))
		} else {
			($(".inside-post-detail #likeBtn i").removeClass("fa-thumbs-down"))
			($(".inside-post-detail #likeBtn i").addClass("fa-thumbs-up"))
		}
	})
	$(".post-comment-form").on("submit", function (e) {
		e.preventDefault();
		e.stopImmediatePropagation();
		$.ajax({
			type:'POST',
			url: $(this).attr('action'),
			data: $(this).serialize(),
			dataType: 'json',
			success: function(data) {
				$("#post-linked-comments div").html(data.comments)
				$('textarea').val('')
				$('.reply-btn').on("click", function () {
					$("#modal-comment-reply textarea").attr("placeholder","Add your reply")
					$("#modal-comment-reply textarea").addClass("comment-reply-adjust")
					var c_id = $(this).data('id');
					$("#c-get-id").val(c_id);
					$('textarea').val('');
					$("#modal-comment-reply").modal("show");
				  });
				  $('.view-replies').on('click', function () {
					var curr = $(this).text()
					var newt = $(this).attr('text')
					$(this).text(newt)
					$(this).attr("text",curr)
					var id = $(this).data('id');
					  if(l == 0){
						$("#c-"+id).show();
						l = -1;
					  } else {
						$("#c-"+id).hide();
						l = 0;
					  }
					});
					$(".comment-reply-form").on("submit", function () {
						$('.post-comment-form textarea').val('');
						$(this).submit();
						$("modal-comment-reply").modal("hide");
					})
			},
			error: function(rs, e){
                console.log(rs.responeText);
            },
		})
	})

	$("#modal-comment-reply textarea").attr("placeholder","Add your reply")
    $("#modal-comment-reply textarea").addClass("comment-reply-adjust")
    $('.reply-btn').on("click", function () {
		var c_id = $(this).data('id');
		$('textarea').val('');
		$("#c-get-id").val(c_id);
    	$("#modal-comment-reply").modal("show");
	});
	$(".comment-reply-form").on("submit", function () {
		$(this).submit();
		$("modal-comment-reply").modal("hide");
	});
    $('.view-replies').on('click', function () {
      var curr = $(this).text()
	  var newt = $(this).attr('text')
	  $(this).text(newt)
	  $(this).attr("text",curr)
	  var id = $(this).data('id');
      if(l == 0){
		$("#c-"+id).show();
        l = -1;
      } else {
        $("#c-"+id).hide();
        l = 0;
      }
	});
	if ( window.history.replaceState ) {
        window.history.replaceState( null, null, window.location.href );
    }
});