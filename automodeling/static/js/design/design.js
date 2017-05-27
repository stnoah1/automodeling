var bbox = {};
var real_objects;

function removeObjects(objects) {
    objects.forEach(function (object) {
        scene.remove(object);
    });
    render();
}

function getDiagonalEdge(maxx, maxy, maxz, minx, miny, minz) {
    var power_sum = Math.pow((maxx - minx), 2) + Math.pow((maxy - miny), 2) + Math.pow((maxz - minz), 2);
    return Math.sqrt(power_sum)
}

function loadSTL(stl_data) {
    removeObjects(real_objects);
    var loader = new THREE.STLLoader();
    var material = new THREE.MeshLambertMaterial({color: 0xfeb74c});
    loader.load(stl_data, function (geometry) {
        var mesh = new THREE.Mesh(geometry, material);

        var box = new THREE.Box3();
        box.setFromObject(mesh);
        var stl_length = getDiagonalEdge(box.max.x, box.max.y, box.max.z, box.min.x, box.min.y, box.min.z);
        var scale = bbox.length / stl_length;

        mesh.position.set(bbox.center.x, bbox.center.y, bbox.center.z);
        mesh.rotation.set(0, 0, 0);
        mesh.scale.set(scale, scale, scale);
        scene.add(mesh);
        render();
    });
}

function getRealObjects(scene) {
    var results = [];
    scene.traverse(function (object) {
        if (object instanceof THREE.Mesh) {
            if (object.visible === false) return;
            var geometry = object.geometry;
            if (geometry instanceof THREE.BufferGeometry) {
                geometry = new THREE.Geometry().fromBufferGeometry(geometry);
            }
            if ((geometry instanceof THREE.BoxGeometry) && (object.material instanceof THREE.MeshLambertMaterial)) {
                results.push(object)
            }
        }
    });
    return results;
}

function getBoundingBoxFromObjects(objects) {
    var box = new THREE.Box3();
    box.setFromObject(objects[0]);
    var minX = box.min.x,
        minY = box.min.y,
        minZ = box.min.z,
        maxX = box.max.x,
        maxY = box.max.y,
        maxZ = box.max.z;

    objects.forEach(function (object) {
        var box = new THREE.Box3();
        box.setFromObject(object);
        minX = Math.min(minX, box.min.x);
        minY = Math.min(minY, box.min.y);
        minZ = Math.min(minZ, box.min.z);
        maxX = Math.max(maxX, box.max.x);
        maxY = Math.max(maxY, box.max.y);
        maxZ = Math.max(maxZ, box.max.z);
    });
    var result = [minX, minY, minZ, maxX, maxY, maxZ];
    return result;
}

function getLocation(scene) {
    real_objects = getRealObjects(scene);
    var bb_info = getBoundingBoxFromObjects(real_objects);
    bbox["center"] = {
        "x": (bb_info[0] + bb_info[3]) / 2,
        "y": (bb_info[1] + bb_info[4]) / 2,
        "z": (bb_info[2] + bb_info[5]) / 2,
    };
    bbox["length"] = getDiagonalEdge(bb_info[0], bb_info[1], bb_info[2], bb_info[3], bb_info[4], bb_info[5])
}

$(document).ready(function () {
    $('a[data-toggle="tooltip"]').tooltip({
        animated: 'fade',
        placement: 'bottom',
        html: true
    });

    $('#btn_check').click(function () {
        var stl_info = saveSTL(scene);
        getLocation(scene);
        $("#list_candidates").html("");
        $.post("convert/", {data: stl_info}, function (data) {
            data['related_models'].forEach(function (model) {
                $("#list_candidates").append('<li><a style="padding: 0px" ' +
                    'onclick="loadSTL(\'/static/data/stl/' + model + '.stl\')">' +
                    '<img class="navbar-brand" style="padding: 5px;" src="/static/data/thumbnails/' + model + '.jpg">' +
                    '</a></li>').trigger("created");
            });
        });
        // FOR TEST
        // var blob = new Blob([stl_info], {type: 'text/plain'});
        // saveAs(blob, 'test.stl');
    });
});
