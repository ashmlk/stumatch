$(document).ready(function(){
	$(document).on('submit','.course-review-form', function (e) {
		e.preventDefault();
		e.stopImmediatePropagation();
		var form = $(this).serialize();
		$.ajax({
		  url: $(this).attr('data-url'),
		  type: 'POST',
		  data: form,
		  dataType: 'json',
		  success: function(data) {
            $("#new-review-s").prepend(data.review); 
			$("#new-review-a").prepend(data.review);
			$(".no-review-box").remove();
            $("#review-all-tab").find("span").text(data.reviews_all_count)
            $("#review-spec-tab").find("span").text(data.reviews_count)
            $('textarea').val('');
		  },
		  error: function(rs, e){
					console.log(rs.responeText);
				},
		});
	  });
	if ( window.history.replaceState ) {
        window.history.replaceState( null, null, window.location.href );
    }
});