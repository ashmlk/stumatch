$(document).ready(function () {
    $('.input-images').imageUploader({
        label: '',
        imagesInputName: 'images',
        maxFiles: 4,
    });
    $(".modal-body textarea").addClass("textarea-hide-outline");
    $(".modal-body input[type='text']").addClass("textinput-hide-outline");
    $("#upload-image").click(function(){
        $("input[type='file']").click();  
    });
    $('.uploaded-image').find("img").addClass("edited-image")
    $("input[type='file']").on("change", function () {
        $(".input-images").show();
    })
});