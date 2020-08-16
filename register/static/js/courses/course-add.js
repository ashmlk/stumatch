$(document).ready(function () {
    $('.list-group a').removeClass("active");
    $('#course-add').addClass("active");
    var options = {
    url: "/static/jsons/world_universities_and_domains.json",
    getValue: "name",
    requestDelay: 200,
    template: {
    type: "description",
    fields: {
        description: "country"
        },
    },
    list: {
        maxNumberOfElements: 7,
        showAnimation: {
        type: "fade", //normal|slide|fade
        time: 300,
        callback: function() {}
        },
        hideAnimation: {
        type: "slide", //normal|slide|fade
        time: 300,
        callback: function() {}
        },
        match: {
            enabled: true
        }
    },
    theme: "square"
    };
    $("#id_course_university").easyAutocomplete(options);

    $('.easy-autocomplete').ready( function () {
        $('div.easy-autocomplete').removeAttr('style')
        $('div').removeClass('easy-autocomplete');
      })
      
    })