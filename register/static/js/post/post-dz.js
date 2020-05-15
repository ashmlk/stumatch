Dropzone.autoDiscover = false;
$(document).ready (function () {
    var myDropzone = new Dropzone("#my-dropzone" , {
        dictDefaultMessage: '',
        addRemoveLinks: true,
        acceptedFiles: ".jpeg,.jpg,.png,.gif",
        uploadMultiple: true,
        url: "/home/post/create/",
        autoProcessQueue: false,
        paramName: "images",
        maxFiles: 4,
        thumbnailWidth: 230,
        dictRemoveFile : 'Remove',
        thumbnailHeight: 250,
        previewTemplate: document.getElementById('preview-template').innerHTML,
        previewsContainer: "#preview-selected",
        init: function () {
            var myDropzone = this;
            $('#sub-etal').on("click", function (e) {
                if (myDropzone.getQueuedFiles().length > 0) { 	
                    e.preventDefault();
                    e.stopImmediatePropagation();
                    myDropzone.processQueue();
                } else {                       
                    myDropzone.uploadFiles([]); //send empty 
                }                                    
            });
            this.on('sendingmultiple', function(file, xhr, formData) {
        // Append all form inputs to the formData Dropzone will POST
            var data = $('.post-create-form').serializeArray();
            $.each(data, function(key, el) {
                formData.append(el.name, el.value);
                });
            });
            this.on("successmultiple", function (files, data) {
                $('#modal-post').modal('hide');
                $('#_np2u').prepend(data.post);
            });
            this.on("error", function (files, data) {
            });
            myDropzone.on("complete", function(file) {
            myDropzone.removeFile(file);
            });

        }
    });
    $('#add-images').on("click", function () {
        $('#my-dropzone').get(0).dropzone.hiddenFileInput.click();
    })
})