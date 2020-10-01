$(document).ready(function () {
    $(document).on('click', '.course-title-box', function (e) {
        e.stopImmediatePropagation();
        var url = $(this).attr("data-url")
        document.location.href = url 
    });
})
