$(document).ready( function (e) {
    var btn;
    $(document).on("click",".scrmvbtn", function (e) {
        btn = $(this)
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
        var form = new FormData(this);
        $.ajax({
            url: $(this).attr('data-url'),
            type: $(this).attr('method'),
            data: form,
            cache: false,
            processData: false,
            contentType: false,
            dataType: 'json',
            success: function(data){
                $('#modal-course-remove').modal('hide');
                $(btn).closest('.card').remove();
            }
        })
    });
})


