$(function() {
    $.FormValidator.init('submit-form');

    $('#submit-file-button').click(function() {
        $('#error-info').hide();
console.log('!!!');
        var r = $.FormValidator.validate('submit-form');
        console.log(r);
        if (false == r) {
            return false;
        }
    });
});