function DjNodeAjax(args, my_callback, extra_callback) {
    this.args = args;

    // set call back
    this.my_callback = my_callback;
    if(!this.my_callback){
        this.my_callback = this.render;
    }

    // set extra callback
    this.my_extra_callback = extra_callback;
    if(!this.my_extra_callback){
        this.my_extra_callback = function(myobj) {};
    }
}

/* ---------- DjNodeAjax Functions ----------*/
DjNodeAjax.prototype.start_waiting = function(myobj) {

    var start_waiting_html = "<div class='wait' style='clear:both; margin: 0; padding: 0; text-align:center;'><img src='/static/dj_node/img/ajax-progress.gif' style='width: 15px; height: 15px;'></img></div>";

    if (myobj.args['node_type'] == 'list'){
        $(myobj.args['selector'] + " .list").after(start_waiting_html);
    }
    else if (myobj.args['node_type'] == 'form'){
        $(myobj.args['selector']).html(start_waiting_html);
    }else{
        $(myobj.args['selector']).after(start_waiting_html);
    }
}

DjNodeAjax.prototype.end_waiting = function(myobj) {

    if (myobj.args['node_type'] == 'list'){
        $(myobj.args['selector'] + " .wait").remove();
    }
    else if (myobj.args['node_type'] == 'form'){
        $(myobj.args['selector'] + " .wait").remove();

    }else{
        $(myobj.args['selector']).siblings(".wait").remove();
    }
}

DjNodeAjax.prototype.render = function(myobj) {
     return function(server_data, textStatus, jqXHR) {
            myobj.end_waiting(myobj);
            if (myobj.args['node_type'] == 'list'){

                if (myobj.args['render_type'] == 'append'){
                    $(myobj.args['selector'] + " .list").append(server_data.html);

                    var page = $(myobj.args['selector'] + " .page").val();
                    var page = parseInt(page) + 1;
                    $(myobj.args['selector'] + " .page").val(page);

                    if( page > parseInt(server_data.list_info['page_count']) ){
                        $(myobj.args['selector'] + " .more").hide();
                    }else{
                        $(myobj.args['selector'] + " .more").unbind('click');
                        $(myobj.args['selector'] + " .more").show();
                        $(myobj.args['selector'] + " .more").on( "click", function(event) {
                                event.preventDefault();
                                myobj.args['page'] = $(myobj.args['selector'] + " .page").val();
                                myobj.ajax(myobj.args, myobj.my_calback);
                                return false;
                        });
                    }

                }else if (myobj.args['render_type'] == 'update'){
                    $(myobj.args['render_action']).html(server_data.html);
                }

                if ("hide-more" in myobj.args && myobj.args['hide-more'] == true){
                     $(myobj.args['selector'] + " .more").hide();
                }
            } //end if
            else  if (myobj.args['node_type'] == 'form'){
                if (server_data['flag_processed'] == 0){
                    var html = server_data['html'];
                    $(myobj.args['selector']).html(html);
                    $(myobj.args['selector'] + " form :submit").on( "click", function(event) {
                            event.preventDefault();
                            myobj.args['type'] = 'POST';
                            myobj.ajax(myobj.args, myobj.my_calback);
                            return false;
                    });
                }else if (server_data['flag_processed'] == 1){
                    if (server_data['return'] == 302){
                        if (server_data['redirect_url'] == "#"){
                            window.location = window.location;
                        }else{
                            window.location = server_data['node_redirect'];
                        }
                    }
                }
            } // end else if

            myobj.my_extra_callback(myobj);
     }; // end return func
};

DjNodeAjax.prototype.ajax = function() {
    //type
    var type = 'GET';
    if (this.args['type'] == 'POST'){
           type = 'POST';
    }

    //data
    var data = {};
    if (this.args['selector'] && this.args['node_type'] == 'form'){
        if ($(this.args['selector'] + " form").length){
            data = $(this.args['selector'] + " form").serialize();
        }
    }

    //build url
    var url = this.args['url'];
    if (this.args['page']){
        if (url.indexOf("?") > -1){
            url = url + "&page=" + this.args['page'];
        }else{
            url = url + "?page=" + this.args['page'];
        }
    }

    //ajax
    this.start_waiting(this);

    var generated_callback = this.my_callback(this);
    $.ajax({ url: url,
             type: type,
             data: data,
             dataType: "json",
             success: generated_callback});
    return false;
};