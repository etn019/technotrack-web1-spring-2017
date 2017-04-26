$(document).ready(
    function() {
        window.setInterval(
            function () {
                element = $('.commentsdiv');
                $(element).load(element.attr('data-url'));
            },
            3000
        )
    }
);