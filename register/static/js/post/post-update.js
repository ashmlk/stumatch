$(document).ready(function (e) {
    var veid = null;
	$('#post-list').on("click",".show-form-update", function (e) {
        e.stopImmediatePropagation();
        var btn = $(this);
        veid = $(this).data("veid");
		$.ajax({
			url: btn.attr("data-url"),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-post-update').modal('show');
			},
			success: function(data){
				$('#modal-post-update .modal-content').html(data.html_form);
			}
		});
	});
	$('#modal-post-update').on("submit",".update-form",function (e){
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
                    $('#modal-post-update').modal('hide');
					$('#_pc_'+veid).html(data.post);
				} 
			}
		})
	});
});
