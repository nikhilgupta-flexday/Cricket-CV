import { useState } from "react";
import "./ServerConfig.css";

const ServerConfig = ({ onSave }) => {
  const [url, setUrl] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!url.trim()) {
      setError("Please enter a server URL");
      return;
    }

    try {
      const urlObj = new URL(url);
      if (!urlObj.protocol.match(/^https?:$/)) {
        setError("URL must start with http:// or https://");
        return;
      }
    } catch {
      if (!url.startsWith("http://") && !url.startsWith("https://")) {
        setUrl("http://" + url);
        setError("Added http:// prefix. Click save again.");
        return;
      } else {
        setError("Invalid URL format");
        return;
      }
    }

    setError("");
    onSave(url.trim());
  };

  const useLocalNetwork = () => {
    setUrl("http://192.168.1.100:5000");
  };

  return (
    <div className="server-config">
      <div className="config-container">
        <h2>Server Configuration</h2>
        <p className="config-description">
          Enter the URL of your laptop server where videos will be sent for
          analysis.
        </p>

        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="serverUrl">Server URL</label>
            <input
              type="text"
              id="serverUrl"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="http://192.168.1.100:5000"
              className="url-input"
            />
            <small className="input-hint">
              Example: http://192.168.1.100:5000 or http://your-laptop-ip:5000
            </small>
          </div>

          {error && <div className="error-message">{error}</div>}

          <button type="submit" className="save-button">
            Save & Continue
          </button>

          <button
            type="button"
            className="quick-fill-button"
            onClick={useLocalNetwork}
          >
            Use Local Network Template
          </button>
        </form>

        <div className="help-section">
          <h3>How to find your server URL:</h3>
          <ol>
            <li>
              On your laptop, run: <code>ipconfig getifaddr en0</code> (Mac) or{" "}
              <code>ipconfig</code> (Windows)
            </li>
            <li>
              Look for your local IP address (usually starts with 192.168.x.x)
            </li>
            <li>Add the port your server is running on (e.g., :5000)</li>
            <li>
              Make sure your phone and laptop are on the same WiFi network
            </li>
          </ol>
        </div>
      </div>
    </div>
  );
};

export default ServerConfig;
