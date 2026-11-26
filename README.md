# Portfolio Website - README

## 🚀 Live Portfolio
**Mohanasundaram Murugesan** - Data Engineer

A premium portfolio website showcasing data engineering projects, experience, and live GitHub activity.

---

## ✨ Features

- **Recruiter-first layout**: headline, résumé button, and past roles are visible without scrolling
- **Light and dark themes**: follows the visitor's system setting, with a toggle that remembers their choice
- **Live GitHub activity**: a year-long contribution heatmap (private contributions included)
- **Accessible**: WCAG AA contrast in both themes, keyboard focus styles, skip link, reduced-motion support, print styles
- **Automated updates**: a GitHub Actions workflow refreshes the activity data weekly

---

## 🛠️ Tech Stack

### Frontend
- HTML5, CSS3, Vanilla JavaScript
- Token-based design system (CSS custom properties) with light and dark themes
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
│   └── styles.css          # Design tokens, light/dark themes, layout
├── js/
│   ├── main.js             # Main JavaScript
│   └── github-activity.js  # GitHub activity visualization
├── scripts/
│   └── github_activity_pipeline.py  # ETL pipeline
├── data/
│   └── github_activity.json         # Generated activity data
├── assets/
│   ├── images/
│   │   ├── headshot.jpg            # Original photo
│   │   └── headshot-portrait.jpg   # Optimized 4:5 crop used on the site
│   └── resume/
│       └── Mohanasundaram_Murugesan_Resume.pdf
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

1. **Extract**: Fetches repositories and events from the REST API, and the past year's contribution calendar from the GraphQL API (falling back to the public contributions page)
2. **Transform**: Computes contribution totals, streaks, and heatmap intensity levels
3. **Load**: Saves to `data/github_activity.json`
4. **Visualize**: Renders the heatmap and summary stats

Private contributions are counted because the GitHub profile setting "Include private contributions" is on; no private repository names or content are exposed.

**Automated Updates**: GitHub Actions runs the pipeline weekly (Sundays, 00:00 UTC).

---

## 🎨 Design System

### Colors (light / dark)
- **Deep teal (buttons, closing band)**: `#0c3b3f` / `#06272a`
- **Accent teal (two-tone headlines, key numbers)**: `#127a6f` / `#5ccfba`
- **Mint (alternating section bands)**: `#eef6f4` / `#0e1c1e`
- **Ink (headings)**: `#0e1f1e` / `#e9f3f1`
- **Body text**: `#2e4341` / `#b9cbc8`

All tokens live in `:root` and `[data-theme="dark"]` at the top of `css/styles.css`.

### Typography
- **Headlines**: Manrope 800, tight letter-spacing
- **Body**: IBM Plex Sans

### Principles
- Short, declarative headlines; the second line in the accent color
- Structure from whitespace and thin rules, not boxes, chips, or shadows
- Every number in the page copy comes from the résumé

---

## 📝 Sections

1. **Hero**: Headline, résumé button, and past roles
2. **Experience**: Banking Soft Solutions, CSUEB, Brahmastra, Tata Elxsi
3. **Results**: Three measured outcomes and where each came from
4. **How I build**: Three-step approach
5. **Skills**: Tech stack, certifications, education, and leadership
6. **Activity**: Contribution heatmap
7. **Contact**: Email (with copy button), LinkedIn, GitHub

---

## 🔗 Links

- **Resume**: [PDF](assets/resume/Mohanasundaram_Murugesan_Resume.pdf) (replace this file to update it)
- **GitHub**: [@mohanasundaramm1](https://github.com/mohanasundaramm1)
- **LinkedIn**: [mohanasundaram-murugesan](https://www.linkedin.com/in/mohanasundaram-murugesan/)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

Built with modern web technologies and data engineering best practices.

**Last Updated**: February 2026
