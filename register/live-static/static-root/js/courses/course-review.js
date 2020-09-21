$(document).ready(function(){
	$(document).on('submit','.course-review-form', function (e) {
		e.preventDefault();
		e.stopImmediatePropagation();
		var form = $(this).serialize();
		$.ajax({
		  url: $(this).attr('data-url'),
		  type: 'POST',
		  data: form,
		  dataType: 'json',
		  success: function(data) {
            $("#new-review-s").prepend(data.review); 
			$("#new-review-a").prepend(data.review);
			$(".no-review-box").remove();
            $("#crsrwalcts").html(data.reviews_all_count)
            $("#crsspecrw").html(data.reviews_count)
            $('textarea').val('');
		  },
		  error: function(rs, e){
					console.log(rs.responeText);
				},
		});
	  });
	if ( window.history.replaceState ) {
        window.history.replaceState( null, null, window.location.href );
    }
});

$(document).ready(function (e) {
    var veid = null;
	$('.c-review-list').on("click",".show-form-delete", function (e) {
		e.stopImmediatePropagation();
        var btn = $(this);
        veid = $(this).data("veid");
		$.ajax({
			url: btn.attr("data-url"),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-review-delete').modal('show');
			},
			success: function(data){
				$('#modal-review-delete .modal-content').html(data.html_form);
			}
		});
	});
	$('#modal-review-delete').on("submit",".delete-form",function (e){
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
					$('#modal-review-delete').modal('hide');
					$('body').removeClass('modal-open');
					$('.modal-backdrop').remove();  
                    $('#_rc_'+veid).remove();
					$("#crsrwalcts").html(data.reviews_all_count)
					$("#crsspecrw").html(data.reviews_count)
                }
                else{
                    $('#modal-review-delete .modal-content').html(data.html_form);
                } 
			}
		})
	});
});


$(document).ready(function () {
	var newest = $('#dvmc').clone(true);

	$(document).on('click', '.srbtnmenu button', function (e) {
		var btn = $(this);
		$('.srbtn').each(function () {
			$(this).removeClass('active');
		});
		$(btn).addClass('active');
	});

	$('.odyr').on('click',function (e) {  
		e.preventDefault()
		$('#dvmc').find('.cntr').sort(function(a, b) { 
			var contentA = parseInt($(a).attr('data-year')); 
			var contentB = parseInt($(b).attr('data-year')); 
			return contentB - contentA;
		}).appendTo("#dvmc");
	});

	$('.odins').on('click',function (e) {  
		e.preventDefault()
		$('#dvmc').find('.cntr').sort(function(a, b) { 
			var contentA = $(a).attr('data-ins').toLowerCase(); 
			var contentB = $(b).attr('data-ins').toLowerCase();
			return String.prototype.localeCompare.call(contentA, contentB);
		}).appendTo("#dvmc");
	});

	$('.odiyr').on('click',function (e) {  
		e.preventDefault()
		$('#dvmc').find('.cntr').sort(function(a, b) { 
			var contentA = $(a).attr('data-ins').toLowerCase(); 
			var contentB = $(b).attr('data-ins').toLowerCase();
			if (contentA === contentB){
				var conA = parseInt($(a).attr('data-year')); 
				var conB = parseInt($(b).attr('data-year'));
				return conB - conA;
			}
			else {
				return String.prototype.localeCompare.call(contentA, contentB);
			}
		}).appendTo("#dvmc");
	});

	$('.odnw').on('click',function (e) {
		e.preventDefault();
		if (!$(this).hasClass('active'))
		$('#a').html(newest)
	});
	
});