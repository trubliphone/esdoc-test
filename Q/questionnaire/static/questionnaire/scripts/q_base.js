/* q_base.js */

/* the Q mostly uses Angular for the client */
/* preferably angular-ui-bootstrap */
/* sometimes it uses Bootstrap directly for look-and-feel stuff */
/* but sometimes, when all else fails, it uses pure JQuery or JavaScript */
/* that code is defined here */

/**************************************/
/* begin jquery widget initialization */
/**************************************/

/* b/c the Q is so dynamic, new JQuery widgets may need to be initialized at run-time */
/* these fns takes care of that (although since moving to ng, there is hardly any need for them) */

function init_widgets(init_fn, elements, force_init) {
    force_init = typeof force_init !== 'undefined' ? force_init : false;
    var initialized_widget_class_name = "initialized_" + init_fn.name;
    $(elements).each(function() {
        if (! $(this).hasClass(initialized_widget_class_name) || (force_init)) {
            init_fn(this);
            $(this).addClass(initialized_widget_class_name)
        }
    });
}

/**************************************/
/* end jquery widget initialization */
/**************************************/

/**************************/
/* begin message handling */
/**************************/

function show_lil_msg(content) {
    var lil_msg = $("div#lil_msg");
    $(lil_msg).html(content);
    var ms_to_show = 2600;
    $(lil_msg)
        .fadeIn()
        .delay(ms_to_show)
        .fadeOut();
};

function show_msg(text, status) {
    status = typeof status !== 'undefined' ? status : "default";
    var box = bootbox.alert(text);
    box.find(".modal-content").addClass(status);
}

function check_msg() {
    /* gets all pending Django messages */

    var messages_url = "/services/messages/";

    $.ajax({
        url: messages_url,
        type: "GET",
        cache: false,
        success: function (data) {
            $.each(data, function (i, message) {
                show_msg(message.text, message.status);
            });
        },
        error: function (xhr, status, error) {
            console.log(xhr.responseText + status + error)
        }
    });
};

/************************/
/* end message handling */
/************************/


/*********************/
/* begin utility fns */
/********************/

function sort_objects_by_attr(objs, attr) {
    sorted_objs = objs.sort(function(a, b) {
        if (a[attr] == b[attr]) { return 0; }
        if (a[attr] > b[attr]) { return 1; }
        else { return -1; }
    });
    return sorted_objs;
}

function get_object_by_attrs(objs, attrs) {
    for(var i=0; i<objs.length; i++) {
        var match = true
        var obj = objs[i];
        for (var k in attrs) {
            if (!obj.hasOwnProperty(k) || obj[k] != attrs[k]) {
                match = false;
                break;
            }
        }
        if (match) {
            return obj;
        }
    }
    return null;
}

/*******************/
/* end utility fns */
/*******************/

/********************/
/* begin validators */
/********************/

/* note that validators are now defined in "q_ng_base.js" as part of the "$qvalidators" service */

/******************/
/* end validators */
/******************/