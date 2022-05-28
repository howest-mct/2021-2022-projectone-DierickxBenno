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
    console.log("gps: ", jsonObject.GPS.latitude);
    console.log("test")
    // map.center: [jsonObject.latitude, -0.09]
  })

  socketio.on("B2F_stap",function (jsonObject) {
    console.log("stap genomen ", jsonObject)
  })

  socketio.on("B2F_meest_recente_data",function (jsonObject) {
    console.log("mrd: ", jsonObject)
    const waardes = document.querySelectorAll(".c-waarde_holder");
    for (const waarde of waardes){
      let waardeId = waarde.getAttribute("sensor-id");
      for (const el of jsonObject.data){
        if ((waardeId != null) && (waardeId == el.sensorid)){
          waarde.innerHTML = el.waarde+" "+el.eenheid
        }
      }
    }
  })
};

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  listenToUI();
  listenToSocket();
  init_map();
});
