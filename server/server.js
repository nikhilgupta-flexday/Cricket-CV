import express from "express";
import multer from "multer";
import cors from "cors";
import path from "path";
import { fileURLToPath } from "url";
import fs from "fs";
import https from "https";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = 5001;

const sslOptions = {
  key: fs.readFileSync(path.join(__dirname, "../localhost+3-key.pem")),
  cert: fs.readFileSync(path.join(__dirname, "../localhost+3.pem")),
};

app.use(cors());
app.use(express.json());

const uploadsDir = path.join(__dirname, "uploads");
if (!fs.existsSync(uploadsDir)) {
  fs.mkdirSync(uploadsDir, { recursive: true });
}

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, uploadsDir);
  },
  filename: (req, file, cb) => {
    const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
    const extension = path.extname(file.originalname) || ".webm";
    cb(null, `bowling-${timestamp}${extension}`);
  },
});

const upload = multer({
  storage,
  limits: {
    fileSize: 100 * 1024 * 1024, // 100MB limit
  },
});
app.get("/", (req, res) => {
  res.send("🏏 Cricket CV Server is running");
});

app.get("/api/health", (req, res) => {
  res.json({
    status: "ok",
    message: "Cricket CV Server is running",
    timestamp: new Date().toISOString(),
  });
});

app.post("/api/upload", upload.single("video"), (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({
        error: "No video file uploaded",
      });
    }

    const videoInfo = {
      filename: req.file.filename,
      originalName: req.file.originalname,
      size: req.file.size,
      path: req.file.path,
      timestamp: req.body.timestamp || new Date().toISOString(),
      uploadedAt: new Date().toISOString(),
    };

    console.log("📹 Video received:", videoInfo);
    console.log(`   Size: ${(req.file.size / 1024 / 1024).toFixed(2)} MB`);
    console.log(`   Saved to: ${req.file.path}`);


    res.json({
      success: true,
      message: "Video uploaded successfully",
      video: {
        filename: videoInfo.filename,
        size: videoInfo.size,
        timestamp: videoInfo.timestamp,
      },
    });
  } catch (error) {
    console.error("Upload error:", error);
    res.status(500).json({
      error: "Failed to process upload",
      message: error.message,
    });
  }
});

app.get("/api/videos", (req, res) => {
  try {
    const files = fs.readdirSync(uploadsDir);
    const videos = files
      .filter((file) => file.endsWith(".webm") || file.endsWith(".mp4"))
      .map((file) => {
        const filePath = path.join(uploadsDir, file);
        const stats = fs.statSync(filePath);
        return {
          filename: file,
          size: stats.size,
          created: stats.birthtime,
          modified: stats.mtime,
        };
      })
      .sort((a, b) => b.created - a.created);

    res.json({
      count: videos.length,
      videos,
    });
  } catch (error) {
    console.error("Error listing videos:", error);
    res.status(500).json({
      error: "Failed to list videos",
      message: error.message,
    });
  }
});

app.use("/uploads", express.static(uploadsDir));

https.createServer(sslOptions, app).listen(PORT, "0.0.0.0", () => {
  console.log("🏏 Cricket CV Server Started!");
  console.log("================================");
  console.log(`📡 Local:   https://localhost:${PORT}`);
  console.log(`📡 Network: https://192.168.68.62:${PORT}`);
  console.log("================================");
  console.log(`📁 Videos will be saved to: ${uploadsDir}`);
  console.log("\n✅ Server is ready to receive videos!\n");
});
