 
var map = L.map('map').setView([12.577656, 106.935126], 13)
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

map.addEventListener('click', (e) => {
    console.log(e.latlng);
});
var a = null
map.on('click', (e) => {
    let lat = e.latlng.lat;
    let longitude = e.latlng.lng;

    a = L.marker([lat, longitude]).addTo(map);
    fetch (`selected-loc?latitude=${lat}&longitude=${longitude}`)
})