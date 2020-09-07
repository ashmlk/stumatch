$('.b_dlfx').ready( function () {
    $('.b_actb').on("click", function () {
        $('#modal-buzz-c').modal('show');
    })
    maxCharacters = 180;
    $('#count').text(maxCharacters);
    $('#id_reply_content').bind('keyup keydown', function() {
        var count = $('#count');
        var characters = $(this).val().length;
        if (characters >= maxCharacters) {
            count.addClass('text-danger');
        } else {
            count.removeClass('text-danger');
        }
        count.text(maxCharacters - characters);
    });
    $(document).on('submit', '.buzz-d-c', function (e) {
       e.preventDefault();
       e.stopImmediatePropagation();
       var form = $(this).serialize();
       $.ajax({
           url: $(this).attr('data-url'),
           type: 'POST',
           data: form,
           dataType: 'json',
           success: function(data){
               $('#modal-buzz-c').modal('hide');
               $('#bznwre_').prepend(data.reply);
               $('#_cct').text(data.r_count);
               $('textarea').val('');
               $('#id_reply_nickname').val('');
           },
           error: function(rs, e){
               console.log(rs.responeText);
           },
       })
    })
});

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
});
$(document).ready(function (e) {
    $('.buzz-ctr').on("click", ".buzz-like-btn", function (e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        var btn = $(this)
        var tk = $(this).attr("data-token");
        $.ajax({
            type: "POST",
            url: $(this).attr("data-url"),
            dataType: 'json',
            data: $(this).closest("form").serialize(),
            success: function (data){
                $(btn).closest(".buzz-likes-container").html(data.buzz);
            },
            error: function(rs, e){
                console.log(rs.responeText);
            },
        });
    });
});
$(document).ready(function (e) {
    $('.buzz-ctr').on("click", ".buzz-wot-btn", function (e) {
        var btn = $(this)
        e.preventDefault();
        e.stopImmediatePropagation();
        var tk = $(this).attr("data-token");
        $.ajax({
            type: "POST",
            url: $(this).attr("data-url"),
            dataType: 'json',
            data: $(this).closest("form").serialize(),
            success: function (data){
                $(btn).closest(".buzz-wots-container").html(data.buzz);
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
    $(document).on("click", ".relikbtnbz", function (e) {
        var btn = $(this)
        e.stopImmediatePropagation();
        e.preventDefault();
        $.ajax({
            type:"POST",
            url: $(this).attr("data-url"),     
            data: $(this).closest("form").serialize(),
            dataType: 'json',
            success: function (data) {
               $(btn).closest("._3buzzcmcntr").html(data.r);
            },
            error: function(rs, e){
                console.log(rs.responeText);
            },
        });
    });
});
$(document).ready(function () {
    var btn_c_rmv = null;
	$('.buzz-comment-container').on("click",".shbzcmdlfrm", function (e) {
        btn_c_rmv = $(this);
        e.preventDefault();
		e.stopImmediatePropagation();
		$.ajax({
			url: $(this).attr("data-url"),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-comment-delete').modal('show');
			},
			success: function(data){
				$('#modal-comment-delete .modal-content').html(data.html_form);
			}
		});
	});
	$('#modal-comment-delete').on("submit",".cbzcmdlfrm",function (e){
		e.preventDefault();
        e.stopImmediatePropagation();
        var form = $(this).serialize();
		$.ajax({
			url: $(this).attr('data-url'),
			type: $(this).attr('method'),
			data: form,
			dataType: 'json',
			success: function(data){
				if(data.form_is_valid){
                    $(btn_c_rmv).closest(".bzrbx").remove();
                    var cm_count = parseInt(document.getElementById("_cct").innerText);
                    cm_count--;
                    document.getElementById("_cct").innerText = cm_count
					$('#modal-comment-delete').modal('hide');
					$('body').removeClass('modal-open');
					$('.modal-backdrop').remove();
				} 
			}
		})
	});
});
    

