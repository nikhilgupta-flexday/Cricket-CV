# Cricket CV - Server

Backend server for receiving and storing cricket bowling videos from the mobile client.

## 🚀 Running the Server

```bash
cd server
node server.js
```

The server will start on:

- **Local:** `http://localhost:5001`
- **Network:** `http://192.168.68.62:5001`

## 📡 API Endpoints

### Health Check

```
GET /api/health
```

Returns server status

### Upload Video

```
POST /api/upload
Content-Type: multipart/form-data
Body: video (file), timestamp (string)
```

Receives and saves video files

### List Videos

```
GET /api/videos
```

Returns list of all uploaded videos

### Access Videos

```
GET /uploads/{filename}
```

Serves uploaded video files

## 📁 File Storage

Videos are saved to: `server/uploads/`

Format: `bowling-{timestamp}.webm`

## 🔜 Next Steps

- Add ML model integration for line detection
- Implement video analysis pipeline
- Return analysis results to client
- Add real-time processing status updates
