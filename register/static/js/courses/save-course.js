$(document).ready(function (e) {
    $('.course-save-form').on("click", ".save-course", function (e) {
        var btn = $(this)
        e.preventDefault();
        e.stopImmediatePropagation();
        $.ajax({
            type: "POST",
            url: $(this).attr("data-url"),
            dataType: 'json',
            data: $(this).closest("form").serialize(),
            success: function (data){
                $('#modal-save-course .text-message').text(data.message);
                $('#modal-save-course').modal('show');
            },
            error: function(rs, e){
                console.log(rs.responeText);
            },
        });
    });
})
