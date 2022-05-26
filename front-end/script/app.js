"use strict";

const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);
const provider = "https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png";
const copyright =
  '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles style by <a href="https://www.hotosm.org/" target="_blank">Humanitarian OpenStreetMap Team</a> hosted by <a href="https://openstreetmap.fr/" target="_blank">OpenStreetMap France</a>';
let map, layergroup;

const init_map = function () {
  console.log("init map initiated!");
  map = L.map("mapid", {
    zoomControl: false,
    maxZoom: 17,
    minZoom: 16,
  }).setView([51.041028, 3.398512], 10);

  map.dragging.enable();

  L.tileLayer(provider, { attribution: copyright }).addTo(map);
};

const listenToUI = function () {};

const listenToSocket = function () {
  socket.on("B2F_temperatuur", function (jsonObject) {
    console.log(`nieuwe temperatuur geschreven`);
    document.querySelector(
      ".c-temperatuur"
    ).innerHTML = `${jsonObject.temperatuur} °C`;
  });
};

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  listenToUI();
  listenToSocket();
  init_map();
});
