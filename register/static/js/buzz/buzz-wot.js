$(document).ready(function (e) {
    $('.buzz-wot-form').on("click", ".buzz-wot-btn", function (e) {
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
                $(btn).closest(".buzz-wots-container").html(data.buzz);
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
