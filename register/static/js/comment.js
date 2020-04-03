$(document).ready(function(){
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
	$('.inside-post-detail #likeBtn').on("click", function () {
		if($(".inside-post-detail #likeBtn i").hasClass("fa-thumbs-up")){
			($(".inside-post-detail #likeBtn i").removeClass("fa-thumbs-up"))
			($(".inside-post-detail #likeBtn i").addClass("fa-thumbs-down"))
		} else {
			($(".inside-post-detail #likeBtn i").removeClass("fa-thumbs-down"))
			($(".inside-post-detail #likeBtn i").addClass("fa-thumbs-up"))
		}
	})
	$(document).on("submit",".post-comment-form", function (e) {
		e.preventDefault();
		$.ajax({
			type:'POST',
			url: $(this).attr('action'),
			data: $(this).serialize(),
			dataType: 'json',
			success: function(data) {
				$("#post-linked-comments div").html(data.comments)
				$('textarea').val('')
			},
			error: function(rs, e){
                console.log(rs.responeText);
            },
		})
	})
});