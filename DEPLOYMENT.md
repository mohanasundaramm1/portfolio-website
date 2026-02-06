# Portfolio Deployment Guide

This guide covers **3 free hosting options** for your portfolio website.

---

## Option 1: Netlify (RECOMMENDED - Easiest)

### Why Netlify?
- ✅ Drag-and-drop deployment
- ✅ Automatic HTTPS
- ✅ Custom domain support
- ✅ Continuous deployment from GitHub
- ✅ Free subdomain: `yourname.netlify.app`

### Steps:

#### Method A: Drag & Drop (Fastest - 2 minutes)

1. **Go to Netlify**: https://www.netlify.com/
2. **Sign up** with GitHub (or email)
3. **Drag & Drop**:
   - Go to https://app.netlify.com/drop
   - Drag your entire `portfolio_website` folder into the browser
   - Wait 10 seconds for deployment
4. **Done!** Your site is live at `random-name.netlify.app`

#### Method B: GitHub Integration (Best for updates)

1. **Create GitHub Repository**:
   ```bash
   cd /Users/mohanasundarammurugasen/dev/portfolio_website
   git init
   git add .
   git commit -m "Initial portfolio commit"
   git branch -M main
   git remote add origin https://github.com/mohanasundaramm1/portfolio.git
   git push -u origin main
   ```

2. **Connect to Netlify**:
   - Go to https://app.netlify.com/
   - Click **"Add new site"** → **"Import an existing project"**
   - Choose **GitHub**
   - Select your `portfolio` repository
   - Build settings:
     - **Build command**: Leave empty (static site)
     - **Publish directory**: `.` (root)
   - Click **"Deploy site"**

3. **Custom Domain** (Optional):
   - Go to **Site settings** → **Domain management**
   - Click **"Add custom domain"**
   - Follow instructions to add your domain

4. **Auto-update GitHub Activity**:
   - Every time you push to GitHub, Netlify auto-deploys
   - Set up GitHub Actions (see below) to update `data/github_activity.json` daily

---

## Option 2: GitHub Pages

### Why GitHub Pages?
- ✅ Free hosting directly from GitHub
- ✅ Custom domain support
- ✅ Easy integration with GitHub Actions
- ✅ Free subdomain: `username.github.io/portfolio`

### Steps:

1. **Create Repository** (if not done):
   ```bash
   cd /Users/mohanasundarammurugasen/dev/portfolio_website
   git init
   git add .
   git commit -m "Initial portfolio commit"
   git branch -M main
   git remote add origin https://github.com/mohanasundaramm1/portfolio.git
   git push -u origin main
   ```

2. **Enable GitHub Pages**:
   - Go to your repo: https://github.com/mohanasundaramm1/portfolio
   - Click **Settings** → **Pages**
   - Under **Source**, select:
     - Branch: `main`
     - Folder: `/ (root)`
   - Click **Save**

3. **Access Your Site**:
   - Your site will be live at: `https://mohanasundaramm1.github.io/portfolio/`
   - Wait 2-3 minutes for first deployment

4. **Custom Domain** (Optional):
   - In **Settings** → **Pages** → **Custom domain**
   - Add your domain (e.g., `mohanasundaram.dev`)
   - Update DNS settings with your domain provider

---

## Option 3: Vercel

### Why Vercel?
- ✅ Fast global CDN
- ✅ Automatic HTTPS
- ✅ GitHub integration
- ✅ Free subdomain: `yourname.vercel.app`

### Steps:

1. **Sign up**: https://vercel.com/signup
2. **Import Project**:
   - Click **"Add New Project"**
   - Import from GitHub
   - Select your `portfolio` repository
3. **Deploy**:
   - Framework Preset: **Other**
   - Build Command: Leave empty
   - Output Directory: `.`
   - Click **Deploy**

---

## Automating GitHub Activity Updates

To keep your GitHub Activity section fresh, set up a **GitHub Actions workflow** that runs daily.

### Create `.github/workflows/update-activity.yml`:

```yaml
name: Update GitHub Activity

on:
  schedule:
    # Runs daily at 00:00 UTC
    - cron: '0 0 * * *'
  workflow_dispatch:  # Allows manual trigger

jobs:
  update-activity:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Run GitHub Activity Pipeline
        run: |
          python3 scripts/github_activity_pipeline.py
      
      - name: Commit updated data
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add data/github_activity.json
          git diff --quiet && git diff --staged --quiet || git commit -m "Update GitHub activity data"
          git push
```

### Enable the Workflow:

1. Create the file above in your repository
2. Push to GitHub:
   ```bash
   git add .github/workflows/update-activity.yml
   git commit -m "Add GitHub Actions workflow"
   git push
   ```
3. The workflow will run daily and update your activity data automatically!

---

## Comparison Table

| Feature | Netlify | GitHub Pages | Vercel |
|---------|---------|--------------|--------|
| **Ease of Setup** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Custom Domain** | ✅ Free | ✅ Free | ✅ Free |
| **HTTPS** | ✅ Auto | ✅ Auto | ✅ Auto |
| **Build Time** | Fast | Medium | Fast |
| **CDN** | Global | GitHub's | Global |
| **Analytics** | ✅ Built-in | ❌ | ✅ Built-in |

---

## Recommended Workflow

1. **Start with Netlify** (drag & drop) to see your site live in 2 minutes
2. **Set up GitHub** repository for version control
3. **Connect Netlify to GitHub** for automatic deployments
4. **Add GitHub Actions** workflow to auto-update activity data
5. **(Optional)** Buy a custom domain and connect it

---

## Quick Start Commands

```bash
# Initialize Git (if not done)
cd /Users/mohanasundarammurugasen/dev/portfolio_website
git init
git add .
git commit -m "Initial portfolio commit"

# Create GitHub repo and push
git branch -M main
git remote add origin https://github.com/mohanasundaramm1/portfolio.git
git push -u origin main

# Then deploy via Netlify or GitHub Pages (see above)
```

---

## Need Help?

- **Netlify Docs**: https://docs.netlify.com/
- **GitHub Pages Docs**: https://docs.github.com/en/pages
- **Vercel Docs**: https://vercel.com/docs

Your portfolio is ready to go live! 🚀
