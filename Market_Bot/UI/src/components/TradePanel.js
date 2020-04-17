import React, { useState, useEffect } from "react";

const TradePanel = (props) => {
  const [bot, setBot] = useState();
  const [token, setToken] = useState("BTC");
  const [asset, setAsset] = useState("USDT");

  useEffect(() => {
    setBot(props.source);
  }, [props.source]);

  function handleTestButtonClicked(e) {
    // POST
    // /api/run_bot/
    console.log("Testing...");
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: bot.name,
        cycles: 5,
        token: token,
        asset: asset,
        test: { status: true },
      }),
    };
    fetch(`${props.apiSignature}/api/run_bot/`, requestOptions)
      .then((res) => res.json())
      .then(
        (result) => {
          props.onDataSubmit(result);
        },
        (error) => {
          console.log("Error");
        }
      );
  }

  function handleRunButtonClicked(e) {
    // POST
    // /api/run_bot/
    console.log("Running...");
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: bot.name,
        cycles: 5,
        token: token,
        asset: asset,
        test: { status: false },
      }),
    };
    fetch(`${props.apiSignature}/api/run_bot/`, requestOptions)
      .then((res) => res.json())
      .then(
        (result) => {
          console.log(result);
        },
        (error) => {
          console.log("Error");
        }
      );
  }

  function onTokenEntryChanged(e) {
    setToken(e.target.value);
  }

  function onAssetEntryChanged(e) {
    setAsset(e.target.value);
  }

  return (
    <>
      <div className="flex-row">
        <div className="label-container">
          <label>Token </label>
          <input
            type="text"
            placeholder="Token"
            onChange={onTokenEntryChanged}
            value={token}
          />
        </div>
        <div className="label-container">
          <label>Asset </label>
          <input
            type="text"
            placeholder="Asset"
            onChange={onAssetEntryChanged}
            value={asset}
          />
        </div>
      </div>

      <div>
        <button className="test-btn" onClick={handleTestButtonClicked}>
          Test
        </button>
        {/* <button className="save-btn" onClick={handleRunButtonClicked}>
          Run
        </button> */}
      </div>
    </>
  );
};

export default TradePanel;
