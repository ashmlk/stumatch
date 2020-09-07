Dropzone.autoDiscover = false;
$(document).ready (function () {
    var myDropzone = new Dropzone("#my-dropzone" , {
        dictDefaultMessage: '',
        addRemoveLinks: true,
        acceptedFiles: ".jpeg,.jpg,.png,.gif",
        uploadMultiple: true,
        url: "/post/create/",
        autoProcessQueue: false,
        paramName: "images",
        maxFiles: 4,
        thumbnailWidth: 230,
        dictRemoveFile : 'Remove',
        thumbnailHeight: 250,
        parallelUploads: 10,
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

            this.on('sendingmultiple', function(files, xhr, formData) {
            var data = $('.post-create-form').serializeArray();
            $.each(data, function(key, el) {
                formData.append(el.name, el.value);
                });
            });

            this.on("successmultiple", function (files, data) {
                if(data.form_is_valid){
					$('#modal-post').modal('hide');
					$('#_np2u').prepend(data.post);
				} else {
					$('#modal-post .modal-content').html(data.html_form)
				}
            });

            this.on("error", function (files, data) {
            });

            this.on("completemultiple", function(file) {
                myDropzone.removeFile(file);
            });

        }
    });
    
    $('#add-images').on("click", function () {
        $('#my-dropzone').get(0).dropzone.hiddenFileInput.click();
    })
})