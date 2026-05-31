# 🚀 AGRITECH PRO - QUICK START GUIDE

## ⚡ 5-Minute Setup

### Prerequisites
- Python 3.8+ installed
- pip package manager
- Terminal/Command Prompt

---

## 📥 INSTALLATION STEPS

### 1️⃣ **Download Files**
Download all files from the package:
- `app.py` (Flask application)
- `templates/index.html` (Dashboard)
- `requirements.txt` (Dependencies)
- `README.md` (Full documentation)

### 2️⃣ **Create Project Folder**
```bash
# Create a folder for the project
mkdir agritech-pro
cd agritech-pro

# Place all downloaded files here
# Make sure templates folder structure is: agritech-pro/templates/index.html
```

### 3️⃣ **Install Python Dependencies**
```bash
# Option A: Direct installation
pip install -r requirements.txt

# Option B: With virtual environment (Recommended)
python -m venv venv

# Activate virtual environment:
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Then install:
pip install -r requirements.txt
```

### 4️⃣ **Verify Installation**
```bash
# Check all packages are installed
python -c "import flask, tensorflow, numpy, pandas; print('✅ All dependencies OK!')"
```

---

## 🎯 RUNNING THE APPLICATION

### Method 1: Direct Python (Development)
```bash
# Simply run the Flask app
python app.py

# Output will show:
# * Running on http://127.0.0.1:5000
# * Debug mode: on
```

### Method 2: Production with Gunicorn
```bash
# Install Gunicorn
pip install gunicorn

# Run with production settings
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

### Method 3: Docker (Containerized)
```bash
# Build Docker image
docker build -t agritech-pro .

# Run container
docker run -p 5000:5000 agritech-pro

# Or use Docker Compose
docker-compose up
```

---

## 📖 ACCESSING THE DASHBOARD

After starting the application:

1. **Open Web Browser**
   - Navigate to: `http://localhost:5000`
   - Or: `http://127.0.0.1:5000`

2. **Initial Loading**
   - System initializes (2-5 seconds)
   - Statistics cards populate automatically
   - Dashboard is ready to use

3. **Using the Dashboard**
   ```
   1. Click the dropdown menu
   2. Select visualization type:
      - Spectral Signatures by Crop Class
      - Crop Health Distribution
      - Soil Property Predictions
      - Pesticide Distribution Analysis
      - Real-time Monitoring Timeline
   
   3. Click "Generate Graph"
   4. View the generated visualization
   5. Check statistics on the left
   ```

---

## 📊 DASHBOARD FEATURES

### Real-Time Statistics
- 🌾 **Crop Health**: Current field health percentage
- 💧 **Soil Moisture**: Current moisture level
- 🧪 **Soil Nitrogen**: Current nitrogen concentration
- 🚜 **Pesticide Coverage**: Application coverage percentage

### Interactive Visualizations
- Line plots (spectral signatures, timelines)
- Bar charts (health distribution)
- Scatter plots (soil predictions)
- Heatmaps (pesticide distribution)
- Pie charts (coverage analysis)

### Auto-Refresh
- Statistics update every 30 seconds
- Manual refresh available
- Real-time alert system

---

## 🐛 TROUBLESHOOTING

### ❌ Port 5000 Already in Use
```bash
# Option 1: Kill process using port 5000
# Windows (PowerShell as Admin):
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process

# macOS/Linux:
lsof -i :5000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Option 2: Use different port
# Edit app.py and change: app.run(port=8000)
```

### ❌ Module Not Found Error
```bash
# Ensure virtual environment is activated
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Reinstall all packages
pip install --force-reinstall -r requirements.txt
```

### ❌ Dashboard Not Loading
```bash
# Clear browser cache
# Ctrl+Shift+Delete (Chrome/Firefox)
# Cmd+Shift+Delete (Safari)

# Open browser console
# F12 or Right-click > Inspect > Console

# Check Flask logs for errors
```

### ❌ Slow Performance
```bash
# Reduce memory usage:
# - Close other applications
# - Restart Flask: Ctrl+C then run again
# - Use production server (Gunicorn)
```

---

## 🔒 SECURITY NOTES

### For Production:
1. **HTTPS/SSL**
   - Use reverse proxy (nginx, Apache)
   - Install SSL certificate

2. **Environment Variables**
   - Store secrets in `.env` file
   - Use environment variables for configuration

3. **Rate Limiting**
   - Configure rate limits for API endpoints
   - Use API key authentication

4. **Firewall**
   - Restrict access to trusted IPs
   - Use VPN for remote access

---

## 📱 MOBILE ACCESS

**Access from another device on same network:**
```
1. Find your computer's IP address
   Windows: ipconfig (look for IPv4 Address)
   macOS/Linux: ifconfig (look for inet)

2. From mobile browser, navigate to:
   http://<YOUR_IP>:5000
   Example: http://192.168.1.100:5000

3. Mobile dashboard fully responsive!
```

---

## 🎓 API ENDPOINTS

**Get Dashboard:**
```
GET http://localhost:5000/
```

**Get Statistics:**
```
GET http://localhost:5000/api/get-stats
```

**Generate Graph:**
```
POST http://localhost:5000/api/get-graph
Content-Type: application/json

Body:
{
  "graph_type": "spectral_signatures"
}

Valid types:
- spectral_signatures
- crop_health_distribution
- soil_properties
- pesticide_distribution
- monitoring_timeline
```

---

## 📚 FILE STRUCTURE

```
agritech-pro/
│
├── 📄 app.py                    # MAIN APPLICATION FILE
├── 📄 requirements.txt          # Python packages
├── 📄 README.md                 # Full documentation
├── 📄 Dockerfile                # Docker configuration
├── 📄 docker-compose.yml        # Docker Compose config
│
└── 📁 templates/
    └── 📄 index.html            # Web dashboard (IMPORTANT)
```

**⚠️ IMPORTANT: Keep folder structure intact!**
```
app.py must be in same directory as templates/ folder
```

---

## 🔄 UPDATE & MAINTENANCE

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Check Versions
```bash
pip list
python --version
```

### Clear Cache
```bash
# Remove Python cache
find . -type d -name "__pycache__" -exec rm -r {} +

# Remove Flask cache
rm -rf instance/ .webassets-cache
```

---

## 📞 SUPPORT & HELP

### Common Issues:

**1. "ModuleNotFoundError: No module named 'flask'"**
   - Solution: `pip install -r requirements.txt`

**2. "Address already in use"**
   - Solution: Change port in app.py or use different port

**3. "Cannot connect to localhost:5000"**
   - Solution: Check if Flask is running, check firewall

**4. "Graphs not loading"**
   - Solution: Refresh page, clear cache, restart Flask

**5. "Very slow performance"**
   - Solution: Use Gunicorn, close other apps, increase RAM

---

## 🎯 NEXT STEPS

1. ✅ Run the application
2. ✅ Explore all visualizations
3. ✅ Review statistics and alerts
4. ✅ Read full README.md for advanced features
5. ✅ Deploy to production (optional)

---

## 📖 KEYBOARD SHORTCUTS

| Shortcut | Action |
|----------|--------|
| `Ctrl+G` or `Cmd+G` | Generate current graph |
| `Escape` | Clear alerts |
| `F12` | Open browser console |
| `Ctrl+Shift+Delete` | Clear browser cache |

---

## 🎉 YOU'RE ALL SET!

Your AgriTech Pro system is ready to monitor and analyze crops!

**Start exploring:** http://localhost:5000

For detailed information, see **README.md**

---

**Happy Farming! 🌾**
