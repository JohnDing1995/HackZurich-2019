var map;

function submitForm() {
    var params = $("#planForm").serialize();
    $.get('http://127.0.0.1:5000/api/route', data = params, function (jsonData) {
        console.log(jsonData);
        var waypts = [];
        var origin = '';
        var destination = '';
        var directionsService = new google.maps.DirectionsService;
        var directionsRenderer = new google.maps.DirectionsRenderer;
        for (var i = 0; i < jsonData.length; i++) {
            if (i === 0) {
                origin = jsonData[0][0].toString() + ',' + jsonData[0][1].toString()
                console.log(origin)
            } else if (i === jsonData.length - 1) {
                destination = jsonData[i][0].toString() + ',' + jsonData[i][1].toString()
            } else {
                waypts.push({
                    location: jsonData[i][0].toString() + ',' + jsonData[i][1].toString(),
                    stopover: true
                })
            }
        }
        directionsService.route({
            origin: origin,
            destination: destination,
            waypoints: waypts,
            optimizeWaypoints: true,
            travelMode: 'DRIVING'
        }, function (response, status) {
            if (status === 'OK') {
                directionsRenderer.setDirections(response);
                var route = response.routes[0];
                var summaryPanel = document.getElementById('list');
                summaryPanel.innerHTML = '';
                // For each route, display summary information.
                for (var i = 0; i < route.legs.length; i++) {
                    var routeSegment = i + 1;
                    summaryPanel.innerHTML += '<b>Route Segment: ' + routeSegment +
                        '</b><br>';
                    summaryPanel.innerHTML += route.legs[i].start_address + ' to ';
                    summaryPanel.innerHTML += route.legs[i].end_address + '<br>';
                    summaryPanel.innerHTML += route.legs[i].distance.text + '<br><br>';
                }
            } else {
                window.alert('Directions request failed due to ' + status);
            }
        });

    });

    return false
}

function initMap() {
    console.log("defwefwfew")
    var directionsRenderer = new google.maps.DirectionsRenderer;
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 6,
        center: {lat: 47.3743182, lng: 8.503577}
    });
    directionsRenderer.setMap(map);

}

