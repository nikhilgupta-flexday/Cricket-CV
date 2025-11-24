# Cricket CV - Client Application

A web-based client application for recording cricket bowling videos on your phone and sending them to a laptop server for ML analysis to detect bowling line violations (no-balls).

## 🎯 Features

- 📹 Live camera recording with front/back camera toggle
- 📱 Mobile-optimized responsive design
- 🚀 Direct video upload to server
- ⚙️ Easy server configuration
- 🎨 Modern, intuitive UI with recording indicators
- 🔄 Real-time upload status
- 🔍 Built-in connection testing

## 🚀 Quick Start

**👉 For complete setup instructions (especially for teammates), see [SETUP.md](./SETUP.md)**  
**📋 Quick setup checklist: [CHECKLIST.md](./CHECKLIST.md)**

### TL;DR

1. **Install mkcert:** `brew install mkcert` and run `mkcert -install`
2. **Find your IP:** `ipconfig getifaddr en0` - example: `192.168.68.62`
3. **Generate certificates:** `mkcert localhost YOUR-IP 127.0.0.1 ::1`
4. **Install dependencies:** `npm install` and `cd server && npm install`
5. **Start server:** `cd server && node server.js`
6. **Start client:** `npm run dev` (in new terminal)
7. **On phone:**
   - Visit `https://YOUR-IP:5001` in Safari/Chrome and **accept the security warning**
   - Then visit `https://YOUR-IP:3000` and **accept the security warning**
   - Configure server URL: `https://YOUR-IP:5001`
   - Grant camera permissions and start recording! 🎥

### Server Configuration

When you first open the app, you'll need to configure the server URL:

1. Enter your laptop server URL: `http://192.168.68.62:5001` (use your actual IP)
2. Make sure your phone and laptop are on the **same WiFi network**
3. The server should be running (see Server Setup below)

## 📱 Usage

1. **Grant Camera Permissions:**

   - When prompted, allow the browser to access your camera and microphone

2. **Start Recording:**

   - Point your phone at the bowling action
   - Tap "Start Recording" to begin
   - The screen will show a red border and "REC" indicator

3. **Stop Recording:**

   - Tap "Stop Recording" when done
   - The video will automatically upload to your server

4. **Camera Controls:**
   - Use "Flip Camera" to switch between front and back cameras
   - Use "Change Server" to update the server URL

## 🏗️ Project Structure

```
Cricket-CV/
├── src/
│   ├── components/
│   │   ├── CameraRecorder.jsx       # Main camera recording component
│   │   ├── CameraRecorder.css
│   │   ├── ServerConfig.jsx         # Server configuration screen
│   │   └── ServerConfig.css
│   ├── services/
│   │   └── videoUpload.js           # Video upload service
│   ├── App.jsx                      # Main app component
│   ├── App.css
│   ├── main.jsx                     # Entry point
│   └── index.css                    # Global styles
├── index.html
├── vite.config.js
├── package.json
└── README.md
```

## 🔧 Configuration

### Server Endpoint

The app expects the following server endpoint:

- **POST** `/api/upload` - Upload video files
  - Content-Type: `multipart/form-data`
  - Body: `video` (file), `timestamp` (string)

Optional health check endpoint:

- **GET** `/api/health` - Check server status

## 📋 Browser Compatibility

The app uses modern web APIs and works best with:

- ✅ Chrome/Edge (Android & Desktop)
- ✅ Safari (iOS & macOS)
- ⚠️ Firefox (may have limited MediaRecorder support)

**Note:** HTTPS is required for camera access on most browsers (except localhost).

## 🐛 Troubleshooting

### Camera not working

- Ensure you've granted camera permissions
- Try refreshing the page
- Check if another app is using the camera

### Cannot connect to server

- Verify both devices are on the same WiFi network
- Check the server URL is correct
- Ensure the server is running
- Try pinging the server IP from your phone's browser

### Upload fails

- Check your internet connection
- Verify the server is accepting uploads
- Check server logs for errors
- Ensure the server endpoint matches `/api/upload`

## 🔜 Future Enhancements

- Real-time video streaming (WebRTC)
- Live analysis feedback
- Video playback with analysis overlay
- Multiple camera angle support
- Offline mode with queue

## 📄 License

MIT

## 🤝 Contributing

This is part of the Cricket CV project for detecting bowling line violations using ML.

---

**Made with ❤️ for cricket enthusiasts**
