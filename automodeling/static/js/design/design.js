$(document).ready(function () {
    $('a[data-toggle="tooltip"]').tooltip({
        animated: 'fade',
        placement: 'bottom',
        html: true
    });
    $('#btn_check').click(function () {
        var stl_info = saveSTL(scene);
        $.post("convert/", {data: stl_info}, function (data) {
            console.log(data);
        });
    });
});
