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
					$('#modal-post').modal('hide');
					$('#_np2u').prepend(data.post);
				} else {
					$('#modal-post .modal-content').html(data.html_form)
				}
			}
		})
		return false;
	}
	$('.create-post-btn').click(ShowForm);
	$('#modal-post').on("submit",".post-create-form",SaveForm)

});

/* 
* Opens form for deleting a post 
*/
$(document).ready(function (e) {
    var veid = null;
	$('#post-list').on("click",".show-form-delete", function (e) {
		e.stopImmediatePropagation();
        var btn = $(this);
        veid = $(this).data("veid");
		$.ajax({
			url: btn.attr("data-url"),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-post-delete').modal('show');
			},
			success: function(data){
				$('#modal-post-delete .modal-content').html(data.html_form);
			}
		});
	});
	$('#modal-post-delete').on("submit",".delete-form",function (e){
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
					$('#modal-post-delete').modal('hide');
					$('body').removeClass('modal-open');
					$('.modal-backdrop').remove();  
					$('#_pc_'+veid).remove();
				} 
			}
		})
	});
});

/* 
* Opens form for updating a post 
*/
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

/*
* Takes user to a posts main page when clicking on content
*/
$(document).on('click', '.post-details-view', function () {
    var url = $(this).attr("data-url")
    document.location.href = url 
});

/*
* Prevents the action of parent div in post container which takes user to post detail page
*/
$(document).on('click', '.p_ico', function(event) {
  event.stopPropagation();
});

/*
* Sets the first image in carousel images as active
*/
$(document).ready(function () {
    $('.carousel').each(function() {
      var c = this;
      $(c).find(".carousel-item").removeClass('active').filter(':first').addClass("active");
    });
  });

