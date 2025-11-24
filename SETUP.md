# Cricket CV - Complete Setup Guide

A complete guide to set up the Cricket Bowling Analysis application on your laptop and phone.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Initial Setup](#initial-setup)
- [SSL Certificate Setup (HTTPS)](#ssl-certificate-setup-https)
- [Running the Application](#running-the-application)
- [Phone Setup](#phone-setup)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, make sure you have:

- **Node.js** (v16 or higher) - [Download here](https://nodejs.org/)
- **npm** (comes with Node.js)
- **Homebrew** (Mac only) - [Install here](https://brew.sh/)
- A **phone** and **laptop** on the **same WiFi network**

---

## Initial Setup

### 1. Clone/Download the Project

```bash
cd /path/to/Cricket-CV
```

### 2. Install Dependencies

**Client dependencies:**

```bash
npm install
```

**Server dependencies:**

```bash
cd server
npm install
cd ..
```

---

## SSL Certificate Setup (HTTPS)

Modern browsers require **HTTPS** to access the camera. We'll create local SSL certificates using `mkcert`.

### Step 1: Install mkcert

**On Mac:**

```bash
brew install mkcert
```

**On Windows:**
Download from [mkcert releases](https://github.com/FiloSottile/mkcert/releases)

**On Linux:**

```bash
# Ubuntu/Debian
sudo apt install libnss3-tools
wget https://github.com/FiloSottile/mkcert/releases/download/v1.4.4/mkcert-v1.4.4-linux-amd64
chmod +x mkcert-v1.4.4-linux-amd64
sudo mv mkcert-v1.4.4-linux-amd64 /usr/local/bin/mkcert
```

### Step 2: Install Local Certificate Authority

```bash
mkcert -install
```

You'll be prompted for your password. This installs a local Certificate Authority on your laptop.

### Step 3: Find Your Laptop's IP Address

**On Mac:**

```bash
ipconfig getifaddr en0
```

**On Windows:**

```bash
ipconfig
```

Look for "IPv4 Address" (usually starts with `192.168.x.x`)

**On Linux:**

```bash
hostname -I | awk '{print $1}'
```

Example output: `192.168.68.62`

### Step 4: Generate SSL Certificates

Replace `192.168.68.62` with YOUR laptop's IP address:

```bash
cd /path/to/Cricket-CV
mkcert localhost 192.168.68.62 127.0.0.1 ::1
```

This creates two files:

- `localhost+3.pem` (certificate)
- `localhost+3-key.pem` (private key)

**Important:** These files must be in the root of the `Cricket-CV` folder.

### Step 5: Verify Certificate Files

```bash
ls -la *.pem
```

You should see:

```
localhost+3-key.pem
localhost+3.pem
```

✅ **SSL setup complete!**

---

## Running the Application

You need to run **both** the client and server.

### Terminal 1: Start the Server

```bash
cd server
node server.js
```

You should see:

```
🏏 Cricket CV Server Started!
================================
📡 Local:   https://localhost:5001
📡 Network: https://192.168.68.62:5001
================================
📁 Videos will be saved to: /Users/you/Cricket-CV/server/uploads

✅ Server is ready to receive videos!
```

**Keep this terminal running.**

### Terminal 2: Start the Client

Open a new terminal:

```bash
npm run dev
```

You should see:

```
  VITE v5.4.21  ready in 115 ms

  ➜  Local:   https://localhost:3000/
  ➜  Network: https://192.168.68.62:3000/
```

**Keep this terminal running too.**

✅ **Both services are now running!**

---

## Phone Setup

### Step 1: Trust the Server Certificate

**This is CRITICAL - the app won't work without this step!**

1. **On your phone, open Safari** (iOS) or **Chrome** (Android)
2. **Go to:** `https://192.168.68.62:5001` (use YOUR laptop's IP)
3. You'll see a security warning: **"This Connection Is Not Private"**
4. **On iPhone:**
   - Tap **"Show Details"**
   - Tap **"visit this website"**
   - Tap **"Visit Website"** again
5. **On Android:**
   - Tap **"Advanced"**
   - Tap **"Proceed to 192.168.68.62 (unsafe)"**
6. You should see: `{"status":"ok","message":"Cricket CV Server is running"...}`

✅ **Certificate trusted!**

### Step 2: Open the App

1. **In the same browser**, go to: `https://192.168.68.62:3000` (use YOUR laptop's IP)
2. Accept the security warning again (same steps as above)
3. The Cricket CV app should load! 🎉

### Step 3: Configure the Server URL

1. You'll see a **Server Configuration** screen
2. Enter: `https://192.168.68.62:5001` (use YOUR laptop's IP, include `https://`)
3. Tap **"Save & Continue"**

### Step 4: Grant Camera Permissions

1. Browser will ask for **Camera** and **Microphone** permissions
2. Tap **"Allow"** for both

### Step 5: Test Connection (Recommended)

1. Tap the **"🔍 Test Connection"** button at the bottom
2. You should see: **"✅ Server is reachable!"**
3. If not, go back to Step 1 and ensure you visited the server URL

### Step 6: Start Recording! 🎥

1. Point camera at the bowling action
2. Tap **"Start Recording"** - you'll see a red border and "REC" indicator
3. Record the bowling
4. Tap **"Stop Recording"**
5. Video uploads automatically!
6. Check your laptop's `server/uploads/` folder for the saved video

---

## Troubleshooting

### ❌ "Could not access camera"

- **Solution:** Grant camera permissions in browser settings
- iPhone: Settings → Safari → Camera → Allow
- Android: Chrome → Site Settings → Camera → Allow

### ❌ "Upload Failed: Load failed"

- **Solution:** You didn't trust the server certificate
- Go back to [Phone Setup Step 1](#step-1-trust-the-server-certificate)
- Visit `https://YOUR-IP:5001` in Safari/Chrome and accept the warning

### ❌ "This Connection Is Not Private" keeps appearing

- **Solution:** Make sure you generated certificates with YOUR actual IP address
- Re-run: `mkcert localhost YOUR-IP 127.0.0.1 ::1`
- Restart both client and server

### ❌ "Cannot reach server"

- Check both devices are on the **same WiFi network**
- Check server is running (Terminal 1 should show "Server is ready")
- Verify IP address hasn't changed: `ipconfig getifaddr en0` (Mac)
- Try the "🔍 Test Connection" button in the app

### ❌ Port already in use

```bash
# Find process on port 3000 or 5001
lsof -ti:3000
lsof -ti:5001

# Kill it
kill -9 <process-id>
```

### ❌ Videos not uploading

- Check `server/uploads/` folder exists
- Check server terminal for error messages
- Verify server URL in app includes `https://` not `http://`

### ❌ IP Address Changed

If your laptop's IP changes (common with WiFi):

1. Find new IP: `ipconfig getifaddr en0`
2. Generate new certificates: `mkcert localhost NEW-IP 127.0.0.1 ::1`
3. Restart client and server
4. Update server URL in phone app

---

## Quick Reference

### URLs (replace with your IP)

- **Client:** `https://192.168.68.62:3000`
- **Server:** `https://192.168.68.62:5001`

### Commands

```bash
# Find IP (Mac)
ipconfig getifaddr en0

# Generate certificates
mkcert localhost YOUR-IP 127.0.0.1 ::1

# Start server
cd server && node server.js

# Start client (new terminal)
npm run dev

# Check if port is in use
lsof -ti:3000
lsof -ti:5001
```

### File Locations

- **Videos saved to:** `server/uploads/`
- **SSL certificates:** `localhost+3.pem` and `localhost+3-key.pem` (in root folder)

---

## Architecture Overview

```
Phone (Safari/Chrome)                    Laptop
┌─────────────────────┐                 ┌──────────────────────┐
│                     │    HTTPS        │                      │
│  Cricket CV Client  │◄───────────────►│   Vite Dev Server    │
│  (Port 3000)        │   Video Upload  │   (Port 3000)        │
│                     │─────────────────┤                      │
└─────────────────────┘                 │   Node.js Server     │
                                        │   (Port 5001)        │
                                        │                      │
                                        │   ML Model           │
                                        │   (Future)           │
                                        └──────────────────────┘
```

---

## Next Steps

- ✅ Test the full recording → upload flow
- 🔜 Integrate ML model for bowling line detection
- 🔜 Display analysis results back to client
- 🔜 Add video playback with frame-by-frame analysis

---

## Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Look at terminal output for error messages
3. Use the "🔍 Test Connection" button in the app
4. Check browser console for detailed errors

**Happy Recording! 🏏🎥**
