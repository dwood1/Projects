import ReactDOM from "react-dom";
import React from "react";
import { BrowserRouter } from "react-router-dom";
import "./css/index.css";
import "./css/main.css";
import "../node_modules/chartist/dist/chartist.min.css";
import App from "./pages/App";
import * as serviceWorker from "./serviceWorker";

ReactDOM.render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>,
  document.getElementById("root")
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
