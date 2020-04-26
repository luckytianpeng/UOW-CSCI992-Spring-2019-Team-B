$(function() {

    function GetQueryString(name)
    {
        var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
        var r = window.location.search.substr(1).match(reg);
        if (null != r) {
            return unescape(r[2]);
        } else {
            return null;
        }
    }

    var ajaxData = "fileid=" + GetQueryString('file');

    $.ajax({
        dataType: "json",
        type: 'POST',
        url: 'fileinfo',
        data: ajaxData,
        success: function (data) {
            if (data.success) {
                $('#en-html').html(data.en_html)
                $('#zhcn-html').html(data.zhcn_html)
                $('#src-html').html(data.src_html)

                $('.number').each(function() {
                    $(this).parent().css("background-color", 'rgb(247, 238, 214)');
                });
            }
        }
    });
});