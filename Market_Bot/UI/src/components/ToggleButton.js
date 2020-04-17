import React, { useState, setState, useEffect } from "react";
import ToggleButton from "@material-ui/lab/ToggleButton";

const ToggleButtona = (props) => {
  const [buttonList, setButtonList] = useState([]);

  return (
    <div>
      <ToggleButton></ToggleButton>
      <ToggleButton></ToggleButton>
    </div>
  );
};

export default ToggleButtona;
