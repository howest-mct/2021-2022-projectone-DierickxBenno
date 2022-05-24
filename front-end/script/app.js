const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

const listenToUI = function () {
};

const listenToSocket = function () {
  socket.on("B2F_temperatuur", function (jsonObject) {
    console.log(`nieuwe temperatuur geschreven`);
    document.querySelector(".c-temperatuur").innerHTML = `${jsonObject.temperatuur} °C`;
    });
};

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  listenToUI();
  listenToSocket();
});
