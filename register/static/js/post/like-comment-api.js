$(document).ready(function (e) {
    var form_c_like;
    $(document).on("submit", ".post-comment-like-form", function (e) {
        form_c_like = $(this)
        e.stopImmediatePropagation();
        e.preventDefault();
        $.ajax({
            type:"POST",
            dataType: 'json',
            url: $(this).attr("data-url"),     
            data: $(this).serialize(),
            success: function (data) {
                var k = $(form_c_like).closest('.clcntr').html(data.comment)
            },
            error: function(rs, e){
                console.log(rs.responeText);
            },
        });
    });
})