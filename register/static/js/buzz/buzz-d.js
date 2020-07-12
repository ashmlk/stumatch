$('.b_dlfx').ready( function () {
     $('.b_actb').on("click", function () {
         $('#modal-buzz-c').modal('show');
	 })
	 maxCharacters = 180;
	 $('#count').text(maxCharacters);
	 $('#id_reply_content').bind('keyup keydown', function() {
		 var count = $('#count');
		 var characters = $(this).val().length;
		 if (characters >= maxCharacters) {
			 count.addClass('text-danger');
		 } else {
			 count.removeClass('text-danger');
		 }
		 count.text(maxCharacters - characters);
	 });
     $(document).on('submit', '.buzz-d-c', function (e) {
        e.preventDefault();
		e.stopImmediatePropagation();
		var form = $(this).serialize();
		$.ajax({
			url: $(this).attr('data-url'),
			type: 'POST',
			data: form,
			dataType: 'json',
			success: function(data){
				$('#modal-buzz-c').modal('hide');
				$('#bznwre_').prepend(data.reply);
				$('#_cct').text(data.r_count);
				$('textarea').val('');
				$('#id_reply_nickname').val('');
			},
			error: function(rs, e){
				console.log(rs.responeText);
			},
		})
     })
});