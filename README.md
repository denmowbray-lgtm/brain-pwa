# DENMOW Brain PWA

Progressive Web App wrapper for the DENMOW Brain Notion intake hub.

## Files
- `index.html` — PWA shell with splash screen + iframe loader
- `manifest.json` — App name, icon, display mode
- `sw.js` — Service worker (caching + offline detection)
- `icon-192.png` / `icon-512.png` — App icons

## Deploy to GitHub Pages

### First time setup (5 minutes)

1. Go to https://github.com/new
2. Create a repo named: `brain-pwa` (keep it Public)
3. Don't initialize with README

### Push these files

```bash
cd brain-pwa
git init
git add .
git commit -m "Initial Brain PWA"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/brain-pwa.git
git push -u origin main
```

### Enable GitHub Pages

1. Go to your repo on GitHub
2. Settings → Pages
3. Source: **Deploy from a branch**
4. Branch: **main** / **/ (root)**
5. Save

Your app will be live at:
`https://YOUR-USERNAME.github.io/brain-pwa/`

(Takes ~2 minutes the first time)

## Install as App

### iPhone / iPad (Safari)
1. Open the GitHub Pages URL in **Safari**
2. Tap the **Share** button
3. Tap **Add to Home Screen**
4. Name it **Brain** → Add

### Android (Chrome)
1. Open the URL in Chrome
2. Tap the **3-dot menu**
3. Tap **Add to Home Screen** or **Install App**

### Desktop (Chrome / Edge)
1. Open the URL
2. Click the **install icon** in the address bar (right side)
3. Click **Install**

## Update the app

Edit files locally → `git add . && git commit -m "update" && git push`  
GitHub Pages auto-deploys in ~60 seconds.

## Change the Brain URL

Edit `index.html` line:
```javascript
const BRAIN_URL = 'http://wcaasitteam.duckdns.org:5678/webhook/brain-intake';
```
