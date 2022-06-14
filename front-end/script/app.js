"use strict";

let lat, longi
const lanIP = `${window.location.hostname}:5000`;
const socketio = io(`http://${lanIP}`);
const provider = "https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png";
// zo kunnen we options aanpassen via socketio
var options_hr, options_spd, option_temp, options_steps;
// const copyright= '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles style by <a href="https://www.hotosm.org/" target="_blank">Humanitarian OpenStreetMap Team</a> hosted by <a href="https://openstreetmap.fr/" target="_blank">OpenStreetMap France</a>';

let map, layergroup;

const listenToPwr = function () {
  const pwrBtn = document.querySelector(".c-shutdown-button")
  pwrBtn.addEventListener("click", function () {
  socketio.emit("F2B_poweroff", {'power': 0})
  console.log("turn off")
  })
}

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

const setColor = function () {
  const slider = document.querySelector(".c-slider")
  // ook bij inladen pagina
  socketio.emit("F2B_set_color", {"hue": slider.value})
  console.log("new slider value sent")
  slider.addEventListener("change", function () {
    socketio.emit("F2B_set_color", {"hue": slider.value})
    console.log("new slider value sent")
  })
}

const listenToCenterDog = function () {
  const btnDog = document.querySelector(".c-button-dog")
  btnDog.addEventListener("click", function () {
    map.panTo(new L.LatLng(lat, longi)); 
  })
}

const displaySidenav = function (buttons) {
  document.querySelector(".o-nav").classList.toggle("displayed")
  document.querySelector(".o-nav").classList.toggle("background-displayed")
  document.querySelector(".c-title").classList.toggle("remove_boxshadow")
  for (const btn of buttons){
    btn.classList.toggle("displayed")
  }
}

const listenToSidenav = function() {
    const toggleTrigger = document.querySelector(".js-toggle-nav");
    const buttons = document.querySelectorAll(".c-button");
    console.log(buttons)
    toggleTrigger.addEventListener("click", function () {
      displaySidenav(buttons)
    })
    for (const btn of buttons){
      btn.addEventListener("click", function () {
      displaySidenav(buttons)
    })}
  }

const listenToUI = function () {
  // listen to slider
  setColor();
  listenToPwr();
  listenToCenterDog();
  listenToSidenav();
};

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
        lat = data.latitude
        longi = data.longitude
        const speed = data.speed
        var marker = L.marker([lat, longi]).addTo(map);
        const waardeHolders = document.querySelectorAll(".c-waarde_holder")
        for (const waarde of waardeHolders){
          if (waarde.getAttribute("eenheid-id") == 1){
            waarde.innerHTML = speed+" km/h"
          }
        }

      }
      else if(dataId == "$GPGGA"){
        lat = data.latitude
        longi = data.longitude
        var marker = L.marker([lat, longi]).addTo(map);
      }
    
  }})

  socketio.on("B2F_stap",function (jsonObject) {
    console.log("stap genomen ", jsonObject)
    const waardeHolders = document.querySelectorAll(".c-waarde_holder")
    for (const holder of waardeHolders){
      const eenheidID = holder.getAttribute("eenheid-id")
      if (eenheidID == 2){
        holder.innerHTML = jsonObject.stap.waarde
      }
    }
  })

  socketio.on("B2F_curr_hue", function (jsonObject) {
    console.log(jsonObject.hue)
    document.querySelector(".c-slider").value = jsonObject.hue
  })

  socketio.on("B2F_meest_recente_data",function (jsonObject) {
    console.log('json:',  jsonObject)
    const waardes = document.querySelectorAll(".c-waarde_holder");
    // set sensor data
    for (const waarde of waardes){
      let eenheidID = waarde.getAttribute("eenheid-id");
      const el = jsonObject.data
      for (const i of el){
        // console.log(eenheidID, i)
        if (eenheidID == 1 && i.eenheidid == 1){
          // snelheid
          waarde.innerHTML = i.waarde+" "+i.eenheid
        }
        else if (eenheidID == 2 && i.eenheidid == 2){
          //stappen
          waarde.innerHTML = i.waarde
        }      
        else if (i.eenheidid == 3){
          lat = i.waarde
        }
        else  if (i.eenheidid == 4){
          longi = i.waarde
        }
        else if (eenheidID == 5 && i.eenheidid == 5){
          // bpm
          waarde.innerHTML = i.waarde+" "+i.eenheid
        }
        else if (i.eenheidid == 7 && eenheidID == 7){
          // temperatuur
          waarde.innerHTML = i.waarde+" "+i.eenheid
        }
        // set location
    }
    }
    map.panTo(new L.LatLng(lat, longi));
    var marker = L.marker([lat, longi]).addTo(map);
  })

  socketio.on("B2F_historiek", function (jsonObject) {
    console.log(jsonObject)
    const historiek = jsonObject.historiek
    const dataSerie = options.series
    for (const el of historiek){ 
      // time sorting properties
      const date = new Date(el.x);
      const dateTimestamp = date.getTime();

      switch (el.eenheidid){
        case 1:
          dataSerie[0].data.push([el.x, el.y])
          break;
        case 2:
          dataSerie[1].data.push([dateTimestamp, el.y])
          break;
        case 5:
          dataSerie[2].data.push([el.x, el.y])
          break;
        case 7:
          dataSerie[3].data.push([el.x, el.y])
          break;
      }
    }
    console.log(dataSerie)
  })
};

const show_graph_hr = function () { // heartrate
  var options_hr = {
    chart: {
      type: 'line',
      height: '100%',
      width: '100%',
    },
    series: [{
      name: 'heartrate',
      data: [[1, 130], [2, 120], [3, 90], [4, 85], [5, 40], [6, 132], [7, 112]],
    }],
    xaxis: {
      type: 'datetime',
      // categories: []
    },
    tooltip: {
      shared: false,
      intersect: false,
      y: {
        formatter: function (y) {
          if (typeof y !== "undefined") {
            return y.toFixed(0) + " bpm";
          }
          return y;
        }
      }
    },
    title: {
      text: 'heartrate',
      align: 'left',
      style:{
        fontSize: '24px',
        fontFamily: 'Co Text'
      }
    }
  }

  var chart_hr = new ApexCharts(document.querySelector(".g-heartrate"), options_hr);
  chart_hr.render();
}

const show_graph_spd = function () { //speed
     
    var options_spd = {
    chart: {
      type: 'area',
      height: '100%',
      width: '100%',
    },
    series: [{
      name: 'speed',
      data: [[1, 30],[2, 32],[3, 23],[4, 21],[5, 15],[6, 13]],
    }],
    xaxis: {
      type: 'datetime',
      // categories: []
    },
    tooltip: {
      shared: false,
      intersect: false,
      y: {
        formatter: function (y) {
          if (typeof y !== "undefined") {
            return y.toFixed(0) + " km/h";
          }
          return y;
        }
      }
    },
    title: {
      text: 'speed',
      align: 'left',
      style:{
        fontSize: '24px',
        fontFamily: 'Co Text'
      }
    }
  }
  var chart_spd = new ApexCharts(document.querySelector(".g-speed"), options_spd);
  chart_spd.render();
}

const show_graph_temp = function () { //temperature
     
  var options_temp = {
    chart: {
      type: 'line',
      height: '100%',
      width: '100%',
    },
    series: [{
      name: 'temp',
      data: [[1, 30],[2, 32],[3, 23],[4, 21],[5, 15],[6, 13]],
    }],
    xaxis: {
      type: 'datetime',
      // categories: []
    },
    tooltip: {
      shared: false,
      intersect: false,
      y: {
        formatter: function (y) {
          if (typeof y !== "undefined") {
            return y.toFixed(0) + " °C";
          }
          return y;
        }
      }
    },
    title: {
      text: 'temperature',
      align: 'left',
      style:{
        fontSize: '24px',
        fontFamily: 'Co Text'
      }
    }
  
  }
  var chart_temp = new ApexCharts(document.querySelector(".g-temperature"), options_temp);
  chart_temp.render();
}

const show_graph_steps = function () {
     
  var options_steps = {
    chart: {
      type: 'bar',
      height: '100%',
      width: '100%',
    },
    series: [{
      name: 'steps',
      data: [[1, 50000],[2, 75000],[3, 10023],[4, 10000],[5, 20000],[6, 50333]],
    }],
    xaxis: {
      type: 'datetime',
      // categories: []
    },
    tooltip: {
      shared: false,
      intersect: false,
      y: {
        formatter: function (y) {
          if (typeof y !== "undefined") {
            return y.toFixed(0) + " steps";
          }
          return y;
        }
      }
    },
    title: {
      text: 'steps',
      align: 'left',
      style:{
        fontSize: '24px',
        fontFamily: 'Co Text'
      }
    }
  }
  var chart_steps = new ApexCharts(document.querySelector(".g-steps"), options_steps);
  chart_steps.render();
}

const show_graphs = function () {
  show_graph_hr();
  show_graph_spd();
  show_graph_temp();
  show_graph_steps();
}

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  listenToUI();
  init_map();
  listenToSocket();
  show_graphs();
});

