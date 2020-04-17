import React, { useState, useEffect } from "react";
import Select from "react-select";

const functions = [
  {
    value: "moving_average",
    label: "Moving Average",
    inputs_placeholder: "e.g. {'interval': 1440}",
  },
  {
    value: "resistance",
    label: "Resistance",
    inputs_placeholder: "e.g. {'interval': 1440}",
  },
  {
    value: "support",
    label: "Support",
    inputs_placeholder: "e.g. {'interval': 1440}",
  },
  {
    value: "resistance_trendline",
    label: "Resistance Trendline",
    inputs_placeholder: "e.g. {'interval': 1440, 'wg': 0.5}",
  },
  {
    value: "support_trendline",
    label: "Support Trendline",
    inputs_placeholder: "e.g. {'interval': 1440, 'wg': 0.5}",
  },
  {
    value: "moving_variance",
    label: "Moving Variance",
    inputs_placeholder: "e.g. {'interval': 1440}",
  },
  {
    value: "moving_deviation",
    label: "Moving Deviation",
    inputs_placeholder: "e.g. {'interval': 1440}",
  },
  {
    value: "moving_tdssd",
    label: "Moving TDSSD",
    inputs_placeholder: "e.g. {'interval': 1440}",
  },
  {
    value: "moving_max",
    label: "Moving Max",
    inputs_placeholder: "e.g. {'interval': 1440}",
  },
  {
    value: "moving_min",
    label: "Moving Min",
    inputs_placeholder: "e.g. {'interval': 1440}",
  },
  {
    value: "linear_regression_forecast",
    label: "Linear Regression",
    inputs_placeholder: "e.g. {'interval': 1440}",
  },
  {
    value: "momentum",
    label: "Time-series Momentum",
    inputs_placeholder: "e.g. {'interval': 1440}",
  },
];

const conditions = [
  { value: "greater_than", label: ">" },
  { value: "greater_than_or_equal_to", label: ">=" },
  { value: "less_than", label: "<" },
  { value: "less_than_or_equal_to", label: "<=" },
  { value: "equal_to", label: "==" },
];

var key = 0;

const BehaviorLeaf = (props) => {
  const [source, setSource] = useState(props.source);
  const [func, setFunc] = useState();
  const [condition, setCondition] = useState();
  const [inputs, setInputs] = useState();
  const [target, setTarget] = useState();
  // TODO -- allows for numeric, or $ = current price
  // (allows for algebra on $ such as $*1.15 which = current_price*1.15)
  // TODO -- error handling for test button
  useEffect(() => {
    setSource(props.source);
    functions.forEach((element) => {
      if (element.value === props.source.function) {
        setFunc(element);
      }
    });
    conditions.forEach((element) => {
      if (element.value === props.source.condition) {
        setCondition(element);
      }
    });
    setTarget(props.source.target);
    setInputs(JSON.stringify(props.source.inputs));
    key = props.keyProp;
  }, [props.source, props.keyProp]);

  function onFunctionSelected(e) {
    //console.log("Function: " + JSON.stringify(e));
    setFunc(e);
    let temp = source;
    temp.function = e.value;
    setSource(temp);
  }

  function onInputFieldChanged(e) {
    //console.log("Input: " + JSON.stringify(source));
    setInputs(e.target.value);
    let temp = source;
    let jsonInputs = JSON.parse(e.target.value);
    temp.inputs = jsonInputs || temp.input;
    setSource(temp);
  }

  function onConditionSelected(e) {
    //console.log("Condition: " + JSON.stringify(source));
    setCondition(e);
    let temp = source;
    temp.condition = e.value;
    setSource(temp);
  }

  function onTargetFieldChanged(e) {
    //console.log("Target: " + JSON.stringify(source));
    setTarget(e.target.value);
    let temp = source;
    temp.target = e.target.value;
    setSource(temp);
  }

  return (
    <div className="leaf flex-row">
      <div className="label-container" style={{ width: "15vw" }}>
        <label>function</label>
        <Select
          value={func}
          onChange={onFunctionSelected}
          options={functions}
        />
      </div>
      <div className="label-container" style={{ width: "10vw" }}>
        <label>inputs</label>
        <input
          type="text"
          value={inputs}
          onChange={onInputFieldChanged}
          placeholder={func && func.inputs_placeholder}
        />
      </div>
      <div className="label-container" style={{ width: "5vw" }}>
        <label>condition</label>
        <Select
          value={condition}
          onChange={onConditionSelected}
          options={conditions}
        />
      </div>
      <div className="label-container" style={{ width: "10vw" }}>
        <label>target</label>
        <input type="text" value={target} onChange={onTargetFieldChanged} />
      </div>
      <button
        className="test-btn"
        onClick={() => props.onBehaviorTested(props.source, 30)}
        style={{ width: "5vw" }}>
        Test
      </button>
      <button
        className="delete-btn"
        onClick={() => props.delete()}
        style={{ width: "5vw" }}>
        X
      </button>
    </div>
  );
};

const customStyles = {
  // option: (provided, state) => ({
  //   ...provided,
  //   borderBottom: "1px dotted pink",
  //   color: state.isSelected ? "red" : "blue",
  //   padding: 20,
  // }),
  // control: () => ({
  //   none of react-select's styles are passed to <Control />
  //   width: 200,
  // }),
  // singleValue: (provided, state) => {
  //   const opacity = state.isDisabled ? 0.5 : 1;
  //   const transition = "opacity 300ms";
  //   return { ...provided, opacity, transition };
  // },
};

export default BehaviorLeaf;
