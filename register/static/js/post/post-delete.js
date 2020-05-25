$(document).ready(function (e) {
    var veid = null;
	$('.post-ctr').on("click",".show-form-delete", function (e) {
		e.stopImmediatePropagation();
        var btn = $(this);
        veid = $(this).data("veid");
		$.ajax({
			url: btn.attr("data-url"),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-post-delete').modal('show');
			},
			success: function(data){
				$('#modal-post-delete .modal-content').html(data.html_form);
			}
		});
	});
	$('#modal-post-delete').on("submit",".delete-form",function (e){
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
					$('#modal-post-delete').modal('hide');
					$('body').removeClass('modal-open');
					$('.modal-backdrop').remove();  
					$('#_pc_'+veid).remove();
				} 
			}
		})
	});
});
