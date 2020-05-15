$(document).ready(function () {
    maxCharacters = 260;
    $('#count').text(maxCharacters);
    $('textarea').bind('keyup keydown', function() {
        var count = $('#count');
        var characters = $(this).val().length;
        if (characters > maxCharacters) {
            count.addClass('text-danger');
        } else {
            count.removeClass('text-danger');
        }
        count.text(maxCharacters - characters);
    });
})