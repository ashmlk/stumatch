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
					$(btn_c_rmv).closest(".comment-box").remove();
					var cm_count = parseInt(document.getElementById("cc_n").innerText);
					cm_count--;
					document.getElementById("cc_n").innerText = cm_count
				} 
			}
		})
	});
});
/*
$(document).ready(function (e) {
    var btn = null;
	$('#cm_all_r').on("click",".show-comment-delete-form", function (e) {
        e.preventDefault();
        var btn = $(this);
        veid = btn.data("veid");
		$.ajax({
			url: btn.attr("data-url"),
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
	$('#modal-comment-delete').on("click",".comment-delete-form",function (e){
		e.preventDefault();
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
                    $(btn).closest(".comment-box").remove()
					var cm_count = parseInt(document.getElementById("cc_n").innerText);
					cm_count--;
					document.getElementById("cc_n").innerText = cm_count
				} 
			}
		})
    });
});
*/