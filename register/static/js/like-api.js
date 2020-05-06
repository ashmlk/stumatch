$(document).ready(function (e) {
    var likes = $(".likeBtn").find("input").attr("value");
    $(".like-count-d").text(likes);
    $('.post-like-form').on("click", ".likeBtn", function (e) {
        var btn = $(this)
        e.preventDefault();
        e.stopImmediatePropagation();
        var tk = $(this).attr("data-token");
        $.ajax({
            type: "POST",
            url: $(this).attr("data-url"),
            dataType: 'json',
            data: { 'csrfmiddlewaretoken':tk },
            success: function (data){
                $(btn).closest(".like-section").html(data.post_likes);
            },
            error: function(rs, e){
                console.log(rs.responeText);
            },
        });
    });
})
