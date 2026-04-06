# Mission Control Dashboard

Streamlit dashboard for Yuki's Mission Control board.

## Deploy to Streamlit Cloud (Free + PIN Protected)

1. **Push to GitHub**
   ```bash
   cd dashboards/mission-control
   git init
   git add -A
   git commit -m "Mission Control Dashboard"
   git remote add origin https://github.com/YOUR_USERNAME/mission-control.git
   git push
   ```

2. **Deploy on Streamlit Cloud**
   - Go to: [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repo
   - Deploy

3. **Set the PIN**
   - In your Streamlit Cloud app settings → Secrets
   - Add: `PIN = "your-secret-pin"`

4. **Login**
   - Open the app URL
   - Enter your PIN to access

## Run Locally

```bash
cd dashboards/mission-control
export PIN="your-pin"
streamlit run app.py
```

Opens at: http://localhost:8501

## Features
- 🔐 PIN protection
- 🚀 4 Pillars status board
- 📊 Active pillar highlighted
- 🔴 Blockers flagged
- 👥 Agent crew status
- ✅ Recent wins
- 🔗 Quick links
