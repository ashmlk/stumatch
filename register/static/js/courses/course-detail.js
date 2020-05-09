$(document).ready(function () {
    $('.v_rebtn').on("click", function () {
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