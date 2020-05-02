$(document).ready(function (e) {
    $('.comment-like-form').on("click", ".comment-like-btn", function (e) {
        e.stopImmediatePropagation();
        e.preventDefault();
        var like_count = parseInt($(".comment-like-count", this).text());
        if($(this).find("span").hasClass("text-danger")){
            like_count--;
            $(".comment-input-like-count", this).val(like_count);
            $("span", this).removeClass("text-danger")
            $(".comment-like-count", this).text(like_count);
        } else {
            like_count++;
            $(".comment-input-like-count", this).val(like_count);
            $("span", this).addClass("text-danger")
            $(".comment-like-count", this).text(like_count); 
        }

        $.ajax({
            type:"POST",
            dataType: 'json',
            url: $(this).closest("form").attr("data-url"),     
            data: $(this).closest("form").serialize(),
            success: function (data) {
                if($(this).find("span").hasClass("text-danger")){
                    like_count--;
                    $(".comment-input-like-count", this).val(like_count);
                    $("span", this).removeClass("text-danger")
                    $(".comment-like-count", this).text(like_count);
                } else {
                    like_count++;
                    $(".comment-input-like-count", this).val(like_count);
                    $("span", this).addClass("text-danger")
                    $(".comment-like-count", this).text(like_count); 
                }

            },
            error: function(rs, e){
                console.log(rs.responeText);
            },
        });
    });
})