# Praveen — Portfolio Website

A personal portfolio website built with HTML, CSS, and a Python (Flask) backend.

---

## 📁 Files

| File | Purpose |
|---|---|
| `index.html` | Main portfolio website |
| `app.py` | Python Flask backend (API + server) |
| `requirements.txt` | Python dependencies |
| `logo.png` | Your logo image |

---

## 🚀 How to Run Locally

### 1. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the backend
```bash
python app.py
```

### 3. Open in browser
Visit: [http://localhost:5000](http://localhost:5000)

---

## 🌐 How to Host on GitHub Pages (Frontend only)

1. Go to your GitHub repository
2. Click **Settings** → **Pages**
3. Set source: `main` branch → `/ (root)`
4. Your site will be live at:  
   `https://yourusername.github.io/repository-name`

---

## 📤 How to Upload to GitHub

Run these commands in your terminal inside the project folder:

```bash
git init
git add .
git commit -m "Initial portfolio upload"
git branch -M main
git remote add origin https://github.com/yourusername/portfolio.git
git push -u origin main
```

---

## ✏️ How to Edit

- **Your info** → Edit `index.html` (look for `✏️` comments)
- **Instagram** → Search `YOUR_INSTAGRAM` and replace with your handle
- **Email** → Search `your@email.com` and replace
- **GitHub link** → Search `yourusername` and replace
- **Projects** → Edit the project cards in `index.html` or update `/api/projects` in `app.py`
- **Backend config** → Edit top section of `app.py`

---

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3 (Dark theme, animations)
- **Backend**: Python 3, Flask, Flask-CORS
- **APIs**: `/api/contact`, `/api/projects`, `/api/profile`

---

Made with ❤️ by Praveen
