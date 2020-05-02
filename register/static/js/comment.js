$(document).ready(function(){
	$('textarea').keyup(function (e) {
		var rows = $(this).val().split("\n");
		$(this).prop('rows', rows.length);
	  });
	var s = 0;
	$("#post-comment-button-viewer").on("click", function(){
		$('textarea').val('')
		$("#post-comment-form-div").fadeIn();
	  });
	$('.inside-post-detail #likeBtn').on("click", function (e) {
		e.preventDefault();
		if($(".inside-post-detail #likeBtn i").hasClass("fa-thumbs-up")){
			$(".inside-post-detail #likeBtn i").removeClass("fa-thumbs-up").addClass("fa-thumbs-down");
		} else {
			$(".inside-post-detail #likeBtn i").removeClass("fa-thumbs-down").addClass("fa-thumbs-up");
		}
	})
	$('.post-comment-form').on('submit', function (e) {
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
			$('.reply-btn').on("click", function () {
				$("#modal-comment-reply textarea").attr("placeholder","Add your reply")
				$("#modal-comment-reply textarea").addClass("comment-reply-adjust")
				var c_id = $(this).data('id');
				$("#c-get-id").val(c_id);
				$('textarea').val('');
				$("#modal-comment-reply").modal("show");
			});
		  },
		  error: function(rs, e){
					console.log(rs.responeText);
				},
		});
	  });
	  $('.comment-reply-form').on("submit", function (e) {
		e.preventDefault();
		e.stopImmediatePropagation();
		var form = $(this).serialize();
		$.ajax({
		  url: $(this).attr('data-url'),
		  type: 'POST',  
		  data: form,
		  dataType: 'json',
		  success: function(data) {
			$('.modal').modal('hide');
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