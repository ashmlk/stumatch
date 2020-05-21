$(document).ready(function () {
    var btn_c_rmv = null;
	$('.buzz-comment-container').on("click",".shbzcmdlfrm", function (e) {
        btn_c_rmv = $(this);
        e.preventDefault();
		e.stopImmediatePropagation();
		$.ajax({
			url: $(this).attr("data-url"),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-comment-delete').modal('show');
			},
			success: function(data){
				$('#modal-comment-delete .modal-content').html(data.html_form);
			}
		});
	});

	$('#modal-comment-delete').on("submit",".cbzcmdlfrm",function (e){
		e.preventDefault();
        e.stopImmediatePropagation();
        var form = $(this).serialize();
		$.ajax({
			url: $(this).attr('data-url'),
			type: $(this).attr('method'),
			data: form,
			dataType: 'json',
			success: function(data){
				if(data.form_is_valid){
                    $(btn_c_rmv).closest(".bzrbx").remove();
                    var cm_count = parseInt(document.getElementById("_cct").innerText);
                    cm_count--;
                    document.getElementById("_cct").innerText = cm_count
					$('#modal-comment-delete').modal('hide');
					$('body').removeClass('modal-open');
					$('.modal-backdrop').remove();
				} 
			}
		})
	});
});
    