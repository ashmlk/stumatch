$(document).ready(function (e) {
    $('.scrmv').on("click", ".scrmvbtn", function (e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        $.ajax({
            type: "POST",
            url: $(this).attr("data-url"),
            dataType: 'json',
            data: $(this).closest("form").serialize(),
            success: function (data){
                $('#modal-saved-courses .text-message').text(data.message);
                $('#modal-saved-courses').modal('show');
                $(this).closest(".card").remove();
            },
            error: function(rs, e){
                console.log(rs.responeText);
            },
        });
    });
});
