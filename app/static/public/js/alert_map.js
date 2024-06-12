var map = L.map("map", {
  zoomControl: false,
  // remove movement controls
  dragging: false,
  center: [12.587362, 106.9245478],
  zoom: 14,
});
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {}).addTo(
  map
);

// loop over 3 colors and add them to the map
let markers = {
  error: "red",
  warning: "orange",
  success: "green",
};

markers = Object.fromEntries(
  Object.entries(markers).map(([_, color]) => [
    _,
    L.icon({
      iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-${color}.png`,
      shadowUrl:
        "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41],
    }),
  ])
);
sensors.forEach((sensor) => {
  m = L.marker(sensor.sensor.point, { icon: markers[sensor.level] })
    .addTo(map)
    .on("click", function (e) {
      htmx.ajax("GET", "/alert/graph/", {
        values: {
          sensor_id: sensor.sensor.id,
        },
        target: "#graph",
        swap: "outerHTML",
      });
    });
});
// L.marker([12.587362, 106.9245478]).addTo(map);
// // add a circle radius to the marker
// L.circle([12.587362, 106.9245478], 10000).addTo(map);
