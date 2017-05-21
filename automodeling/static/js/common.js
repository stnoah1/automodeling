$(document).ready(function () {
    $('a[data-toggle="tooltip"]').tooltip({
        animated: 'fade',
        placement: 'bottom',
        html: true
    });
    $('#btn_check').click(function () {
        var stl_data = saveSTL(scene);
        console.log(stl_data);
    });
});