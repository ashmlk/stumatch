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
            $("#review-all-tab").find("span").text(data.reviews_all_count)
            $("#review-spec-tab").find("span").text(data.reviews_count)
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