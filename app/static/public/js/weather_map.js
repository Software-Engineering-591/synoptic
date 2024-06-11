var map = L.map(
    "map",
    { 
        zoomControl: false,
        // remove movement controls
        dragging: false,
        center: [12.587362, 106.9245478],
        zoom: 9
    }
);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {}).addTo(
  map
);
L.marker([12.587362, 106.9245478]).addTo(map);
// add a circle radius to the marker
L.circle([12.587362, 106.9245478], 10000).addTo(map);

