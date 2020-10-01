$(document).ready(function (e) {
    $(document).on("click", ".review-like-btn", function (e) {
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
                $(btn).closest(".review-likes-container").html(data.review);
            },
            error: function(rs, e){
                console.log(rs.responeText);
            },
        });
    });
})
