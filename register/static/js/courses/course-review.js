$(document).ready(function(){
    $('.v_rebtn').on("click", function () {
        if ($(this).data("text") == "Show"){
            $('.review-textbox').show();
            $(this).data('text',"Hide");
        }
        else if ($(this).data("text") == "Hide"){
            $('.review-textbox').hide();
            $(this).data('text',"Show");
        }
    })
	$('.course-review-form').on('submit', function (e) {
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