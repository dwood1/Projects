import React, { useState } from "react";
import ChartistGraph from "react-chartist";
import TradePanel from "../components/TradePanel";
import BotEditor from "../components/BotEditor";
import Select from "react-select";
import "../css/main.css";
import Chartist from "../../node_modules/chartist/";

const apiSignature = "http://localhost:5000";

const fillerData = {
  labels: ["A", "B", "C", "D", "E", "F"],
  series: [[1, 5, 2, 3, 6]],
};

var defaultOptions = {
  // Options for X-Axis
  axisX: {
    // The offset of the labels to the chart area
    offset: 30,
    // Position where labels are placed. Can be set to `start` or `end` where `start` is equivalent to left or top on vertical axis and `end` is equivalent to right or bottom on horizontal axis.
    position: "end",
    // Allows you to correct label positioning on this axis by positive or negative x and y offset.
    labelOffset: {
      x: 0,
      y: 0,
    },
    // If labels should be shown or not
    showLabel: true,
    // If the axis grid should be drawn or not
    showGrid: false,
    // Interpolation function that allows you to intercept the value from the axis label
    labelInterpolationFnc: function (value, index) {
      return index % 2 === 0 ? value : null;
    },
    // Set the axis type to be used to project values on this axis. If not defined, Chartist.StepAxis will be used for the X-Axis, where the ticks option will be set to the labels in the data and the stretch option will be set to the global fullWidth option. This type can be changed to any axis constructor available (e.g. Chartist.FixedScaleAxis), where all axis options should be present here.
    type: undefined,
  },
  // Options for Y-Axis
  axisY: {
    // The offset of the labels to the chart area
    offset: 0,
    // Position where labels are placed. Can be set to `start` or `end` where `start` is equivalent to left or top on vertical axis and `end` is equivalent to right or bottom on horizontal axis.
    position: "start",
    // Allows you to correct label positioning on this axis by positive or negative x and y offset.
    labelOffset: {
      x: 0,
      y: 10,
    },
    // If labels should be shown or not
    showLabel: true,
    // If the axis grid should be drawn or not
    showGrid: true,
    // Interpolation function that allows you to intercept the value from the axis label
    labelInterpolationFnc: function (value, index) {
      return index % 2 === 0 ? value : null;
    },
    // Set the axis type to be used to project values on this axis. If not defined, Chartist.AutoScaleAxis will be used for the Y-Axis, where the high and low options will be set to the global high and low options. This type can be changed to any axis constructor available (e.g. Chartist.FixedScaleAxis), where all axis options should be present here.
    type: undefined,
    // This value specifies the minimum height in pixel of the scale steps
    scaleMinSpace: 20,
    // Use only integer values (whole numbers) for the scale steps
    onlyInteger: false,
  },
  // Specify a fixed width for the chart as a string (i.e. '100px' or '50%')
  width: undefined,
  // Specify a fixed height for the chart as a string (i.e. '100px' or '50%')
  height: undefined,
  // If the line should be drawn or not
  showLine: true,
  // If dots should be drawn or not
  showPoint: false,
  // If the line chart should draw an area
  showArea: false,
  // The base for the area chart that will be used to close the area shape (is normally 0)
  areaBase: 0,
  lineSmooth: true,
  showGridBackground: false,
  low: undefined,
  high: undefined,
  chartPadding: {
    top: 15,
    right: 15,
    bottom: 5,
    left: 10,
  },
  fullWidth: false,
  reverseData: false,
  classNames: {
    chart: "ct-chart-line",
    label: "ct-label-1",
    labelGroup: "ct-labels",
    series: "ct-series",
    line: "ct-line",
    point: "ct-point",
    area: "ct-area",
    grid: "ct-grid-1",
    gridGroup: "ct-grids",
    gridBackground: "ct-grid-background",
    vertical: "ct-vertical",
    horizontal: "ct-horizontal",
    start: "ct-start",
    end: "ct-end",
  },
  // plugins: [
  //   Chartist.plugins.zoom({
  //     onZoom: onZoom,
  //   }),
  // ],
};

var resetFnc;
function onZoom(chart, reset) {
  resetFnc = reset;
}

var keyCounter = 0;

function App() {
  const [data, setData] = useState(fillerData);
  const [chartOptions, setChartOptions] = useState(defaultOptions);
  const [type, setType] = useState("Line");
  const [charts, setCharts] = useState([]);
  const [botNames, setBotNames] = useState([]);
  const [bot, setBot] = useState();

  function renderChart(input_data) {
    let temp = data;
    temp.series = input_data;
    setData(temp);
    console.log(data);

    var newChart = (
      <div className="graph-container">
        <ChartistGraph
          key={keyCounter++}
          className="margin-top-bottom border-white ct-octave"
          data={data}
          options={chartOptions}
          type={type}
        />
      </div>
    );

    if (newChart !== null) {
      setCharts([...charts, newChart]);
    }
  }

  function executeOnBotSaved(source) {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: source.name,
        buy_behaviors: source.buy_behaviors,
        sell_behaviors: source.sell_behaviors,
      }),
    };
    fetch(`${apiSignature}/api/save_bot/`, requestOptions)
      .then((res) => res.json())
      .then(
        (result) => {
          setBot(source);
          getBotNames();
        },
        (error) => {
          console.log("Error");
        }
      );
  }

  function executeOnBehaviorTested(source, days = 30) {
    if (validateBehavior(source)) {
      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          days: days,
          token: "BTC",
          asset: "USDT",
          behavior: source,
        }),
      };
      fetch(`${apiSignature}/api/test_behavior/`, requestOptions)
        .then((res) => res.json())
        .then(
          (result) => {
            renderChart(result);
          },
          (error) => {
            console.log("Error");
          }
        );
    }
  }

  function validateBehavior(behavior) {
    if (
      "function" in behavior &&
      "inputs" in behavior &&
      "condition" in behavior &&
      "target" in behavior
    ) {
      if (
        behavior.condition === "greater_than" ||
        behavior.condition === "less_than" ||
        behavior.condition === "equal_to" ||
        behavior.condition === "greater_than_or_equal_to" ||
        behavior.condition === "less_than_or_equal_to"
      ) {
        if (
          behavior.function === "moving_average" ||
          behavior.function === "resistance" ||
          behavior.function === "support" ||
          behavior.function === "moving_variance" ||
          behavior.function === "moving_deviation" ||
          behavior.function === "moving_tdssd" ||
          behavior.function === "moving_max" ||
          behavior.function === "moving_min" ||
          behavior.function === "linear_regression_forecast" ||
          behavior.function === "momentum"
        ) {
          if (
            "interval" in behavior.inputs &&
            typeof behavior.inputs.interval === "number"
          ) {
            return true;
          }
        } else if (
          behavior.function === "resistance_trendline" ||
          behavior.function === "support_trendline"
        ) {
          if (
            "interval" in behavior.inputs &&
            typeof behavior.inputs.interval === "number" &&
            "wg" in behavior.inputs &&
            typeof behavior.inputs.wg === "number"
          ) {
            return true;
          }
        }
      }
    }
    return false;
  }

  function getBotNames() {
    // /api/get_bot_names/
    var names = [];
    var keyCounter = 1;
    const requestOptions = {
      method: "GET",
    };
    return fetch(`${apiSignature}/api/get_bots/`, requestOptions)
      .then((res) => res.json())
      .then(
        (result) => {
          result.forEach((element) => {
            let newBot = { value: element.name, label: element.name };
            names.push(newBot);
          });

          if (JSON.stringify(names) !== JSON.stringify(botNames)) {
            setBotNames(names);
          }
        },
        (error) => {
          console.log("Error");
        }
      );
  }

  function onBotNameSelected(e) {
    // GET
    // /api/get_bot/{e.target.value}
    if (e.value !== undefined && e.value !== "") {
      const requestOptions = {
        method: "GET",
      };
      fetch(`${apiSignature}/api/get_bot/${e.value}`, requestOptions)
        .then((res) => res.json())
        .then(
          (result) => {
            setBot(result);
          },
          (error) => {
            console.log("Error");
          }
        );
    }
  }

  if (botNames.length === 0) {
    getBotNames();
  }

  return (
    <div className="App">
      <div id="grid-main" className="grid" style={{ padding: 10 }}>
        <div style={{ gridRow: 1, gridColumn: 1 }}>
          <Select
            value={
              bot === undefined ? null : { label: bot.name, value: bot.name }
            }
            options={botNames}
            onChange={onBotNameSelected}
          />
          <BotEditor
            onSave={executeOnBotSaved}
            source={bot === undefined ? {} : bot}
            onBehaviorTested={executeOnBehaviorTested}
          />
          <TradePanel
            apiSignature={apiSignature}
            onDataSubmit={renderChart}
            source={bot === undefined ? {} : bot}
          />
        </div>
        <div style={{ gridRow: 1, gridColumn: 2 }}>{charts}</div>
      </div>
    </div>
  );
}

export default App;
