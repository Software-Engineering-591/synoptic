geo_data.forEach((d) => {
  var map = L.map(`map_${d.id}`)
    .setView(d.point, 16);
  
  L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }
  ).addTo(map);
  
  L.marker(d.point).addTo(map);
});