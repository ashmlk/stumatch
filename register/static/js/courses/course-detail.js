$(document).ready(function () {
    $(document).on("click",'.v_rebtn', function () {
        if ($(this).data("text") == "Show"){
            $('.review-textbox').show();
            $(this).data('text',"Hide");
        }
        else if ($(this).data("text") == "Hide"){
            $('.review-textbox').hide();
            $(this).data('text',"Show");
        }
    })
});