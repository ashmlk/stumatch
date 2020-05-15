$(document).ready(function(){
	$('textarea').keyup(function (e) {
		var rows = $(this).val().split("\n");
		$(this).prop('rows', rows.length);
	  });
	$("#post-comment-button-viewer").on("click", function(){
		$('textarea').val('')
		$("#post-comment-form-div").fadeIn();
	  });
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
