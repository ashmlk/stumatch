$(document).ready( function (e) {
    var sbtn=null;
    $(document).on("click",".scrmvbtn", function (e) {
        sbtn = $(this);
        e.stopImmediatePropagation();
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType:'json',
            beforeSend: function(){
                $('#modal-course-remove').modal('show');
            },
            success: function(data){
                $('#modal-course-remove .modal-content').html(data.html_form);
            }
        });
    });

    $('#modal-course-remove').on("submit",".saved-course-remove-form",function (e){
        e.preventDefault();
        e.stopImmediatePropagation();
        var form = $(this).serialize();
        $.ajax({
            url: $(this).attr('data-url'),
            type: "POST",
            data: form,
            dataType: 'json',
            success: function(data){
                $(sbtn).closest('.card').remove();
                $('#modal-course-remove').modal('hide');
            }
        })
    });
})


