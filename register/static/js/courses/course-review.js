$(document).ready(function(){

	var anon_or_not = ''
	$(document).on('click', '.rw-submit-btn', function () {
		anon_or_not = $(this).attr('data-value');

	});
	
	$(document).on('submit','.course-review-form', function (e) {
		e.preventDefault();
		e.stopImmediatePropagation();
		var form = $(this).serializeArray();
		form.push({name: "rw_submit", value:anon_or_not});
		$.ajax({
		  url: $(this).attr('data-url'),
		  type: 'POST',
		  data: form,
		  dataType: 'json',
		  success: function(data) {
            $("#new-review-s").prepend(data.review); 
			$("#new-review-a").prepend(data.review);
			$(".no-review-box").remove();
            $("#crsrwalcts").html(data.reviews_all_count)
            $("#crsspecrw").html(data.reviews_count)
			$('#crwfrmcntr').find(form).remove()
			$('#crwfrmcntr').html('<p class="text-muted text-center">Your review was successfully submitted. You can only write one review per course for each instructor.</p>')
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

$(document).ready(function (e) {
    var veid = null;
	$('.c-review-list').on("click",".show-form-delete", function (e) {
		e.stopImmediatePropagation();
        var btn = $(this);
        veid = $(this).data("veid");
		$.ajax({
			url: btn.attr("data-url"),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-review-delete').modal('show');
			},
			success: function(data){
				$('#modal-review-delete .modal-content').html(data.html_form);
			}
		});
	});
	$('#modal-review-delete').on("submit",".delete-form",function (e){
		e.preventDefault();
		e.stopImmediatePropagation();
		var form = new FormData(this);
		$.ajax({
			url: $(this).attr('data-url'),
			type: $(this).attr('method'),
			data: form,
			cache: false,
			processData: false,
			contentType: false,
			dataType: 'json',
			success: function(data){
				let parent_ctr = $('#_rc_'+veid).closest('.course-reviews-list')
				if(data.form_is_valid){
					$('#modal-review-delete').modal('hide');
					$('body').removeClass('modal-open');
					$('.modal-backdrop').remove();  
                    $('#_rc_'+veid).remove();
					$("#crsrwalcts").html(data.reviews_all_count)
					$("#crsspecrw").html(data.reviews_count)
					if(data.can_review){
						$('#crwfrmcntr').html(data.review_form);
					}
					if($('#course-all-reviews-shown').length){
						if(!$(parent_ctr).find('.course-review-object').length){
							$(parent_ctr).closest('.review-group-container').remove();
							if(!$(document).find('.review-group-container').length){
								let emptyMessage = `
								<div class="no-review-box">
									<div class="d-flex justify-content-center pt-2 my-2">
										<div>
											<h6>No reviews to show</h6>
										</div>
									</div>
								</div>
								`
								$('.c-review-list').html(emptyMessage)
							}
						}
					}
                }
                else{
                    $('#modal-review-delete .modal-content').html(data.html_form);
                } 
			}
		})
	});
});
