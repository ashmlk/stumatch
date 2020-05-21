$(document).ready(function (e) {
    $(document).on("click", ".relikbtnbz", function (e) {
        var btn = $(this)
        e.stopImmediatePropagation();
        e.preventDefault();
        $.ajax({
            type:"POST",
            url: $(this).attr("data-url"),     
            data: $(this).closest("form").serialize(),
            dataType: 'json',
            success: function (data) {
               $(btn).closest("._3buzzcmcntr").html(data.r);
            },
            error: function(rs, e){
                console.log(rs.responeText);
            },
        });
    });
})