$(function() {
    $.FormValidator.init('sign-in-form');

    $('#sign-in-button').click(function() {

        $('#error-info').hide();

        var r = $.FormValidator.validate('sign-in-form');
        if (false == r) {
            return false;
        }
        
        var email = $('#email').val().trim();
        var password = $('#password').val().trim();

        var ajaxData = 'email=' + email +
            '&password=' + password +
            '&remember-me=' + $('#remember-me').prop('checked');

        $.ajax({
            dataType: "json",
            type: 'POST',
            url: 'signin',
            async: false,
            data: ajaxData,
            success: function (data) {

                if (data.wantVerificationCodes) {
                    $('#verification').show();
                    $('#verification-codes').addClass('auto-validate');
                }

                if (data.success) {
                    window.location.href = data.url;
                } else {
                    $('#verification-image').trigger('click');
                    
                    if (data.errmsg == "verification code is incorrect") {
                        $('#verification-codes-info').html(data.errmsg);
                        $('#verification-codes-info').show();
                        $('#verification-codes').focus();
                    } else {
                        $('#error-info').html(data.errmsg);
                        $('#error-info').show();
                        $('#email').focus();
                    }
                }
            }
        });

        return false;
    });
});