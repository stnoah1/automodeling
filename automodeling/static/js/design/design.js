$(document).ready(function () {
    function loadSTL(stl_data) {
        var loader = new THREE.STLLoader();
        var material = new THREE.MeshLambertMaterial({color: 0xfeb74c});
        loader.load(stl_data, function (geometry) {
            var mesh = new THREE.Mesh(geometry, material);
            mesh.position.set(75, 25, 25);
            mesh.rotation.set(-Math.PI / 2, 0, 0);
            mesh.scale.set(1000, 1000, 1000);
            scene.add(mesh);
        });
    }

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

        // FOR TEST
        // var blob = new Blob([stl_info], {type: 'text/plain'});
        // saveAs(blob, 'test.stl');
    });
    $('#btn_load_stl').click(function () {
        loadSTL("/static/data/sample/stl/binary/pr2_head_pan.stl");
    });
});
