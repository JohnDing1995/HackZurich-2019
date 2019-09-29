var map;
$("#submitBtn").click(function(){
        $("#planForm").submit(); // Submit the form
    });
      function initMap() {
        map = new google.maps.Map(document.getElementById('map'), {
          zoom: 8
        });
             // infoWindow = new google.maps.InfoWindow;
          // Try HTML5 geolocation.
      }
      // function geocodeReverse (pos) {
      //   var geocoder = new google.maps.Geocoder;
      //   var latlng = {lat: parseFloat(pos.coords.latitude), lng: parseFloat(pos.coords.longitude)};
      //   geocoder.geocode({'location': latlng}, function(results, status) {
      //     if (status === 'OK') {
      //       if (results[0]) {
      //         document.getElementById("search-query-city").value = results[0];
      //         debugger;
      //         console.log(results);
      //       } else {
      //         window.alert('No results found');
      //       }
      //     } else {
      //       window.alert('Geocoder failed due to: ' + status);
      //     }
      //   });
      // }

function sendOptions() {

}
      function handleLocationError(browserHasGeolocation, infoWindow, pos) {
        infoWindow.setPosition(pos);
        infoWindow.setContent(browserHasGeolocation ?
                              'Error: The Geolocation service failed.' :
                              'Error: Your browser doesn\'t support geolocation.');
        infoWindow.open(map);

      }



