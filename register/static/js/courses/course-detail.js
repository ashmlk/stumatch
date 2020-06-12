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
$(document).ready(function () {
    /* 
    * Sorting methods for sorting reviews in All and Specific page
    * div a is reviews all and div s is for course specific to instructor
    */
        $(document).on('click', '.srbtnmenu button', function (e) {
            e.preventDefault();
            var btn = $(this);
            $('.srbtn').each(function () {
                $(this).removeClass('active');
            });
            $(btn).addClass('active');
        });

        $(document).on('click','.odyr',function (e) {  // sort based on course year
            e.preventDefault()
            $('#dvmc').find('.cntr').sort(function(a, b) { 
                var contentA = parseInt($(a).attr('data-year')); 
                var contentB = parseInt($(b).attr('data-year')); 
                return contentB - contentA;
            }).appendTo("#dvmc");
        });

        $(document).on('click','.odins',function (e) { // sort based on course insrtructor
            e.preventDefault()
            $('#dvmc').find('.cntr').sort(function(a, b) { 
                var contentA = $(a).attr('data-ins').toLowerCase(); 
                var contentB = $(b).attr('data-ins').toLowerCase();
                return String.prototype.localeCompare.call(contentA, contentB);
            }).appendTo("#dvmc");
        });

        $(document).on('click','.odiyr',function (e) {  // sort based on course year and instructor
            e.preventDefault()
            $('#dvmc').find('.cntr').sort(function(a, b) { 
                var contentA = $(a).attr('data-ins').toLowerCase(); 
                var contentB = $(b).attr('data-ins').toLowerCase();
                if (contentA === contentB){
                    var conA = parseInt($(a).attr('data-year')); 
                    var conB = parseInt($(b).attr('data-year'));
                    return conB - conA;
                }
                else {
                    return String.prototype.localeCompare.call(contentA, contentB);
                }
            }).appendTo("#dvmc");
        });

        $(document).on('click','.odnw', function (e) { // newset
            e.preventDefault();
            $('#dvmc').find('.cntr').sort(function(a, b) { 
                var contentA = parseInt($(a).attr('data-new')); 
                var contentB = parseInt($(b).attr('data-new')); 
                return contentA - contentB;
            }).appendTo("#dvmc");
        });

        $(document).on('click','.odyrs',function (e) {  // sort basedon year added - specific to instructor
            e.preventDefault()
            $('#dvmcs').find('.cntr').sort(function(a, b) { 
                var contentA = parseInt($(a).attr('data-year')); 
                var contentB = parseInt($(b).attr('data-year')); 
                return contentB - contentA;
            }).appendTo("#dvmcs");
        });

        $(document).on('click','.odnws', function (e) {  // sort newest on instructor page
            e.preventDefault();
            $('#dvmcs').find('.cntr').sort(function(a, b) { 
                var contentA = parseInt($(a).attr('data-new')); 
                var contentB = parseInt($(b).attr('data-new')); 
                return contentA - contentB;
            }).appendTo("#dvmcs");
        });

    });
    $(document).ready(function (){
        
        $(document).ajaxSend(function (event, jqxhr, settings) {
        jqxhr.setRequestHeader("X-CSRFToken", '{{ csrf_token }}');
        });
        
        var ShowCourseAutoAddForm = function(e){
            e.stopImmediatePropagation();
            var btn = $(this);
            $.ajax({
                url: btn.attr("data-url"),
                type: 'get',
                dataType:'json',
                beforeSend: function(){
                    $('#modal-course-auto-add').modal('show');
                    $('#hint_id_course_instructor').remove()
                },
                success: function(data){
                    $('#modal-course-auto-add .modal-content').html(data.html_form);
                    $('#hint_id_course_instructor').remove()
                }
            });
            return false;
        };
        
        var SaveCourseAutoAddForm =  function(e){
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
                    if(data.form_is_valid){
                        $('#modal-course-auto-add .modal-content .modal-body').empty()
                        $('#modal-course-auto-add .modal-content .modal-footer').empty()
                        $('#modal-course-auto-add .modal-content .modal-body').append('<div class="d-flex justify-content-center p-4"> <div> <h5 class="text-success font-size-smaller">'+ data.message + "</h5> </div> </div>")
                        window.setTimeout(function(){
                            $('#modal-course-auto-add').modal('hide');
                        }, 2500);
                    
                    } else {
                        $('#modal-course-auto-add .modal-content').html(data.html_form)
                    }
                }
            })
            return false;
        }
        
        $('.btncrsatadd').click(ShowCourseAutoAddForm);
        $('#modal-course-auto-add').on("submit",".course-auto-add-form",SaveCourseAutoAddForm)
        });