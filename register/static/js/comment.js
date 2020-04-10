$(document).ready(function(){
	$('textarea').keyup(function (e) {
		var rows = $(this).val().split("\n");
		$(this).prop('rows', rows.length);
	  });
	var s = 0;
	var l = 0;
	$("#post-comment-button-viewer").click(function(){
		if(s == 0){
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
				$('#modal-comment-reply').modal('hide');
			},
			error: function(rs, e){
                console.log(rs.responeText);
            },
		})
	})
});