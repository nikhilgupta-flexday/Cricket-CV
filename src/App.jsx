import { useState } from "react";
import CameraRecorder from "./components/CameraRecorder";
import ServerConfig from "./components/ServerConfig";
import "./App.css";

function App() {
  const [serverUrl, setServerUrl] = useState(() => {
    return localStorage.getItem("serverUrl") || "";
  });
  const [isConfigured, setIsConfigured] = useState(() => {
    return !!localStorage.getItem("serverUrl");
  });

  const handleSaveConfig = (url) => {
    localStorage.setItem("serverUrl", url);
    setServerUrl(url);
    setIsConfigured(true);
  };

  const handleReconfigure = () => {
    setIsConfigured(false);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🏏 Cricket CV</h1>
        <p>Bowling Line Detection</p>
      </header>

      {!isConfigured ? (
        <ServerConfig onSave={handleSaveConfig} />
      ) : (
        <CameraRecorder
          serverUrl={serverUrl}
          onReconfigure={handleReconfigure}
        />
      )}
    </div>
  );
}

export default App;
