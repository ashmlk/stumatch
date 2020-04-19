$(document).ready(function (e) {
    $('.post-like-form').on("click", ".likeBtn", function (e) {
        var like_count = parseInt($(".like-count", this).text());
        e.preventDefault();
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
        //var tk = $(this).attr("data-token")
        $.ajax({
            type: "POST",
            dataType: 'json',
            url: $(this).attr("data-url"),
            //data: {'csrfmiddlewaretoken': tk}, 
            //added below
            headers: {'X-CSRFToken': '{{ csrf_token }}'},       
            data: $(this).closest("form").serialize(),
            //end
            success: function (data){
                var like_count = parseInt($(".like-count", this).text());
                e.preventDefault();
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
                //$("#post-list div").html(data.posts)
                $("#post-detail-container div").html(data.post_detail)
            },
            error: function(rs, e){
                console.log(rs.responeText);
            },
        });
    });
})
