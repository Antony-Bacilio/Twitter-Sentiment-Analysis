var mymap = L.map('mapid').setView([51.512, -0.104], 1);

// Webserver using Python Flask and include Leaflet in the frontend to generate an empty World Map.
L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoiYW50b255YmFjaWxpbyIsImEiOiJjbDFzNWFqdGIwYm84M2RwbHY0d3BpaTJ3In0.U00u45zTkiQMdsF39bcxwQ'
}).addTo(mymap);

// From within the frontend we are calling the first route with HTML5 Server-Sent Events and
// creating a new marker on the map for each newly received message in the Kafka topic.
var source = new EventSource('/topic/twitterdata1');

source.addEventListener('message', function(e){
    obj = JSON.parse(e.data);
    console.log("antony")
    console.log(obj);

    lat = obj.place.bounding_box.coordinates[0][0][1];
    long = obj.place.bounding_box.coordinates[0][0][0];

    username = obj.user.name;
    tweet = obj.text;
    city = obj.place.name;
    country = obj.place.country;

    marker = L.marker([lat,long],).addTo(mymap).bindPopup('Username: <strong>' + username + '</strong><br>Tweet: <strong>' + tweet + '</strong><br><br>City: ' + city + '<br>Country: <strong>' + country + '</strong>');

}, false);
