import React, { useState, useEffect } from "react";
import BehaviorGroupTree from "../components/BehaviorGroupTree";

var key = 0;
var emptyBot = {
  name: "",
  buy_behaviors: { key: key++, group: [], group_condition: "or" },
  sell_behaviors: { key: key++, group: [], group_condition: "or" },
};

const BotEditor = (props) => {
  const [bot, setBot] = useState(emptyBot);
  const [botName, setBotName] = useState(emptyBot.name);
  const [buyBehaviors, setBuyBehaviors] = useState(emptyBot.buy_behaviors);
  const [sellBehaviors, setSellBehaviors] = useState(emptyBot.sell_behaviors);

  useEffect(() => {
    setBot(JSON.parse(JSON.stringify(props.source || emptyBot)));
    setBotName(props.source.name || emptyBot.name);
    setBuyBehaviors(props.source.buy_behaviors || emptyBot.buy_behaviors);
    setSellBehaviors(props.source.sell_behaviors || emptyBot.sell_behaviors);
  }, [props.source]);

  function handleBotNameChanged(e) {
    setBotName(e.target.value);
  }

  function onSaveButtonClicked(e) {
    let temp = JSON.parse(JSON.stringify(bot));
    temp.name = botName;
    temp.buy_behaviors = correctBehaviorGroup(buyBehaviors);
    temp.sell_behaviors = correctBehaviorGroup(sellBehaviors);
    setBot(temp);
    props.onSave(temp);
  }

  function correctBehaviorGroup(jsonObject) {
    // Removes any object that does not have the necessary properties to interface with the API
    if (
      jsonObject !== undefined &&
      jsonObject !== null &&
      JSON.stringify(jsonObject) !== "{}" &&
      typeof jsonObject === "object"
    ) {
      if (
        "function" in jsonObject &&
        "inputs" in jsonObject &&
        "target" in jsonObject &&
        "condition" in jsonObject
      ) {
        return jsonObject;
      } else if ("group" in jsonObject && "group_condition" in jsonObject) {
        var validatedGroup = [];
        jsonObject.group.forEach((element) => {
          let validatedElement = correctBehaviorGroup(element);
          if (validatedElement !== undefined) {
            validatedGroup = [...validatedGroup, validatedElement];
          }
        });
        jsonObject.group = validatedGroup;
        return jsonObject;
      }
    }
  }

  return (
    <div className="grid">
      <div>
        <input
          style={{ gridRow: 1, gridColumn: 1 }}
          type="text"
          id="txtBotName"
          placeholder="Name"
          value={botName || ""}
          onChange={handleBotNameChanged}
        />
      </div>
      <div style={{ gridRow: 2, gridColumn: 1 }}>
        {
          <BehaviorGroupTree
            keyProp={key++}
            onBehaviorTested={props.onBehaviorTested}
            source={buyBehaviors}
          />
        }
      </div>
      <div style={{ gridRow: 3, gridColumn: 1 }}>
        {
          <BehaviorGroupTree
            keyProp={key++}
            source={sellBehaviors}
            onBehaviorTested={props.onBehaviorTested}
          />
        }
      </div>
      <button className="save-btn" onClick={onSaveButtonClicked}>
        Save
      </button>
    </div>
  );
};

export default BotEditor;
