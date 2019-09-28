      var map;
      function initMap() {
        map = new google.maps.Map(document.getElementById('map'), {
          zoom: 8
        });
             infoWindow = new google.maps.InfoWindow;
          // Try HTML5 geolocation.
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(function(position) {
            var pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };

            infoWindow.setPosition(pos);
            infoWindow.setContent('Location found.');
            infoWindow.open(map);
            map.setCenter(pos);
            // geocodeReverse(position)
          }, function() {
            handleLocationError(true, infoWindow, map.getCenter());
          });
        } else {
          // Browser doesn't support Geolocation
          handleLocationError(false, infoWindow, map.getCenter());
        }
      }
      function geocodeReverse (pos) {
        var geocoder = new google.maps.Geocoder;
        var latlng = {lat: parseFloat(pos.coords.latitude), lng: parseFloat(pos.coords.longitude)};
        geocoder.geocode({'location': latlng}, function(results, status) {
          if (status === 'OK') {
            if (results[0]) {
              document.getElementById("search-query-city").value = results[0];
              debugger;
              console.log(results);
            } else {
              window.alert('No results found');
            }
          } else {
            window.alert('Geocoder failed due to: ' + status);
          }
        });
      }

      function handleLocationError(browserHasGeolocation, infoWindow, pos) {
        infoWindow.setPosition(pos);
        infoWindow.setContent(browserHasGeolocation ?
                              'Error: The Geolocation service failed.' :
                              'Error: Your browser doesn\'t support geolocation.');
        infoWindow.open(map);

      }

      function pusjh () {
          
      }
