"use strict";

const lanIP = `${window.location.hostname}:5000`;
const socketio = io(`http://${lanIP}`);
const provider = "https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png";
// zo kunnen we options aanpassen via socketio
var options;
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

const setColor = function () {
  const slider = document.querySelector(".c-slider")
  // ook bij inladen pagina
  socketio.emit("F2B_set_color", {"hue": slider.value})
  console.log("new slider value sent")
  slider.addEventListener("click", function () {
    socketio.emit("F2B_set_color", {"hue": slider.value})
    console.log("new slider value sent")
  })
}

const listenToUI = function () {
  // listen to slider
  setColor();

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
        const lat = data.latitude/100
        const longi = data.longitude/100
        const speed = data.speed
        map.panTo(new L.LatLng(lat, longi));
        const waardeHolders = document.querySelectorAll(".c-waarde_holder")
        for (const waarde of waardeHolders){
          if (waarde.getAttribute("eenheid-id") == 1){
            waarde.innerHTML = speed+" km/h"
          }
        }

      }
      else if(dataId == "$GPGGA"){
        const lat = data.latitude/100
        const longi = data.longitude/100 
        map.panTo(new L.LatLng(lat, longi));
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

  socketio.on("B2F_meest_recente_data",function (jsonObject) {
    // console.log(jsonObject)
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
        else if (eenheidID == 5 && i.eenheidid == 5){
          // bpm
          waarde.innerHTML = i.waarde+" "+i.eenheid
        }
        else if (i.eenheidid == 7 && eenheidID == 7){
          // temperatuur
          waarde.innerHTML = i.waarde+" "+i.eenheid
        }
        
    }
    }
    
    // set location
    const lat = jsonObject.data[3].waarde/100
    const longi = jsonObject.data[4].waarde/100
    console.log("3")
    map.panTo(new L.LatLng(lat, longi)); 
  })
  socketio.on("B2F_historiek", function (jsonObject) {
    const historiek = jsonObject.historiek;
    console.log(historiek)
    console.log(options)
    // options.labels = [""]
    for (const el of historiek){
      options.labels.push((el.tijdstip))
      if (el.eenheidid == 1){
        
      }
    }
    // {eenheidid: 5, waarde: '33', tijdstip: '03/06/2022', eenheid: 'bpm'}
    // show_graph();
  })
};

const show_graph = function () {
     
  options = {
    series: [{
    name: 'stappen',
    type: 'column',
    data: []
  }, {
    name: 'speed',
    type: 'area',
    data: []
  }, {
    name: 'temperature',
    type: 'line',
    data: []
  }, {
    name: 'heartrate',
    type: 'line',
    data: []
  }],
    chart: {
    height: '350px',
    type: 'line',
    stacked: false,
  },
  stroke: {
    width: [0, 2, 5],
    curve: 'smooth'
  },
  plotOptions: {
    bar: {
      columnWidth: '50%'
    }
  },
  
  fill: {
    opacity: [0.85, 0.25, 1],
    gradient: {
      inverseColors: false,
      shade: 'light',
      type: "vertical",
      opacityFrom: 0.85,
      opacityTo: 0.55,
      stops: [0, 100, 100, 100]
    }
  },
  labels: [],
  markers: {
    size: 0
  },
  xaxis: {
    type: 'datetime'
  },
  yaxis: {
    title: {
      text: '',
    },
    min: 0
  },
  tooltip: {
    shared: true,
    intersect: false,
    y: {
      formatter: function (y) {
        if (typeof y !== "undefined") {
          return y.toFixed(0) + " eenheid";
        }
        return y;
  
      }
    }
  }
  };
  
  var chart = new ApexCharts(document.querySelector(".c-graph"), options);
  
  chart.render();
}

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  listenToUI();
  init_map();
  show_graph();
  listenToSocket();
});

