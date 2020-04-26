$(function() {
    $('#submit-file-button').click(function() {
        $.mobile.changePage('submit_file.html');
    });

    $('#text-file-button').click(function() {
        $.mobile.changePage('type_text.html');
    });

    var ajaxData = "";

    $('#flesh-button').click(function() {
        $.ajax({
            dataType: "json",
            type: 'POST',
            url: 'filelist',
            data: ajaxData,
            success: function (data) {

                if (data.success) {
                    $('#file_list').html(data.file_list)
                } else {
                    //
                }
            }
        });
    });

    $('#flesh-button').trigger('click');
});