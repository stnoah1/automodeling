function loadSTL(stl_data) {
    var loader = new THREE.STLLoader();
    var material = new THREE.MeshLambertMaterial({color: 0xfeb74c});
    loader.load(stl_data, function (geometry) {
        var mesh = new THREE.Mesh(geometry, material);
        mesh.position.set(75, 25, 25);
        mesh.rotation.set(-Math.PI / 2, 0, 0);
        mesh.scale.set(1000, 1000, 1000);
        scene.add(mesh);
        render();
    });
}

$(document).ready(function () {
    $('a[data-toggle="tooltip"]').tooltip({
        animated: 'fade',
        placement: 'bottom',
        html: true
    });

    $('#btn_check').click(function () {
        var stl_info = saveSTL(scene);
        $("#list_candidates").html("");
        $.post("convert/", {data: stl_info}, function (data) {
            data['related_models'].forEach(function (model) {
                $("#list_candidates").append('<li><a style="padding: 0px" ' +
                    'onclick="loadSTL(\'/static/data/stl/'+model+'.stl\')">' +
                    '<img class="navbar-brand" style="padding: 5px;" src="/static/data/thumbnails/' + model + '.jpg">' +
                    '</a></li>').trigger("created");
            });
        });
        // FOR TEST
        // var blob = new Blob([stl_info], {type: 'text/plain'});
        // saveAs(blob, 'test.stl');
    });
});
