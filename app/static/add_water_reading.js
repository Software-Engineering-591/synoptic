const markers = [];

var map = L.map('map').setView([12.5776539, 106.9323423], 13)
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);


for (i=0; i < data.length; i++) {
    var marker = data[i];
    lat = marker.lat;
    lon = marker.lon;
    let this_marker = L.marker([lat, lon]).addTo(map);
    this_marker.bindPopup(`Water sensor: ${marker.name}`);
    markers.push(this_marker);
   
}


markers.forEach(element => {
    element.on('click', (e) =>
{
    lat = document.getElementById('lat')
    lon = document.getElementById('lon')
    fetch(`?lat=${element.getLatLng().lat}&longitude=${element.getLatLng().lng}`)
    lat.value = element.getLatLng().lat
    lon.value = element.getLatLng().lng
    lon.innerHTML = element.getLatLng().lon
    
})
})
    
