$(document).ready(function(){
	var ShowForm = function(e){
		e.stopImmediatePropagation();
		var btn = $(this);
		$.ajax({
			url: btn.attr("data-url"),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-post-detail').modal('show');
			},
			success: function(data){
				$('#modal-post-detail .modal-content').html(data.html_data);
			}
		});
	};

	var SaveForm =  function(e){
		e.stopImmediatePropagation();
		var form = $(this);
		$.ajax({
			url: form.attr('data-url'),
			data: form.serialize(),
			type: form.attr('method'),
			dataType: 'json',
			success: function(data){
				if(data.form_is_valid){
                    $('#post-linked-comments div').html(data.comments);
                    alert('Comment added')
				} else {
                    $('#modal-post-detail .modal-content').html(data.html_data)
				}
			}
		})
		return false;
	}
	
//adding a comment
$('.comment-post-btn').click(ShowForm);
$('.post-detail-clickable-details-view').click(ShowForm);
$('#modal-post-detail').on("submit",".post-comment-form",SaveForm)

});