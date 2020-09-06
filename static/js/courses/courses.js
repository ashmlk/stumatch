$(document).ready(function () {

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

	var sbtn=null;
    $(document).on("click",".scrmvbtn", function (e) {
        sbtn = $(this);
        e.stopImmediatePropagation();
        var btn = $(this);
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

    $('#modal-course-remove').on("submit",".saved-course-remove-form",function (e){
        e.preventDefault();
        e.stopImmediatePropagation();
        var form = $(this).serialize();
        $.ajax({
            url: $(this).attr('data-url'),
            type: "POST",
            data: form,
            dataType: 'json',
            success: function(data){
                $(sbtn).closest('.card').remove();
                $('#modal-course-remove').modal('hide');
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

$(document).ready(function () {
	var infinite = new Waypoint.Infinite({
			element: $('.infinite-container')[0],
			onBeforePageLoad: function () {
			$('.loading').show();
			},
			onAfterPageLoad: function ($items) {
			$('.loading').hide();
			}
		});
		$(document).ajaxSend(function (event, jqxhr, settings) {
			jqxhr.setRequestHeader("X-CSRFToken", '{{ csrf_token }}');
		});
		var btn_list_co;
		var ShowForm = function(e){
			e.stopImmediatePropagation();
			btn_list_co = $(this);
			$.ajax({
				url: btn_list_co.attr("data-url"),
				type: 'get',
				dataType:'json',
				beforeSend: function(){
					$('#modal-course-list').modal('show');
				},
				success: function(data){
					$('#modal-course-list .modal-content').html(data.html_form);
				}
			});
			return false;
		};
		var SaveForm =  function(e){
			e.preventDefault();
			e.stopImmediatePropagation();
			var f = $(this);
			var form = $(this).serialize();
			$.ajax({
				url: $(this).attr('data-url'),
				type: $(this).attr('method'),
				data: form,
				dataType: 'json',
				success: function(data){
					if(data.form_is_valid){
						var obj = data.list
						$('#crslistul').append(obj);
						$('#modal-course-list').modal('hide');
					} 
					else if(data.form_delete_is_valid){
						if (data.redirect){
							window.location = data.new_url
							$('#modal-course-list').modal('hide');
						}
						else if($(btn_list_co).attr('data-type') == 'list'){
							$(btn_list_co).closest('li').remove();
							$('#modal-course-list').modal('hide');
						}
					} 
					else if(data.form_edit_is_valid){
						if ($(f).hasClass('form-redirect-go')){
							window.location = data.new_url 
							$('#modal-course-list').modal('hide');
						}
						else {
							$(btn_list_co).closest('li').replaceWith(data.list);
							$('#modal-course-list').modal('hide');
						}  
					}
					else if (data.form_crsaction_is_valid){
						window.location = data.new_url 
						$('#modal-course-list').modal('hide');
					} 
					else {
						$('#modal-course-list .modal-content').html(data.html_form)
					}
				}
			})
			return false;
		}
		$(document).on('click','.create-list-btn',ShowForm);
		$('#modal-course-list').on("submit",".course-list-create-form",SaveForm)
		$(document).on('click','.delete-crslist-btn',ShowForm);
		$('#modal-course-list').on("submit",".course-list-delete-form",SaveForm)
		$(document).on('click','.edit-crslist-btn',ShowForm);
		$('#modal-course-list').on("submit",".course-list-edit-form",SaveForm)
		$(document).on('click','.list-addcrs-btn',ShowForm);
		$('#modal-course-list').on("submit",".crs-itm-course-list-create-form",SaveForm)
		$(document).on('click','.list-deletecrs-btn',ShowForm); 
		$('#modal-course-list').on("submit",".crs-itm-course-list-delete-form",SaveForm)
		$(document).on('click','.list-editcrs-btn',ShowForm); 
		$('#modal-course-list').on("submit",".crs-itm-course-list-edit-form",SaveForm);

		$(document).on("click", ".review-like-btn", function (e) {
			var btnre = $(this)
			e.preventDefault();
			e.stopImmediatePropagation();
			var tk = $(this).attr("data-token");
			$.ajax({
				type: "POST",
				url: $(this).attr("data-url"),
				dataType: 'json',
				data: $(this).closest("form").serialize(),
				success: function (data){
					$(btnre).closest(".review-likes-container").html(data.review);
				},
				error: function(rs, e){
					console.log(rs.responeText);
				},
			});
		});
	})


