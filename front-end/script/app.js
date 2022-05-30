"use strict";

const lanIP = `${window.location.hostname}:5000`;
const socketio = io(`http://${lanIP}`);
const provider = "https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png";
// const copyright= '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles style by <a href="https://www.hotosm.org/" target="_blank">Humanitarian OpenStreetMap Team</a> hosted by <a href="https://openstreetmap.fr/" target="_blank">OpenStreetMap France</a>';

  let map, layergroup;

const init_map = function () {
  console.log("init map initiated!");
  map = L.map("mapid", {
    attributionControl: false,
    zoomControl: false,
    maxZoom: 17,
    minZoom: 16,
  }).setView([51.041028, 3.398512], 10);

  map.dragging.enable();

  L.tileLayer(provider).addTo(map);
  // L.tileLayer(provider, { attribution: copyright }).addTo(map);
};

const listenToUI = function () {};

const listenToSocket = function () {
  socketio.on("B2F_temperatuur", function (jsonObject) {
    document.querySelector(
      ".c-temperatuur"
    ).innerHTML = `${jsonObject.temperatuur} °C`;
  });

  socketio.on("B2F_GPS",function (jsonObject) {
    const data = jsonObject.GPS
    if (data != null){
    const dataId = data["data-id"]
    if (dataId == "$GPRMC"){
      const lat = data.latitude/100
      const longi = data.longitude/100 
      map.panTo(new L.LatLng(lat, longi));
    }
    else if(dataId == "$GPGGA"){
      const lat = data.latitude/100
      const longi = data.longitude/100 
      map.panTo(new L.LatLng(lat, longi));
    }
    
  }})

  socketio.on("B2F_stap",function (jsonObject) {
    console.log("stap genomen ", jsonObject)
  })

  socketio.on("B2F_meest_recente_data",function (jsonObject) {
    console.log(jsonObject)
    const waardes = document.querySelectorAll(".c-waarde_holder");
    // set sensor data
    for (const waarde of waardes){
      let waardeId = waarde.getAttribute("sensor-id");
      for (const el of jsonObject.data){
        let eenheid = waarde.getAttribute("eenheid")
        if ((waardeId != null) && (waardeId == el.sensorid)){
          waarde.innerHTML = el.waarde+" "+eenheid
        }
        //set speed & stappen
        if (eenheid != null){
          if (eenheid == "km/h"){
            const snelheid = jsonObject.snelheid[0].snelheid;
            console.log(snelheid)
            waarde.innerHTML = snelheid+" "+eenheid
          }
          else if (eenheid == ""){
            const stappen = jsonObject.stappen[0].stappen;
            waarde.innerHTML = stappen
          }
        }
      }
    }
    // set location
    const lat = jsonObject.locatie[0].latitude;
    const longi = jsonObject.locatie[0].longitude;
    map.panTo(new L.LatLng(lat, longi));
  })
};

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  listenToUI();
  listenToSocket();
  init_map();
});
