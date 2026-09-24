# Netlify Deployment Guide

This guide explains how to deploy the **Smart Farming Dashboard** to **Netlify** using Netlify's Python Serverless Functions and Global Edge CDN.

---

## 🏗️ Architecture Overview

| Component | How it Works on Netlify |
| :--- | :--- |
| **Backend Engine** | Flask wrapped using `serverless-wsgi` inside `netlify/functions/app.py`. |
| **Static Assets** | CSS, JS, and vendor icons are automatically synchronized to `public/static/` during build and served directly by Netlify's high-speed CDN. |
| **Routing** | Handled via `netlify.toml` and `public/_redirects`: `/static/*` served from CDN, `/*` routed to `/.netlify/functions/app`. |
| **Database** | SQLite database automatically initialized from `database/agritech.db` with demo accounts and seeded records, utilizing `/tmp` storage in serverless execution to prevent read-only filesystem errors. |

---

## 🚀 Deployment Methods

### Option 1: Deploy via GitHub (Recommended)

1. **Commit and Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Configure project for Netlify serverless deployment"
   git remote add origin https://github.com/<your-username>/<your-repo-name>.git
   git branch -M main
   git push -u origin main
   ```

2. **Connect to Netlify:**
   - Go to [Netlify App](https://app.netlify.com/).
   - Click **"Add new site"** > **"Import an existing project"**.
   - Select **GitHub** and authorize access.
   - Choose your repository.

3. **Verify Build Settings:**
   Netlify will automatically detect settings from `netlify.toml`:
   - **Build command:** `python build.py`
   - **Publish directory:** `public`
   - **Functions directory:** `netlify/functions`

4. **Environment Variables (Optional):**
   - Under **Site configuration** > **Environment variables**, you can set:
     - `SECRET_KEY`: A secure random string for session encryption (e.g. `your-production-secret-key-2026`).

5. **Deploy:**
   - Click **"Deploy site"**. Netlify will run `python build.py`, install Python dependencies from `requirements.txt`, bundle the function, and publish your site!

---

### Option 2: Deploy via Netlify CLI

If you prefer deploying directly from your terminal:

1. **Install Netlify CLI:**
   ```bash
   npm install -g netlify-cli
   ```

2. **Authenticate with Netlify:**
   ```bash
   netlify login
   ```

3. **Build & Deploy:**
   ```bash
   # Run the local build step
   python build.py

   # Deploy to Netlify production
   netlify deploy --prod
   ```

---

## 🔑 Demo Access Credentials

Once deployed, log in using any of the pre-seeded accounts:

| Role | Email | Password |
| :--- | :--- | :--- |
| **Farmer (User)** | `farmer@agritech.com` | `Farmer@123` |
| **Administrator** | `admin@agritech.com` | `Admin@123` |

---

## 🛠️ Local Testing

You can still run the application locally anytime:

```bash
# Standard local Flask server
python app.py
```
Or test the Netlify build script:
```bash
python build.py
```
