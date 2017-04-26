$(document).ready(
    function () {
        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", $('meta[name=csrf]').attr("content"));
                }
            }
        });

        $(".modalopen").click(function () {
            $(".modal-content").load($(this).attr('data-url'));
        });
        $(document).on('submit', '.ajaxform', function () {
            var form = $(this);
            $.post(form.attr('action'), form.serialize(), function (response) {
                if (response == 'ok') {
                    location.reload();
                }
            });

            return false;
        });
    }
);
