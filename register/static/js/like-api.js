$(document).ready(function (e) {
    $(document).on("click", "#likeBtn", function (e) {
        e.preventDefault();
        var pk = $(this).attr("value");
        var tk = $(this).attr("data-token")
        $.ajax({
            type: "POST",
            dataType: 'json',
            url: $(this).attr("data-url"),
            data: {'id':pk, 'csrfmiddlewaretoken': tk},        
            success: function (data){
                $("#post-list div").html(data.html)
            },
            error: function(rs, e){
                console.log(rs.responeText);
            },
        });
    });
})