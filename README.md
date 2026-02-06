# Portfolio Website - README

## 🚀 Live Portfolio
**Mohanasundaram Murugesan** - Data Engineer

A premium portfolio website showcasing data engineering projects, experience, and live GitHub activity.

---

## ✨ Features

- **Premium Glassmorphism Design**: Modern, professional UI with blurred glass cards and cyan accents
- **Live GitHub Activity**: Automated ETL pipeline displaying real-time coding metrics
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **5 Featured Projects**: PhishGuard, Cloud Capacity Forecaster, ThreatIntel, Dark Data, Logistics Optimizer
- **Automated Updates**: GitHub Actions workflow updates activity data daily

---

## 🛠️ Tech Stack

### Frontend
- HTML5, CSS3, Vanilla JavaScript
- Glassmorphism design system
- Responsive grid layouts

### Data Pipeline
- Python 3 (standard library only)
- GitHub API integration
- JSON data storage

### Deployment
- Netlify / GitHub Pages / Vercel
- GitHub Actions for automation
- Free HTTPS and custom domain support

---

## 📂 Project Structure

```
portfolio_website/
├── index.html              # Main HTML file
├── css/
│   └── styles.css          # Glassmorphism styles
├── js/
│   ├── main.js             # Main JavaScript
│   └── github-activity.js  # GitHub activity visualization
├── scripts/
│   └── github_activity_pipeline.py  # ETL pipeline
├── data/
│   └── github_activity.json         # Generated activity data
├── assets/
│   └── images/
│       └── headshot.jpg    # Profile image
├── .github/
│   └── workflows/
│       └── update-activity.yml      # GitHub Actions workflow
└── DEPLOYMENT.md           # Deployment guide
```

---

## 🚀 Quick Start

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mohanasundaramm1/portfolio.git
   cd portfolio
   ```

2. **Run local server**:
   ```bash
   python3 -m http.server 8000
   ```

3. **Open in browser**:
   ```
   http://localhost:8000
   ```

### Update GitHub Activity

```bash
python3 scripts/github_activity_pipeline.py
```

---

## 🌐 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions on deploying to:
- **Netlify** (recommended)
- **GitHub Pages**
- **Vercel**

### Quick Deploy to Netlify

1. Go to https://app.netlify.com/drop
2. Drag the entire `portfolio_website` folder
3. Done! Your site is live in seconds

---

## 📊 GitHub Activity Pipeline

The portfolio features a **live data engineering showcase**:

1. **Extract**: Fetches GitHub events via API
2. **Transform**: Aggregates commits, repos, and events
3. **Load**: Saves to `data/github_activity.json`
4. **Visualize**: Displays stats cards and recent repos

**Automated Updates**: GitHub Actions runs the pipeline daily at midnight UTC.

---

## 🎨 Design System

### Colors
- **Navy Dark**: `#020c1b`
- **Navy Light**: `#112240`
- **Cyan**: `#64ffda`
- **Slate**: `#8892b0`
- **White**: `#e6f1ff`

### Typography
- **Headings**: Inter, sans-serif
- **Body**: Inter, sans-serif
- **Mono**: SF Mono, Fira Code

---

## 📝 Sections

1. **Hero**: Introduction and CTA
2. **Experience**: Work history (Bhramastra, Tata Elxsi)
3. **Projects**: 5 featured data engineering projects
4. **Skills**: Tech stack organized by category
5. **Education**: MS in Business Analytics (CSUEB), BE in CS (Anna University)
6. **Leadership**: AI Club President
7. **GitHub Activity**: Live coding metrics (NEW!)
8. **Contact**: Email and social links

---

## 🔗 Links

- **Resume**: [Google Drive](https://drive.google.com/file/d/1bWocFgA16_Pk7QOcWAtyewN3uVtUZVaZ/view)
- **GitHub**: [@mohanasundaramm1](https://github.com/mohanasundaramm1)
- **LinkedIn**: [mohanasundaramm](https://www.linkedin.com/in/mohanasundaramm/)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

Built with modern web technologies and data engineering best practices.

**Last Updated**: February 2026
