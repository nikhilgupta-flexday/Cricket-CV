import { useState, useRef, useEffect } from "react";
import { uploadVideo, checkServerConnection } from "../services/videoUpload";
import "./CameraRecorder.css";

const CameraRecorder = ({ serverUrl, onReconfigure }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState("");
  const [error, setError] = useState("");
  const [cameraReady, setCameraReady] = useState(false);
  const [facingMode, setFacingMode] = useState("environment"); // 'user' for front, 'environment' for back
  const [serverStatus, setServerStatus] = useState("unknown");

  const videoRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const streamRef = useRef(null);

  useEffect(() => {
    startCamera();
    return () => {
      stopCamera();
    };
  }, [facingMode]);

  const startCamera = async () => {
    try {
      setError("");
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: facingMode,
          width: { ideal: 1920 },
          height: { ideal: 1080 },
        },
        audio: true,
      });

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        streamRef.current = stream;
        setCameraReady(true);
      }
    } catch (err) {
      console.error("Error accessing camera:", err);
      setError("Could not access camera. Please grant camera permissions.");
    }
  };

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
    }
  };

  const startRecording = () => {
    if (!streamRef.current) {
      setError("Camera stream not available");
      return;
    }

    try {
      chunksRef.current = [];

      // Try different mimeTypes for better compatibility
      let options = { mimeType: "video/webm;codecs=vp8,opus" };

      if (!MediaRecorder.isTypeSupported(options.mimeType)) {
        options = { mimeType: "video/webm" };
      }

      if (!MediaRecorder.isTypeSupported(options.mimeType)) {
        options = { mimeType: "video/mp4" };
      }

      if (!MediaRecorder.isTypeSupported(options.mimeType)) {
        options = {}; // Use default
      }

      console.log("Recording with mimeType:", options.mimeType || "default");

      mediaRecorderRef.current = new MediaRecorder(streamRef.current, options);

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          console.log("Data chunk received:", event.data.size, "bytes");
          chunksRef.current.push(event.data);
        }
      };

      mediaRecorderRef.current.onstop = handleRecordingStop;

      mediaRecorderRef.current.onerror = (event) => {
        console.error("MediaRecorder error:", event);
        setError("Recording error occurred");
        setIsRecording(false);
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
      setUploadStatus("");
      setError("");
      console.log("Recording started");
    } catch (err) {
      console.error("Error starting recording:", err);
      setError("Could not start recording: " + err.message);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const handleRecordingStop = async () => {
    try {
      setUploadStatus(
        `📹 Recording stopped. Video size: ${chunksRef.current.length} chunks`
      );

      const blob = new Blob(chunksRef.current, { type: "video/webm" });
      setUploadStatus(
        `📦 Video blob created: ${(blob.size / 1024 / 1024).toFixed(2)} MB`
      );

      // Create a timestamp for the filename
      const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
      const filename = `bowling-${timestamp}.webm`;

      setIsUploading(true);
      setUploadStatus(`📤 Uploading to: ${serverUrl}`);

      try {
        const result = await uploadVideo(blob, filename, serverUrl);
        setUploadStatus(`✓ Upload successful! ${result.message || ""}`);
        setError("");
        setTimeout(() => setUploadStatus(""), 5000);
      } catch (err) {
        console.error("Upload error:", err);
        const errorDetails = `
❌ Upload Failed:
• Error: ${err.message}
• Server: ${serverUrl}
• Video size: ${(blob.size / 1024 / 1024).toFixed(2)} MB
• Time: ${new Date().toLocaleTimeString()}

Check if:
1. Server is running
2. Server URL is correct
3. Both devices on same WiFi
        `.trim();
        setError(errorDetails);
        setUploadStatus("");
      } finally {
        setIsUploading(false);
      }
    } catch (err) {
      setError(`Failed to process recording: ${err.message}`);
      setIsUploading(false);
    }
  };

  const toggleCamera = () => {
    setFacingMode((prev) => (prev === "user" ? "environment" : "user"));
  };

  const testServerConnection = async () => {
    setServerStatus("testing");
    setError("");
    setUploadStatus("🔍 Testing server connection...");

    try {
      const isConnected = await checkServerConnection(serverUrl);
      if (isConnected) {
        setServerStatus("connected");
        setUploadStatus("✅ Server is reachable!");
        setTimeout(() => setUploadStatus(""), 3000);
      } else {
        setServerStatus("error");
        setError(
          `Cannot connect to server at ${serverUrl}\n\n🔐 If using HTTPS:\n1. Open ${serverUrl} in Safari\n2. Accept the certificate warning\n3. Come back and try again`
        );
      }
    } catch (err) {
      setServerStatus("error");
      setError(
        `Connection test failed: ${err.message}\n\n🔐 Try opening ${serverUrl} in Safari first to accept the certificate`
      );
    }
  };

  return (
    <div className="camera-recorder">
      <div className="video-container">
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className={`video-preview ${isRecording ? "recording" : ""}`}
        />
        {isRecording && <div className="recording-indicator">● REC</div>}
      </div>

      <div className="controls">
        {error && <div className="error-message">{error}</div>}
        {uploadStatus && <div className="status-message">{uploadStatus}</div>}

        <div className="button-group">
          <button
            className={`record-button ${isRecording ? "stop" : "start"}`}
            onClick={isRecording ? stopRecording : startRecording}
            disabled={!cameraReady || isUploading}
          >
            {isRecording ? "⬛ Stop Recording" : "⚫ Start Recording"}
          </button>

          <button
            className="flip-button"
            onClick={toggleCamera}
            disabled={isRecording || isUploading}
          >
            🔄 Flip Camera
          </button>
        </div>

        <div className="server-info">
          <p>Server: {serverUrl}</p>
          <div className="server-buttons">
            <button
              className="test-button"
              onClick={testServerConnection}
              disabled={
                isRecording || isUploading || serverStatus === "testing"
              }
            >
              {serverStatus === "testing"
                ? "⏳ Testing..."
                : "🔍 Test Connection"}
            </button>
            <button
              className="config-button"
              onClick={onReconfigure}
              disabled={isRecording || isUploading}
            >
              ⚙️ Change Server
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CameraRecorder;
