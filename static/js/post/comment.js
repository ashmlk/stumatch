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
