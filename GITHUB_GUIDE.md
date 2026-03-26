# 📤 How to Upload Your Portfolio to GitHub
## Step-by-Step Guide for Praveen

---

## STEP 1 — Create a Repository on GitHub

1. Go to 👉 https://github.com
2. Click the **green "New"** button (top left)
3. Fill in:
   - **Repository name**: `portfolio`  (or any name you like)
   - **Description**: My personal portfolio website
   - **Visibility**: Public  ← important for free hosting
   - ❌ Do NOT check "Add a README file" (we already have one)
4. Click **"Create repository"**
5. GitHub will show you a page with commands — keep it open!

---

## STEP 2 — Install Git (if not installed)

Open your **Terminal** (Mac/Linux) or **Command Prompt** (Windows) and type:

```bash
git --version
```

If you see a version number → ✅ Git is installed, skip to Step 3.

If not → Download from: https://git-scm.com/downloads  
Install it, then restart your terminal.

---

## STEP 3 — Put Your Files in One Folder

Make sure all these files are in the **same folder** on your computer:

```
portfolio/
├── index.html       ← your website
├── app.py           ← Python backend
├── requirements.txt
├── README.md
├── .gitignore
└── logo.png         ← your logo image
```

---

## STEP 4 — Open Terminal in That Folder

**Windows:**  
- Open the folder in File Explorer  
- Hold `Shift` + Right-click inside the folder  
- Click **"Open PowerShell window here"**

**Mac:**  
- Right-click the folder  
- Click **"New Terminal at Folder"**

---

## STEP 5 — Run These Commands (one by one)

Copy and paste each line, press Enter after each:

```bash
git init
```
*(Initializes git in your folder)*

```bash
git add .
```
*(Adds all files)*

```bash
git commit -m "My portfolio website - first upload"
```
*(Saves a snapshot)*

```bash
git branch -M main
```
*(Names your branch "main")*

```bash
git remote add origin https://github.com/YOURUSERNAME/portfolio.git
```
⚠️ Replace `YOURUSERNAME` with your actual GitHub username!

```bash
git push -u origin main
```
*(Uploads everything to GitHub)*

---

## STEP 6 — Check GitHub

1. Go to `https://github.com/YOURUSERNAME/portfolio`
2. You should see all your files there ✅

---

## STEP 7 — Enable Free Hosting (GitHub Pages)

1. In your repository, click **"Settings"** (top menu)
2. Scroll down to **"Pages"** (left sidebar)
3. Under **Source**, select:
   - Branch: `main`
   - Folder: `/ (root)`
4. Click **Save**
5. Wait 2–3 minutes
6. Your site will be live at:  
   👉 `https://YOURUSERNAME.github.io/portfolio`

---

## ✏️ How to Update the Site Later

Whenever you change a file:

```bash
git add .
git commit -m "Updated projects section"
git push
```

That's it! Changes go live automatically in a few minutes.

---

## ❓ Common Errors & Fixes

| Error | Fix |
|---|---|
| `git: command not found` | Install Git from git-scm.com |
| `remote origin already exists` | Run: `git remote remove origin` then add again |
| `Permission denied` | Make sure you're logged into GitHub in terminal |
| `Push rejected` | Run: `git pull origin main --rebase` then push again |

---

Need help with any step? Just tell me which step and what error you see! 🙌
