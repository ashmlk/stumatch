$(document).ready(function(){
	var ShowForm = function(){
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
	};

	var SaveForm =  function(){
		var form = $(this);
		$.ajax({
			url: form.attr('data-url'),
			data: form.serialize(),
			type: form.attr('method'),
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

	$('#MybtnModal').click(function(){
		$('#Mymodal').modal('show')
  });
//update
$('#post-list').on("click",".show-form-update",ShowForm);
$('#modal-post').on("submit",".update-form",SaveForm)

//delete
$('#post-list').on("click",".show-form-delete",ShowForm);
$('#modal-post').on("submit",".delete-form",SaveForm)
});



/*
$(document).ready(function(){
    function updateText(btn, newCount, verb){
       btn.text(newCount + " " + verb)
       btn.attr("data-likes", newCount)
}

$(".like-btn").click(function(e){
  e.preventDefault()
  var this_ = $(this)
  var likeUrl = this_.attr("data-href")
  var likeCount = parseInt(this_.attr("data-likes")) | 0
  var addLike = likeCount + 1
  var removeLike = likeCount - 1
  if (likeUrl){
     $.ajax({
      url: likeUrl,
      method: "GET",
      data: {},
      success: function(data){
        console.log(data)
        var newLikes;
        if (data.liked){
            updateText(this_, addLike, "Unlike")
        } else {
            updateText(this_, removeLike, "Like")
            // remove one like
        }

      }, error: function(error){
        console.log(error)
        console.log("error")
      }
    })
  }
})
})

function popupWindow(url, title, win, w, h) {
	const y = win.top.outerHeight / 2 + win.top.screenY - ( h / 2);
	const x = win.top.outerWidth / 2 + win.top.screenX - ( w / 2);
	return win.open(url, title, 'toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, copyhistory=no, width='+w+', height='+h+', top='+y+', left='+x);
}
*/