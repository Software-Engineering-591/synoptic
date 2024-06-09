const markers = [];
var map = L.map('map').setView([12.577656, 106.935126], 13)
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var a = null

for (i=0; i < data.length; i++) {
    var marker = data[i];
    lat = marker.lat;
    lon = marker.lon;
    let markerz = L.marker([lat, lon]).addTo(map);
    markerz.bindPopup("hello");
    markers.push(markerz);
   
}


markers.forEach(element => {
    element.on('click', (e) =>
{
    as = document.getElementById('lol')
    as.innerHTML = element.getLatLng().lat;
    fetch(`?lat=${element.getLatLng().lat}&longitude=${element.getLatLng().lng}`)
    document.getElementById('lat').value = element.getLatLng().lat
    document.getElementById('lon').value = element.getLatLng().lng

    document.getElementById('map_modal').close();
    
})
})
    
