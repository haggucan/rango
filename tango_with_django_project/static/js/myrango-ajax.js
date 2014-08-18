$(document).ready(function () {

    //localStorage.clear();
    $('.drop-files').hide();

    $.ajaxSetup({ 
         beforeSend: function(xhr, settings) {
             function getCookie(name) {
                 var cookieValue = null;
                 if (document.cookie && document.cookie != '') {
                     var cookies = document.cookie.split(';');
                     for (var i = 0; i < cookies.length; i++) {
                         var cookie = jQuery.trim(cookies[i]);
                         // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
             }
             if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                 // Only send the token to relative URLs i.e. locally.
                 xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
             }
         } 
    });

    $('#likes').click(function () {
        var catid;
        catid = $(this).attr("data-catid");
        $.get('/myrango/like_category/', {category_id: catid}, function (data) {
            $('#like_count').html(data);
            $('#likes').hide();
        });
    });

    $('#suggestion').keyup(function () {
        var query;
        query = $(this).val();
        $.get('/myrango/suggest_category/', {suggestion: query}, function (data) {
            $('#cats').html(data);
        });
    });

    $('.myrango-add').click(function () {
        var cat_id, title, link
        cat_id = $(this).attr("data-catid")
        title = $(this).attr("data-title")
        link = $(this).attr("data-url")
        index = $(this).attr("id")
        var mapping = {
            "cat_id": cat_id,
            "title": title,
            "link": link

        };
        $.get("/myrango/auto_add_page/", mapping, function (data) {
            $("#" + index).hide()

        });
    });

    $('.finish_auth').hide();
    $('.code').click(function(){
       $(this).val('');

    });

    $('.auth').click(function () {
       var heyy =  $.get('/rango/dropbox/auth', function (data,status,xhr) {

            var resp=data['authorize_url'];
            $('.auth_url_result').html(resp);
            $('.auth').hide();
            $('.finish_auth').show();

        });
    });

    $('.send_code').click(function(){
        
        var code = $('.code').val();
        var html = $.post('/rango/dropbox/finish/',{'code':code},function(data){

            $('.general_authentication').hide();
            $('.dropbox_content').html(data);
            $('.dropbox_content').show();

            $( "li" ).addClass(function() {
                return "crud" ;
            });
            
        });
    });

    $('.upload').click(function(){
        $('.drop-files').show();


    });

    

});
$(document).on({
    mouseenter: function () {
        if($(this).hasClass("dir crud"))
        {
          $(this).append( "<span class=buttons> <button class=upload btn btn-mini btn btn-info>Upload</button> </span> <div class=content>"+
    "<div id=drop-files ondragover=return false> Drop Images Here </div>" ); 
        }
        else if ($(this).hasClass("file crud"))
        {
         $(this).append( "<span class=buttons> <button class=delete btn btn-mini btn-danger>Delete</button>"+ 
        "<button class=open btn btn-mini btn-info>Open</button> </span>" ); 
        }
        $
        

    },
    mouseleave: function () {
        $(this).children(".buttons").remove();
         $(this).children(".content").hide();
    }
}, ".crud"); 


