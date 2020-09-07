$(document).ready(function(){
	$(document).ajaxSend(function (event, jqxhr, settings) {
		jqxhr.setRequestHeader("X-CSRFToken", '{{ csrf_token }}');
	});
	var ShowForm = function(e){
		e.stopImmediatePropagation();
		var btn = $(this);
		$.ajax({
			url: btn.attr("data-url"),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-buzz').modal('show');
			},
			success: function(data){
				$('#modal-buzz .modal-content').html(data.html_form);
			}
		});
		return false;
	};
	var SaveForm =  function(e){
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
					$('#modal-buzz').modal('hide');
					$('#_nb21').prepend(data.buzz);
				} else {
					$('#modal-buzz .modal-content').html(data.html_form)
				}
			}
		})
		return false;
	}
	$('.create-buzz-btn').click(ShowForm);
	$('#modal-buzz').on("submit",".buzz-create-form",SaveForm)
});





