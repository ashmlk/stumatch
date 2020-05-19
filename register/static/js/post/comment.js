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
