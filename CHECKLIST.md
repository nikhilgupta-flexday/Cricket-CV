# Cricket CV - Setup Checklist

Use this checklist to ensure everything is set up correctly.

## 🖥️ Laptop Setup

### One-Time Setup

- [ ] Node.js installed (`node --version`)
- [ ] mkcert installed (`mkcert --version`)
- [ ] Ran `mkcert -install`
- [ ] Found laptop IP address (run `ipconfig getifaddr en0` on Mac)
- [ ] Generated SSL certificates with your IP: `mkcert localhost YOUR-IP 127.0.0.1 ::1`
- [ ] Verified `.pem` files exist in root folder
- [ ] Installed client dependencies: `npm install`
- [ ] Installed server dependencies: `cd server && npm install`

### Every Time You Run

- [ ] Both laptop and phone on same WiFi network
- [ ] Terminal 1: Server running (`cd server && node server.js`)
- [ ] Terminal 2: Client running (`npm run dev`)
- [ ] Note down the Network URLs shown in terminal

## 📱 Phone Setup

### First Time Only (or after certificate regeneration)

- [ ] Opened Safari/Chrome on phone
- [ ] Visited `https://YOUR-IP:5001`
- [ ] Accepted security warning ("Show Details" → "visit this website")
- [ ] Saw server health check message
- [ ] Visited `https://YOUR-IP:3000`
- [ ] Accepted security warning again
- [ ] App loaded successfully

### App Configuration

- [ ] Entered server URL: `https://YOUR-IP:5001` (with https://)
- [ ] Tapped "Save & Continue"
- [ ] Granted camera permission when asked
- [ ] Granted microphone permission when asked
- [ ] Tested connection (🔍 Test Connection button)
- [ ] Saw "✅ Server is reachable!"

### Testing

- [ ] Tapped "Start Recording"
- [ ] Saw red border and "REC" indicator
- [ ] Recorded for a few seconds
- [ ] Tapped "Stop Recording"
- [ ] Saw "✓ Upload successful!" message
- [ ] Verified video exists in `server/uploads/` folder on laptop

## 🐛 Common Issues

If something doesn't work:

**Camera not working?**
→ Grant permissions in browser settings

**"Upload Failed: Load failed"?**
→ You didn't accept the certificate. Go to Step 1 of Phone Setup

**"Cannot reach server"?**
→ Check both devices on same WiFi, server is running, IP is correct

**Certificate warning every time?**
→ Make sure you generated certificate with YOUR actual IP address

---

✅ **All checked? You're ready to record bowling videos!** 🏏🎥
