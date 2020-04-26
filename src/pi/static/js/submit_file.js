$(function() {
    $.FormValidator.init('submit-form');

    $('#submit-file-button').click(function() {
        $('#error-info').hide();

        var r = $.FormValidator.validate('submit-form');
        if (false == r) {
            return false;
        }
    });
});