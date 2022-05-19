const DEFAULT_URL = "http://10.138.126.181:5000";
const submitForm = document.querySelector("#submit-form");
const yearInput = document.querySelector("#year-input");
const monthInput = document.querySelector("#month-input");
const submitInput = document.querySelector("#submit-input");
const SNBrowser = document.querySelector("#sn-browsers");
const fileBrowser = document.querySelector("#file-browsers");
const fileInput = document.querySelector("#file-input");
const modify_btn = document.querySelector("#modify-button");
const monthBrowser = document.querySelector("#month-browsers");
const reset_btn = document.querySelector("#reset-button");
const plots_parent = document.querySelector("#plots-parent");
const plots = document.querySelector("#plots");
const STATUS = document.querySelector(".status");
var Data;

getDate();

function getDate() {
  Current_Date = new Date();
  yearInput.value = Current_Date.getFullYear();

  if (Current_Date.getMonth() < 9) {
    monthInput.value = `0${Current_Date.getMonth() + 1}`;
  } else {
    monthInput.value = Current_Date.getMonth() + 1;
  }
}

function handleSNSubmit(event) {
  event.preventDefault();

  if (submitInput.value != "") {
    STATUS.classList.toggle("loading");

    let xhr = new XMLHttpRequest();
    xhr.open("POST", `${DEFAULT_URL}/submit`);
    xhr.setRequestHeader("Accept", "application/json");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onload = function () {
      File_List = JSON.parse(xhr.response);

      data = File_List[submitInput.value];

      Object.keys(data).forEach(function (key) {
        add(key);
        plotData(
          submitInput.value,
          key,
          data[key].Angle,
          data[key].Count,
          data[key].Peaks_Pos,
          data[key].Peaks_Height
        );
      });

      Data = data;
      STATUS.classList.toggle("loading");
      modify_btn.classList.toggle("hidden");
    };

    let data = JSON.stringify({
      SN: `${submitInput.value}`,
      YEAR: `${yearInput.value}`,
      MONTH: `${monthInput.value}`,
    });
    xhr.send(data);
  }
}

function plotData(SN, File, Angle, Count, Peaks_Pos, Peaks_Height) {
  colors = [];
  sizes = [];
  for (var i = 0; i < Angle.length; i++) {
    colors.push("C1C1C1");
  }
  let PLOT = document.getElementById(`${File}_plot`);
  let SPAN = document.getElementById(`${File}_span`);
  SPAN.innerHTML = File;
  var myPlot = PLOT,
    Angle,
    Count,
    data = [
      {
        x: Angle,
        y: Count,
        type: "scatter",
        mode: "markers",
        marker: { color: colors, size: 4 },
      },
    ];
  Plotly.newPlot(PLOT, data);
  myPlot.on("plotly_click", function (data) {
    var pn = "",
      tn = "",
      colors = [];

    for (var i = 0; i < data.points.length; i++) {
      pn = data.points[i].pointNumber;
      tn = data.points[i].curveNumber;
      colors = data.points[i].data.marker.color;
    }

    if (colors[pn] != "#FF0000") {
      colors[pn] = "#FF0000";
      Peaks_Pos.push(Angle[pn].toPrecision(4));
      Peaks_Height.push(Count[pn].toPrecision(4));
    } else {
      colors[pn] = "#C1C1C1";
      Peaks_Pos = arrayRemove(Peaks_Pos, Angle[pn].toPrecision(4).toString());
      Peaks_Height = arrayRemove(
        Peaks_Height,
        Count[pn].toPrecision(4).toString()
      );
    }

    var update = { marker: { color: colors, size: 4 } };
    Plotly.restyle(`${File}_plot`, update, [tn]);
    SPAN.innerHTML = `${File} : ${Peaks_Pos}`;
  });
}

function add(id) {
  const span = document.createElement("span");
  const div = document.createElement("div");
  span.setAttribute("id", `${id}_span`);
  div.setAttribute("id", `${id}_plot`);
  document.getElementById("plots").appendChild(span);
  document.getElementById("plots").appendChild(div);
}

function remove() {
  document.getElementById("plots").remove();
  const div = document.createElement("div");
  div.setAttribute("id", "plots");
  div.setAttribute("style", "width: 1100px; height: 2000px");
  document.getElementById("plots-parent").appendChild(div);
  submitInput.value = "";
}
function handleClick(event) {
  let current_value = document.querySelector(`#${event.path[0].id}`).value;
  if (current_value != "") {
    document.querySelector(`#${event.path[0].id}`).value = "";
  }
}

function arrayRemove(arr, value) {
  return arr.filter(function (ele) {
    return ele != value;
  });
}

function handleModify(event) {
  event.preventDefault();

  let xhr = new XMLHttpRequest();
  xhr.open("POST", `${DEFAULT_URL}/calc`);
  xhr.setRequestHeader("Accept", "application/json");
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onload = function () {
    remove();
    modify_btn.classList.toggle("hidden");
    alert(xhr.response);
  };

  Files = [];
  Peaks_Pos = [];
  Peaks_Height = [];

  Object.keys(Data).forEach(function (key) {
    Peaks_Pos.push(Data[key].Peaks_Pos);
    Peaks_Height.push(Data[key].Peaks_Height);
    Files.push(key);
  });

  let data = JSON.stringify({
    SN: submitInput.value,
    YEAR: yearInput.value,
    MONTH: monthInput.value,
    File: Files,
    Peaks_Pos: Peaks_Pos,
    Peaks_Height: Peaks_Height,
  });

  console.log(data);

  xhr.send(data);
  alert("결과가 전달되었습니다. 잠시만 기다려주세요.");
}

function handleReset() {
  remove();
  modify_btn.classList.toggle("hidden");
}

function yearInit() {
  yearInput.value = "";
  monthInput.value = "";
  submitInput.value = "";
}

function monthInit() {
  monthInput.value = "";
}

function handleChange() {
  let xhr = new XMLHttpRequest();
  xhr.open("POST", `${DEFAULT_URL}/main`);
  xhr.setRequestHeader("Accept", "application/json");
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onload = function () {
    Month_List = JSON.parse(xhr.response)["Month_List"];
    SN_List = JSON.parse(xhr.response)["SN_List"];

    Months = "";

    for (var i = 0; i < Month_List.length; i++) {
      Months += `<option value=${Month_List[i]}></option>`;
    }
    monthBrowser.innerHTML = Months;

    SNs = "";

    for (var i = 0; i < SN_List.length; i++) {
      SNs += `<option value=${SN_List[i]}></option>`;
    }
    SNBrowser.innerHTML = SNs;
  };

  let data = JSON.stringify({
    YEAR: yearInput.value,
    MONTH: monthInput.value,
  });

  xhr.send(data);
}

submitForm.addEventListener("submit", handleSNSubmit);
modify_btn.addEventListener("click", handleModify);
reset_btn.addEventListener("click", handleReset);
submitInput.addEventListener("click", handleClick);
yearInput.addEventListener("click", yearInit);
yearInput.addEventListener("change", handleChange);
monthInput.addEventListener("click", monthInit);
monthInput.addEventListener("change", handleChange);
