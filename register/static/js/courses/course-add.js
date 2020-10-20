$(document).ready(function () {

    var selectedUni = $( "#id_course_university option:selected" ).text();

    $(document).on('change','#id_course_university',function(){
        selectedUni = $( "#id_course_university option:selected" ).text();
    })
    

    $(document).on('keyup','#id_course_code', function () {
        // set the obj_text to val
        var obj_text = $(this).val();
        // check to see if course instructor has been provided by user
        if ($('#id_course_instructor').val().length > 0) {
            // course instructor field has been set
            var get_url = "/courses/add/get_obj?u=" + selectedUni + "&q=" + obj_text + "&o=" + $('#id_course_instructor').val() + "&ot=code"
        } else {
            // value of course instructor is unknown so we are now just searching for similar course code
            var get_url = "/courses/add/get_obj?u=" + selectedUni + "&q=" + obj_text + "&oj=code"
        }
        if(obj_text != ''){
            $.ajax({
                type: "GET",
                url: get_url,
                dataType: 'json',
                success: function (data) {
                    if (data.code.length > 0){
                        $('#crs-cc-dp').find('li').remove();
                        for (i in data.code){
                            var element = "<li class='list-group-item itm-slct itm-slct-cd' data-textvalue = " + data.code[i] + ">" + data.code[i] + "</li>"
                            $('#crs-cc-dp').find('ul').append(element)
                        }
                        $('#crs-cc-dp').show();
                    } else if (data.code.length <= 0) {
                        $('#crs-cc-dp').find('li').remove();
                    }
                },
                error: function (rs, e) {
                    console.log(rs.responeText);
                },
            })
        } else {
            $('#crs-cc-dp').find('ul').empty();
            $('#crs-cc-dp').hide();
        }
    });

    $(document).on('keyup','#id_course_instructor', function () {
        // set the obj_text to val
        var obj_text = $(this).val();
        /* 
        * first check what values are types by the user
        */
        if ($('#id_course_code').val().length > 0 ) {
            // course code field has been set
            var get_url = "/courses/add/get_obj?u=" + selectedUni + "&q=" + obj_text + "&o=" + $('#id_course_code').val() + "&ot=instructor";
        } else {
            // value of course instructor is unknown so we are now just searching for similar course code
            var get_url = "/courses/add/get_obj?u=" + selectedUni + "&q=" + obj_text + "&oj=instructor";
        }
        if(obj_text != ''){
            $.ajax({
                type: "GET",
                url: get_url,
                dataType: 'json',
                success: function (data) {
                    if (data.ins.length > 0 ) {
                        $('#crs-ins-dp').find('li').remove();
                        for (i in data.ins){
                            var element = "<li class='list-group-item itm-slct itm-slct-ins' data-inslastname = " 
                            + data.ins[i]["course_instructor"] + " data-insfirstname = " + data.ins[i]["course_instructor_fn"]
                            + ">" + data.ins[i]["course_instructor_fn"] + " " + data.ins[i]["course_instructor"] 
                            + "<span class='float-right text-muted small ml-2 mt-1'>" + data.ins[i]["course_university"] + " </span>" + "</li>"
                            $('#crs-ins-dp').find('ul').append(element);
                        }
                    $('#crs-ins-dp').show();
                    } else if( data.ins.length <= 0){
                        $('#crs-ins-dp').find('li').remove();
                    }
                },
                error: function (rs, e) {
                    console.log(rs.responeText);
                },
            })
        } else {
            $('#crs-ins-dp').find('ul').empty();
            $('#crs-ins-dp').hide();
        }
    });

    $(document).on('keyup','#id_course_instructor_fn', function () {
        // set the obj_text to val
        var obj_text = $(this).val();
        /* 
        * first check what values are types by the user
        */
        if ($('#id_course_code').val().length > 0 ) {
            // course code field has been set
            var get_url = "/courses/add/get_obj?u=" + selectedUni + "&q=" + obj_text + "&o=" + $('#id_course_code').val() + "&ot=instructor" + "&is_fn=True";
        } else {
            // value of course instructor is unknown so we are now just searching for similar course code
            var get_url = "/courses/add/get_obj?u=" + selectedUni + "&q=" + obj_text + "&oj=instructor" + "&is_fn=True";
        }
        if(obj_text != ''){
            $.ajax({
                type: "GET",
                url: get_url,
                dataType: 'json',
                success: function (data) {
                    if (data.ins.length > 0 ) {
                        $('#crs-ins-fn-dp').find('li').remove();
                        for (i in data.ins){
                            var element = "<li class='list-group-item itm-slct itm-slct-ins' data-inslastname = "
                            + data.ins[i]["course_instructor"] + " data-insfirstname = " 
                            + data.ins[i]["course_instructor_fn"]  + ">" + data.ins[i]["course_instructor_fn"] + " " + data.ins[i]["course_instructor"] 
                            + "<span class='float-right text-muted small ml-2 mt-1'>" + data.ins[i]["course_university"] + " </span>" + "</li>"
                            $('#crs-ins-fn-dp').find('ul').append(element);
                        }
                    $('#crs-ins-fn-dp').show();
                    } else if( data.ins.length <= 0){
                        $('#crs-ins-fn-dp').find('li').remove();
                    }
                },
                error: function (rs, e) {
                    console.log(rs.responeText);
                },
            })
        } else {
            $('#crs-ins-fn-dp').find('ul').empty();
            $('#crs-ins-fn-dp').hide();
        }
    });

    $(document).on('click', '.itm-slct-ins', function (e) {
        e.stopPropagation();
        var first_name = $(this).attr('data-insfirstname');
        var last_name = $(this).attr('data-inslastname');
        $('#id_course_instructor').val(last_name);
        $('#id_course_instructor_fn').val(first_name);
        $('.query-result').hide();
    })

    $(document).on('click', '.itm-slct-cd', function (e) {
        e.stopPropagation();
        var val = $(this).attr('data-textvalue');
        $('#id_course_code').val(val);
        $('.query-result').hide();
    })

    $(document).on('click', function (e){
        e.stopPropagation();
        $('.query-result').hide();
    })
})