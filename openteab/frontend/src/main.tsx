import React from "react";
import ReactDOM from "react-dom/client";
import "./fonts.css";
import App from "./App";
import { ConfigProvider } from "./contexts/ConfigContext";

document.addEventListener("contextmenu", (event) => {
  event.preventDefault();
});

const root = document.getElementById("root");

ReactDOM.createRoot(root as HTMLElement).render(
  <React.StrictMode>
    <ConfigProvider>
      <App />
    </ConfigProvider>
  </React.StrictMode>
);