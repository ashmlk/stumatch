$(document).ready(function (e) {
    $(document).on("click", "#likeBtn", function (e) {
        e.preventDefault();
        var tk = $(this).attr("data-token")
        $.ajax({
            type: "POST",
            dataType: 'json',
            url: $(this).attr("data-url"),
            data: {'csrfmiddlewaretoken': tk},        
            success: function (data){
                $("#post-list div").html(data.posts)
            },
            error: function(rs, e){
                console.log(rs.responeText);
            },
        });
    });
})
