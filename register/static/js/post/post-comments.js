$(document).ready(function () {
    $('.reply-btn').on("click", function () {
        $("#modal-comment-reply textarea").attr("placeholder","Add your reply")
		    $("#modal-comment-reply textarea").addClass("comment-reply-adjust")
			  var c_id = $(this).data('id');
			  $("#c-get-id").val(c_id);
			  $('textarea').val('');
			  $("#modal-comment-reply").modal("show");
			  });
		$('.view-replies').on('click', function () {
			  var h = $(this).data('hidden');
			  var curr = $(this).text()
			  var newt = $(this).attr('text')
			  $(this).text(newt)
			  $(this).attr("text",curr)
			  var id = $(this).data('id');
			  if(h == 1){
				$("#c-"+id).show();
				$(this).data('hidden',0);
				} else {
				$("#c-"+id).hide();
				$(this).data('hidden',1);
				}
			});
  });