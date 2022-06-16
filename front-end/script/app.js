"use strict";

let lat, longi
const lanIP = `${window.location.hostname}:5000`;
const socketio = io(`http://${lanIP}`);
const provider = "https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png";
// zo kunnen we options aanpassen via socketio
var options_hr, options_spd, options_temp, options_steps;
var chart_hr, chart_spd, chart_steps, chart_temp;
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
  // console.log("new slider value sent")
  document.querySelector('.c-curr_color').style.background = `hsl(${Math.round(((slider.value)/255)*360)}, 100%, 50%)`
  slider.addEventListener("change", function () {
    document.querySelector('.c-curr_color').style.background = `hsl(${Math.round(((slider.value)/255)*360)}, 100%, 50%)`
    socketio.emit("F2B_set_color", {"hue": slider.value})
    // console.log("new slider value sent")
    const presets = document.querySelectorAll(".js-preset")
    for (const color of presets){
      color.classList.remove('c-selected_color')
    }

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
    // console.log(buttons)
    toggleTrigger.addEventListener("click", function () {
      displaySidenav(buttons)
    })
    for (const btn of buttons){
      btn.addEventListener("click", function () {
      displaySidenav(buttons)
    })}
}

const listenToPresets = function () {
  const presets = document.querySelectorAll(".js-preset")
  // console.log(presets)
  for (const color of presets){
    color.addEventListener('click', function () {
      for (const color of presets){
        color.classList.remove('c-selected_color')
      }
      // presets.classList.remove('c-selected_color');
      color.classList.add('c-selected_color');
      const kleurId = color.getAttribute("kleur-id")
      // console.log(kleurId)
      switch (kleurId){
        case '0':
          document.querySelector('.c-curr_color').style.background = 'linear-gradient(to bottom right, #FF0018, #FFA52C, #FFFF41, #008018, #0000F9, #86007D)'
          socketio.emit('F2B_set_color', {'hue': 'pride'})
          break
        case '1':
          document.querySelector('.c-curr_color').style.background = 'white'
          socketio.emit('F2B_set_color', {'hue': 'white'})
          // console.log("white!!")
          break
      }
    })
  }
}

const listenToUI = function () {
  setColor();
  listenToPwr();
  listenToCenterDog();
  listenToSidenav();
  listenToPresets();
};

const listenToSocket = function () {

  socketio.on("connected", () => {
    console.log("sio connect"); // true
  });
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
        console.log(lat, longi, lat != null && longi != null)
        if (lat != null && longi != null)
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
    const presets = ['pride', 'white']
    console.log(presets.includes(jsonObject.hue))
    if (presets.includes(jsonObject.hue)){
      switch (jsonObject.hue){
        case 'pride':
          for (const el of document.querySelectorAll('.js-preset')) {
            el.classList.remove("c-selected_color")
            if (el.getAttribute('kleur-id') == 0){
              el.classList.add("c-selected_color")
            }
          }
          document.querySelector('.c-curr_color').style.background = 'linear-gradient(to bottom right, #FF0018, #FFA52C, #FFFF41, #008018, #0000F9, #86007D)'
          break

        case 'white':
          for (const el of document.querySelectorAll('.js-preset')) {
            el.classList.remove("c-selected_color")
            if (el.getAttribute('kleur-id') == 1){
              console.log(el)
              el.classList.add("c-selected_color")
            }
          }         
          document.querySelector('.c-curr_color').style.background = 'white'
          break
      }
    }
    else{
      for (const el of document.querySelectorAll('.js-preset')) {
        el.classList.remove("c-selected_color")          
        }
      document.querySelector(".c-slider").value = jsonObject.hue
      document.querySelector('.c-curr_color').style.background = `hsl(${Math.round(((document.querySelector(".c-slider").value)/255)*360)}, 100%, 50%)`
    }
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
    console.log(lat, longi, lat != null && longi != null)
    if (lat != null && longi != null) {
    map.panTo(new L.LatLng(lat, longi));
    var marker = L.marker([lat, longi]).addTo(map);
  }
  })

  socketio.on("B2F_status_led", function (jsonObject) {
    const statusLed = jsonObject.status;
    document.querySelector(".js-status").innerHTML = statusLed;
  })
};

// #region graphs
const show_graph_hr = function () { // heartrate
  options_hr = {
    chart: {
      type: 'line',
      height: '100%',
      width: '100%',
    },
    series: [{
      name: 'heartrate',
      data: [],
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

  chart_hr = new ApexCharts(document.querySelector(".g-heartrate"), options_hr);
}

const show_graph_spd = function () { //speed
    
    options_spd = {
    chart: {
      type: 'area',
      height: '100%',
      width: '100%',
    },
    series: [{
      name: 'speed',
      data: [],
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
  chart_spd = new ApexCharts(document.querySelector(".g-speed"), options_spd);
}

const show_graph_temp = function () { //temperature
    
  options_temp = {
    chart: {
      type: 'line',
      height: '100%',
      width: '100%',
    },
    series: [{
      name: 'temp',
      data: [],
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
  chart_temp = new ApexCharts(document.querySelector(".g-temperature"), options_temp);
}

const show_graph_steps = function () {
    
  options_steps = {
    chart: {
      type: 'bar',
      height: '100%',
      width: '100%',
    },
    series: [{
      name: 'steps',
      data: [],
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
  chart_steps = new ApexCharts(document.querySelector(".g-steps"), options_steps);
}

const show_graphs = function () {
  show_graph_hr();
  show_graph_spd();
  show_graph_temp();
  show_graph_steps();
}

const renderGraphs = function () {
  chart_hr.render();
  chart_spd.render();
  chart_temp.render();
  chart_steps.render();
}
// #endregion

const getHistory = function (jsonObject) {
  // console.log('history: ',jsonObject)
  const historiek = jsonObject
  console.log(jsonObject)
  // console.log('options ', options_hr)
  console.log(options_hr)
  const dataSerie_hr = options_hr.series[0]
  const dataSerie_spd = options_spd.series[0]
  const dataSerie_temp = options_temp.series[0]
  const dataSerie_steps = options_steps.series[0]
  for (const el of historiek){ 
    // time sorting properties
    const date = new Date(el.x);
    const dateTimestamp = date.getTime();

    switch (el.eenheidid){
      case 1:
        dataSerie_spd.data.push([el.x, el.y])
        break;
      case 2:
        dataSerie_steps.data.push([dateTimestamp, el.y])
        break;
      case 5:
        dataSerie_hr.data.push([el.x, el.y])
        break;
      case 7:
        console.log(dataSerie_temp)
        dataSerie_temp.data.push([el.x, el.y])
        break;
    }
  }
  renderGraphs();
  // console.log('route returned',historiek)
}

const handleHistory = function () {
  const url = `http://${lanIP}/api/v1/historiek/day/`;
  handleData(url, getHistory);
  
}

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
    listenToUI();
    init_map();
    listenToSocket();
    show_graphs();
    handleHistory();
});