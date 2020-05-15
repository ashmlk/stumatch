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
	
	// removing acourse form your courses
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
                    $('#modal-course-remove').modal('hide');
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

$(document).ready(function () {
		//sharing taking a course
		$(document).on("click",".sh-shr-c", function (e) {
			e.preventDefault();
			e.stopImmediatePropagation();
			var btn = $(this);
			$.ajax({
				url: btn.attr("data-url"),
				type: 'get',
				dataType:'json',
				beforeSend: function(){
					$('#modal-course-share').modal('show');
				},
				success: function(data){
					$('#modal-course-share .modal-content').html(data.html);
				}
			});
		});
	
		$('#modal-course-share').on("submit",".share-course-form",function (e){
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
					$(".share-course-form #before-success").remove();
					$(".share-course-form #success_tic").show();
					setTimeout(function() {
						$('#modal-course-share').modal('hide');
						$('body').removeClass('modal-open');
						$('.modal-backdrop').remove();  
					}, 
					2300);			
				} 
			})
		});
})


