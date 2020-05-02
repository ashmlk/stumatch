$(document).ready(function (e) {
    $('.post-like-form').on("click", ".likeBtn", function (e) {
        var like_count = $(".input-like-count", this).val();
        $(".like-count-d").text(like_count);
        e.preventDefault();
        if($(this).find("i").hasClass("fa-thumbs-up")){
            like_count++;
            $(".input-like-count", this).val(like_count);
            $("i", this).removeClass("fa-thumbs-up").addClass("fa-thumbs-down")
            $(".like-count", this).text(like_count);
            $(".like-count-d").text(like_count);
        } else {
            like_count--;
            $(".input-like-count", this).val(like_count);
            $("i", this).removeClass("fa-thumbs-down").addClass("fa-thumbs-up")
            $(".like-count", this).text(like_count);
            $(".like-count-d").text(like_count);
        }
        var tk = $(this).attr("data-token");
        var pg = $(this).attr('value');
        $.ajax({
            type: "POST",
            url: $(this).attr("data-url"),
            dataType: 'json',
            data: {'guid_url': pg, 'csrfmiddlewaretoken':tk },
            success: function (data){
                var like_count = parseInt($(".like-count", this).text());
                if($(this).find("i").hasClass("fa-thumbs-up")){
                    like_count++;
                    $(".input-like-count", this).val(like_count);
                    $("i", this).removeClass("fa-thumbs-up").addClass("fa-thumbs-down")
                    $(".like-count", this).text(like_count);
                } else {
                    like_count--;
                    $(".input-like-count", this).val(like_count);
                    $("i", this).removeClass("fa-thumbs-down").addClass("fa-thumbs-up")
                    $(".like-count", this).text(like_count);
                }
                $("#post-detail-container div").html(data.post_detail)
            },
            error: function(rs, e){
                console.log(rs.responeText);
            },
        });
    });
})
