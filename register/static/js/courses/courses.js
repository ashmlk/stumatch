$(document).ready(function () {
        $('.c_dis').addClass("border rounded p-1 mr-2")
        $('.c_dis').css({'font-size':'0.94rem'});
        $('.c_dis').find('span.text-dark').css({'font-weight':'600'});
        $('._ar').addClass("border rounded-circle");
        $(document).on('click', '.course-goto', function (e) {
        e.stopImmediatePropagation();
        var url = $(this).attr("data-url")
        document.location.href = url 
        });
    var veid = null;
	$(document).on("click",".sh-rmv-c", function (e) {
		e.stopImmediatePropagation();
        var btn = $(this);
        veid = $(this).data("veid");
		$.ajax({
			url: btn.attr("data-url"),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-course-remove').modal('show');
			},
			success: function(data){
				$('#modal-course-remove .modal-content').html(data.html_form);
			}
		});
	});
	$('#modal-course-remove').on("submit",".remove-form",function (e){
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
                if(data.done){
                    $('#modal-course-remove').modal('hide');s
                }
				if(data.is_valid){
                    $('#modal-course-remove').modal('hide');
					$('#_cc_'+veid).remove();
				} 
			}
		})
	});
});

$(function () {
	$('[data-toggle="tooltip"]').tooltip()
});
