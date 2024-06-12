var map = L.map('map').setView([12.5776539, 106.9323423], 13)
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

let selected = null;

map.on('click', (e) => {
    lat = e.latlng.lat
    longitude = e.latlng.lng
    if (selected != null){
        map.removeLayer(selected);
    }
    selected = L.marker([lat, longitude]).addTo(map);


        fetch(`?lat=${lat}&longitude=${longitude}`)
        lat_detail = document.getElementById('lat')
        lon_detail = document.getElementById('lon')
        lat_detail.value = lat
        lon_detail.value = longitude
        console.log(lon_detail)
  
})