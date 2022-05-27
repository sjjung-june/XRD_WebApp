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
          data[key].Peaks_Height,
          data[key].Peaks_Id
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

function plotData(SN, File, Angle, Count, Peaks_Pos, Peaks_Height, Peaks_Id) {
  colors = [];
  sizes = [];
  for (var i = 0; i < Angle.length; i++) {
    colors.push("C1C1C1");
  }
  let NAME = document.getElementById(`${File}_file_name`);
  let PLOT = document.getElementById(`${File}_plot_div`);
  let PEAKS_DIV = document.getElementById(`${File}_peaks_div`);

  NAME.innerHTML = `${File}`;
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

    let POINT_ANGLE = Angle[pn].toPrecision(4).toString();
    let POINT_COUNT = Count[pn].toPrecision(4).toString();

    PEAKS_DIV.innerHTML += `<div class="peaks_div_content" id=${File}_${POINT_ANGLE}_${POINT_COUNT} style="text-align:center"><input type="checkbox" class="peak_id_check" id=${File}_${POINT_ANGLE}_${POINT_COUNT}_check /><label> ${POINT_ANGLE} </label><button id=${File}_${POINT_ANGLE}_${POINT_COUNT}_btn class="peak_del_btn" style="margin:0 auto;">X</button></div>`;

    Peaks_Pos.push(Angle[pn].toPrecision(4).toString());
    Peaks_Height.push(Count[pn].toPrecision(4).toString());
    Peaks_Id.push(false);

    const peak_del_btns = document.querySelectorAll(".peak_del_btn");
    const peak_id_checks = document.querySelectorAll(".peak_id_check");

    peak_del_btns.forEach((peak_del_btn) => {
      try {
        peak_del_btn.removeEventListener("click", handleDel);
      } finally {
        peak_del_btn.addEventListener("click", handleDel);
      }
    });

    peak_id_checks.forEach((peak_id_check) => {
      try {
        peak_id_check.removeEventListener("change", handleCheck);
      } finally {
        peak_id_check.addEventListener("change", handleCheck);
      }
    });

    console.log(Peaks_Pos);
    console.log(Peaks_Height);
    console.log(Peaks_Id);
  });
}

function add(id) {
  const file_name = document.createElement("span");
  const file_div = document.createElement("div");
  const plot_div = document.createElement("div");
  const peaks_div = document.createElement("div");

  file_name.setAttribute("id", `${id}_file_name`);
  file_div.setAttribute("id", `${id}_file_div`);
  file_div.setAttribute("class", `file_div`);
  plot_div.setAttribute("id", `${id}_plot_div`);
  peaks_div.setAttribute("id", `${id}_peaks_div`);
  peaks_div.setAttribute("class", `peaks_div`);

  document.getElementById("plots").appendChild(file_name);
  document.getElementById("plots").appendChild(file_div);
  document.getElementById(`${id}_file_div`).appendChild(plot_div);
  document.getElementById(`${id}_file_div`).appendChild(peaks_div);
}

function remove() {
  document.getElementById("plots").remove();
  const div = document.createElement("div");
  div.setAttribute("id", "plots");
  div.setAttribute("style", "width: 800px; height: 2000px");
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
  Peaks_Id = [];

  Object.keys(Data).forEach(function (key) {
    Peaks_Pos.push(Data[key].Peaks_Pos);
    Peaks_Height.push(Data[key].Peaks_Height);
    Peaks_Id.push(Data[key].Peaks_Id);
    Files.push(key);
  });

  let data = JSON.stringify({
    SN: submitInput.value,
    YEAR: yearInput.value,
    MONTH: monthInput.value,
    File: Files,
    Peaks_Pos: Peaks_Pos,
    Peaks_Height: Peaks_Height,
    Peaks_Id: Peaks_Id,
  });

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

function handleDel(event) {
  event.path[1].remove();
  const POS = event.target.id.split("_")[event.target.id.split("_").length - 3];
  const Key = `${event.target.id.split("_")[0]}_${
    event.target.id.split("_")[1]
  }_${event.target.id.split("_")[2]}`;

  const POS_idx = Data[Key].Peaks_Pos.indexOf(POS);

  Data[Key].Peaks_Pos.splice(POS_idx, 1);
  Data[Key].Peaks_Height.splice(POS_idx, 1);
  Data[Key].Peaks_Id.splice(POS_idx, 1);

  console.log(Data[Key].Peaks_Pos);
  console.log(Data[Key].Peaks_Height);
  console.log(Data[Key].Peaks_Id);
}

function handleCheck(event) {
  const POS = event.target.id.split("_")[event.target.id.split("_").length - 3];
  const Key = `${event.target.id.split("_")[0]}_${
    event.target.id.split("_")[1]
  }_${event.target.id.split("_")[2]}`;

  const POS_idx = Data[Key].Peaks_Pos.indexOf(POS);

  if (Data[Key].Peaks_Id[POS_idx]) {
    Data[Key].Peaks_Id[POS_idx] = false;
  } else {
    Data[Key].Peaks_Id[POS_idx] = true;
  }

  console.log(Data[Key].Peaks_Pos);
  console.log(Data[Key].Peaks_Height);
  console.log(Data[Key].Peaks_Id);
}

submitForm.addEventListener("submit", handleSNSubmit);
modify_btn.addEventListener("click", handleModify);
reset_btn.addEventListener("click", handleReset);
submitInput.addEventListener("click", handleClick);
yearInput.addEventListener("click", yearInit);
yearInput.addEventListener("change", handleChange);
monthInput.addEventListener("click", monthInit);
monthInput.addEventListener("change", handleChange);
