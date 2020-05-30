$(document).ready(function (e) {
    $(document).on('click', '.course-goto', function (e) {
        e.stopImmediatePropagation();
        var url = $(this).attr("data-url")
        document.location.href = url 
	});
    $('.scrmv').on("click", ".scrmvbtn", function (e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        var btn = $(this);
        $.ajax({
            type: "POST",
            url: $(this).attr("data-url"),
            dataType: 'json',
            data: $(this).closest("form").serialize(),
            success: function (data){
                $('#modal-saved-courses .text-message').text(data.message);
                $('#modal-saved-courses').modal('show');
                $(btn).closest(".card").remove();
            },
            error: function(rs, e){
                console.log(rs.responeText);
            },
        });
    });
});
