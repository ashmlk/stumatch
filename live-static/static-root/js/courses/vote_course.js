$(document).ready(function (e) {
    $(document).on("click", ".c_v", function (e) {
        var btn = $(this);
        e.preventDefault();
        e.stopImmediatePropagation();
        var tk = $(this).attr("data-token");
        $.ajax({
            type: "POST",
            url: $(this).attr("data-url"),
            dataType: 'json',
            data: { 'csrfmiddlewaretoken':tk },
            success: function (data){
                $(btn).closest(".votes-container").html(data.course_vote);
            },
            error: function(rs, e){
                console.log(rs.responeText);
            },
        });
    });
    if ( window.history.replaceState ) {
        window.history.replaceState( null, null, window.location.href );
    }
})
