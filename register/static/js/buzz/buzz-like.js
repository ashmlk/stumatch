$(document).ready(function (e) {
    $('.buzz-like-form').on("click", ".buzz-like-btn", function (e) {
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
                $(btn).closest(".buzz-likes-container").html(data.buzz);
            },
            error: function(rs, e){
                console.log(rs.responeText);
            },
        });
    });
})
