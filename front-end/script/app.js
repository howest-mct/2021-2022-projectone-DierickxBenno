const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

const listenToUI = function () {
};

const listenToSocket = function () {
  socket.on("B2F_temperatuur", function (jsonObject) {
    document.querySelector("c-temperatuur").innerhtml = jsonObject.temperatuur;
    });
};

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  listenToUI();
  listenToSocket();
});
