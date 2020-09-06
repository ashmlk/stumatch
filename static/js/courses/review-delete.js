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
				if(data.form_is_valid){
					$('#modal-review-delete').modal('hide');
					$('body').removeClass('modal-open');
					$('.modal-backdrop').remove();  
                    $('#_rc_'+veid).remove();
					$("#review-all-tab").find("span").text(data.reviews_all_count)
					$("#review-spec-tab").find("span").text(data.reviews_count)
                }
                else{
                    $('#modal-review-delete .modal-content').html(data.html_form);
                } 
			}
		})
	});
});
