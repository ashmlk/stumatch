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
				$('#modal-post').modal('show');
			},
			success: function(data){
				$('#modal-post .modal-content').html(data.html_form);
			}
		});
		return false;
	};
	var SaveForm =  function(e){
		var form = new FormData(this);
		e.stopImmediatePropagation();
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
					$('#post-list div').html(data.posts);
					$('#modal-post').modal('hide');
				} else {
					$('#modal-post .modal-content').html(data.html_form)
				}
			}
		})
		return false;
	}
	
//create
$('.create-post-btn').click(ShowForm);
$('#modal-post').on("submit",".post-create-form",SaveForm)

//update
$('#post-list').on("click",".show-form-update",ShowForm);
$('#modal-post').on("submit",".update-form",SaveForm)

//delete
$('#post-list').on("click",".show-form-delete",ShowForm);
$('#modal-post').on("submit",".delete-form",SaveForm)
});

