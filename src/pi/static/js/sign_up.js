$(function() {
    $.FormValidator.init('signup-form');
    
    $('#ok-button').bind('click', function() {
        $('#info-dialog').popup('close');
    });

    $('#sign-up-button').click(function() {
        if (false == $.FormValidator.validate('signup-form')) {
            return;
        }

        var email = $('#email').val().trim();
        var password = $('#password').val().trim();
        var repassword = $('#repassword').val().trim();
        if (password != repassword) {
            $('#password-info').hide();
            $('#repassword-info').html('you input different passwords');
            $('#repassword-info').show();
            return;
        }

        var ajaxData = 'email=' + email + 
            '&password=' + password +
            '&name=' + name;
        
        $.ajax({
            dataType: "json",
            type: 'POST',
            url: 'signup',
            data: ajaxData,
            success: function (data) {
                if (data.success) {
                    $('#info-dialog').popup({
                     afterclose: function (event, ui) {
                            $.mobile.changePage(data.url);
                        }
                    });
                    $('#info-title').html('Successful');
                    $('#into').html('Active code has been sent to your email box. Please use the link to active your account.');
                    $('#info-dialog').popup('open');
                } else {
                    $('#info-dialog').popup({
                        afterclose: function (event, ui) {
                            //
                        }
                    });
                    $('#info-title').html('!');
                    $('#info').html(data.errmsg);
                    $('#info-dialog').popup('open');
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                $('#info-dialog').popup({
                     afterclose: function (event, ui) {
                            //
                        }
                    });
                    $('#info-title').html(errorThrown);
                    $('#info').html('Please try again later.');
                    $('#info-dialog').popup('open');
            }
        });
    });
});