$(document).ready(function () {
    var btn_c_rmv = null;
	$('#cm_all_r').on("click",".show-comment-delete-form", function (e) {
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

	$('#modal-comment-delete').on("submit",".comment-delete-form",function (e){
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
					$('#modal-comment-delete').modal('hide');
					$('body').removeClass('modal-open');
					$('.modal-backdrop').remove();
					if($(btn_c_rmv).attr("data-type")=="reply"){
						$(btn_c_rmv).closest(".reply-box").remove();
						var rp_count = $("#rsrcp").val();
						alert(rp_count)
						rp_count--;
						$("#rsrcp").val(rp_count)
						document.getElementById("srfc").attr("text","Replies (" + rp_count + ")");
					} else {
						$(btn_c_rmv).closest(".comment-box").remove();
						var cm_count = parseInt(document.getElementById("cc_n").innerText);
						cm_count--;
						document.getElementById("cc_n").innerText = cm_count
					}
				} 
			}
		})
	});
});
    