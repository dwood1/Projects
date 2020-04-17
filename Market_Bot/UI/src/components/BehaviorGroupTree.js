import React, { useState, useEffect } from "react";
import ToggleButtonGroup from "@material-ui/lab/ToggleButtonGroup";
import ToggleButton from "@material-ui/lab/ToggleButton";
import BehaviorLeaf from "../components/BehaviorLeaf";

const toggleTypes = [
  <ToggleButton key={1} value="or">
    OR
  </ToggleButton>,
  <ToggleButton key={2} value="and">
    AND
  </ToggleButton>,
];

var key = 0;

const BehaviorGroupTree = (props) => {
  const [source, setSource] = useState({});
  const [condition, setCondition] = useState();
  const [group, setGroup] = useState();

  useEffect(() => {
    setSource(props.source);
    setCondition(props.source.group_condition);
    setGroup(props.source.group);
    key = props.keyProp;
  }, [props.source, props.keyProp]);

  function handleChange(event, value) {
    let newCondition = value || "or";
    setCondition(newCondition);
    let temp = source;
    temp.group_condition = newCondition;
    setSource(temp);
  }

  function renderBehaviorGroupTree(jsonObject) {
    if (
      jsonObject !== null &&
      jsonObject !== undefined &&
      JSON.stringify(jsonObject) !== "{}" &&
      typeof jsonObject === "object"
    ) {
      var leaves = [];
      jsonObject.forEach((element) => {
        if ("group" in element && "group_condition" in element) {
          // fits the requirements to be a behavior group object
          element["key"] = key++;
          leaves.push(
            <BehaviorGroupTree
              keyProp={key++}
              onBehaviorTested={props.onBehaviorTested}
              source={element}
              delete={() => deleteBehavior(element.key)}
            />
          );
        } else if (
          "function" in element &&
          "inputs" in element &&
          "target" in element &&
          "condition" in element
        ) {
          // fits the requirements to be a behavior leaf object
          element["key"] = key++;
          leaves.push(
            <BehaviorLeaf
              keyProp={key++}
              source={element}
              delete={() => deleteBehavior(element.key)}
              onBehaviorTested={props.onBehaviorTested}
            />
          );
        }
      });
      return leaves;
    }
  }

  function deleteBehavior(key) {
    // attempts to remove the element associated with the key from the group object
    var tempGroup = [...group];
    if (removeFromGroup(key, tempGroup) === "removed") {
      setGroup(tempGroup);
      let tempSource = source;
      tempSource.group = tempGroup;
      setSource(tempSource);
    }
  }

  function removeFromGroup(key, behavior) {
    if (behavior !== undefined) {
      if ("key" in behavior) {
        if (key === behavior.key) {
          return true;
        }
        return false;
      } else {
        for (var i = 0; i < behavior.length; i++) {
          let result = removeFromGroup(key, behavior[i]);
          if (result === true) {
            behavior[i] = {};
            return "removed";
          } else if (result === "removed") {
            return "removed";
          }
        }
      }
    }
    return "undefined";
  }

  function executeOnAddBehaviorClicked(e) {
    // renders an additional behavior leaf and adds an empty behavior ("{}") to the
    let element = {
      key: key++,
      function: "",
      inputs: {},
      condition: "",
      target: "",
    };
    let tempGroup = [...group, element];
    setGroup(tempGroup);
    let tempSource = source;
    tempSource.group = tempGroup;
    setSource(tempSource);
  }

  function executeOnAddGroupClicked(e) {
    // renders an additional behaviorgrouptree and adds an empty behavior group to the group
    let element = { key: key++, group: [], group_condition: "or" };
    let tempGroup = [...group, element];
    setGroup(tempGroup);
    let tempSource = source;
    tempSource.group = tempGroup;
    setSource(tempSource);
  }

  return (
    <div className="tree">
      <ToggleButtonGroup
        size="small"
        value={condition}
        exclusive
        onChange={handleChange}>
        {toggleTypes}
      </ToggleButtonGroup>
      <div>{renderBehaviorGroupTree(group)}</div>
      <div className="flex-row flex-end">
        <button className="btn" onClick={executeOnAddBehaviorClicked}>
          +Add Behavior
        </button>
        <button className="btn" onClick={executeOnAddGroupClicked}>
          +Add Group
        </button>
        {props.delete && (
          <button className="delete-btn" onClick={props.delete}>
            -Remove Group
          </button>
        )}
      </div>
    </div>
  );
};

export default BehaviorGroupTree;
