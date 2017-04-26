$(document).ready(function() {
    $(document).on('click', 'button.ajaxlike', function (e) {
        var button = $(this);
        var data = $(this).data();
        //console.log(data);
        var likesButton = $('#likes-' + data.postid);
        $.ajax(
            data.url,
            {
                method: 'POST',
                success : function (response) {
                    console.log(button);
                    var postdiv = $(button).closest('.postpanel');
                    //console.log(postdiv);
                    console.log(response);
                    if (response == 'True') {
                        $(button).addClass('btn-primary').removeClass('btn-info').html('Разонравилось!');
                        current = $('.likecount-' + data.postid);
                        current.datacount = parseInt($(current).attr('data-count')) + 1;
                        $(current).attr('data-count', current.datacount);
                        $(current).html('Оценили: ' + current.datacount);
                        console.log(parseInt($(current).attr('data-count')) + 1);
                    } else if (response == 'False') {
                        $(button).addClass('btn-info').removeClass('btn-primary').html('Мне нравится!');
                        current = $('.likecount-' + data.postid);
                        current.datacount = parseInt($(current).attr('data-count')) - 1;
                        $(current).attr('data-count', current.datacount);
                        $(current).html('Оценили: ' + current.datacount);
                        console.log(parseInt($(current).attr('data-count')) - 1);
                    }
                }
            }
        );
        return false;
    });
    $(document).on('mouseover', 'button.ajaxlike', function (e) {
        var button = $(this);
        var data = $(this).data();

        $.ajax(
            data.url,
            {
                method: 'GET',
                success : function (response) {
                    var str = '';
                    if (!$.isEmptyObject(response)) {
                        for (key in response) {
                            if (response.hasOwnProperty(key)) {
                                str += response[key] + ', ';
                            }
                        }
                        str = str.slice(0, -2);
                        str += ' оценили';
                    } else {
                        str += 'Ещё никто не оценил';
                    }
                    console.log(str);
                    $('[data-toggle="tooltip"]').attr('title', str);
                    //$('[data-toggle="tooltip"]').tooltip();
                }
            }
        )

    })
});


