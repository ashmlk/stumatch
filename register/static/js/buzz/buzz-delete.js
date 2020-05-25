$(document).ready(function (e) {
	//var veid = null;
	var btn = null
	$('.buzz-ctr').on("click",".show-form-delete", function (e) {
		e.stopImmediatePropagation();
        btn = $(this);
        //veid = $(this).data("veid");
		$.ajax({
			url: btn.attr("data-url"),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-buzz-delete').modal('show');
			},
			success: function(data){
				$('#modal-buzz-delete .modal-content').html(data.html_form);
			}
		});
	});
	$('#modal-buzz-delete').on("submit",".delete-form",function (e){
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
					$('#modal-buzz-delete').modal('hide');
					$('body').removeClass('modal-open');
					$('.modal-backdrop').remove();  
					$(btn).closest('.buzz-ctr').remove();
				} 
			}
		})
	});
});

$(document).ready(function () {
	$('.bd-gt').on("click", function () {
		var url = $(this).attr("data-url")
		document.location.href = url 
	})
})
