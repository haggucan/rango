$(document).ready(function () {

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

    $('.auth').click(function () {
        $.get('/rango/dropbox/auth', function (data) {
            $('.auth_url_result').html(data);
            $('.auth').hide();

        });


    });

});


