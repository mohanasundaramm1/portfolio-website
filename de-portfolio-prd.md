# Data Engineering Portfolio Website – Product Requirements Document (PRD)

## 1. Overview

### 1.1 Purpose
Design and implement a high-impact personal portfolio website for **Mohanasundaram Murugesan**, targeting **data engineering roles** in the US. The site should:
- Clearly communicate data engineering skills, experience, and projects.
- Showcase real, end-to-end data engineering work with measurable impact.
- Be performant, mobile-friendly, and professional.
- Be hosted for **free** with minimal ongoing maintenance.

### 1.2 Objectives
- Increase recruiter and hiring manager engagement (profile views → interview calls).
- Demonstrate **practical data engineering skills** (pipelines, orchestration, streaming, cloud, etc.).
- Centralize professional presence (resume, LinkedIn, GitHub, certifications, projects).

### 1.3 Success Metrics (Indicative)
- At least **3–5 interview inquiries** within 3 months of launch.
- Average **time on site** > 2 minutes.
- At least **50 unique visitors** per month (from LinkedIn, resume link, email signature).

---

## 2. Target Audience & Positioning

### 2.1 Primary Audience
- **Recruiters** hiring for data engineer / analytics engineer / ML data engineer roles.
- **Hiring managers** (Data Engineering Leads, Analytics Managers).

### 2.2 Secondary Audience
- Peers in data engineering and analytics.
- University professors / career services.

### 2.3 Positioning Statement
> "A pragmatic data engineer with hands-on experience building production-grade pipelines, medallion architectures, and streaming systems, now seeking data engineering roles in the US."

Tone: Confident but humble, impact-focused, technically solid.

---

## 3. Branding & Visual Direction

### 3.1 Brand Attributes
- **Professional** (enterprise-ready, trust-building)
- **Technical** (code, architecture, systems diagrams)
- **Clear & Minimal** (no clutter, easy to scan)

### 3.2 Visual Style
- Color palette: Dark blue / navy primary, accent with teal or green; plenty of white space.
- Typography: Clean, modern sans-serif (e.g., Inter, Roboto, or system fonts).
- Use simple line icons for tools (AWS, Snowflake, Python, Kafka, etc.).

### 3.3 Logo / Name Display
- Top-left: Text-based logo: **"Mohanasundaram | Data Engineer"**.

---

## 4. Information Architecture & Pages

### 4.1 Top-Level Navigation
- **Home**
- **Experience**
- **Projects**
- **Tech Stack**
- **Leadership** (optional; can be merged into About or Experience)
- **Resume**
- **Contact**

### 4.2 Page / Section Details

#### 4.2.1 Home (Landing)
Purpose: 10-second impression page answering "Who is this? Why should I care?"

Content blocks:
- Hero section:
  - Name: "Hi, I’m **Mohanasundaram Murugesan**"
  - Title: "Data Engineer | Streaming, Medallion Lakehouse, Cloud Analytics"
  - Short 2–3 line summary focused on outcomes (latency reduction, reliability, data quality, etc.).
  - Primary CTA: **"View Projects"**
  - Secondary CTA: **"Download Resume"**

- Quick Stats (Data-Engineering-Flavored):
  - Years of experience in data/AI.
  - Largest dataset volume handled.
  - Latency / cost / performance improvements from your projects.

- Highlighted badges/logos:
  - AWS Cloud Practitioner.
  - SnowPro Associate.
  - University (CSU East Bay, Anna University).


#### 4.2.2 Experience
Purpose: Expand on resume-style work experience but tailored for data engineering.

Per role (Tata Elxsi, Bhramastra):
- Role, company, location, dates.
- 3–5 bullet points each, already optimized for impact (as in resume), but visually structured:
  - Use bold for technologies.
  - Highlight measurable impact ("reduced batch processing time by 60%" etc.).
- Optional: Small architecture diagram per major project (static image).


#### 4.2.3 Projects
Purpose: This is the **core** section for data engineering.

Each project card should include:
- Title + short one-line tagline.
- Tech stack badges (PySpark, Airflow, Kafka, Snowflake, AWS, R, etc.).
- Problem, Solution, Impact structure:
  - **Problem**: What was broken or missing.
  - **Solution**: What you implemented (architecture, tools, patterns).
  - **Impact**: Metrics and outcomes.
- Links:
  - GitHub repo.
  - Blog post / detailed write-up (if any).

Projects to include (minimum):
1. **ThreatIntel | PySpark, Airflow, Kafka**
   - Emphasize medallion architecture, streaming enrichment, data quality.
   - Diagram: Bronze → Silver → Gold, with Airflow DAGs and Kafka ingestion.
2. **Cloud Capacity Forecasting | R**
   - Emphasize hybrid modeling, data pipeline, and impact on resource allocation.
3. At least **1 new portfolio-friendly project** designed specifically to be demoable:
   - Example: "GitHub Activity Analytics Pipeline" (see Section 6: Data Engineering Features).


#### 4.2.4 Tech Stack
Purpose: Quick way for recruiters to see tools at a glance.

Group by category:
- Languages: Python, SQL, R, Bash
- Data Engineering: PySpark, Airflow, Kafka, Delta Lake, Spark Structured Streaming, ETL/ELT, Hadoop, Hive
- Cloud & Databases: AWS (S3, Glue, Lambda, Redshift, EC2, IAM), Snowflake, PostgreSQL, MySQL, MS SQL Server
- ML: TensorFlow, Keras, Scikit-Learn, Computer Vision (YOLO, R-CNN), Pandas
- BI & Visualization: Tableau, Streamlit, Plotly
- DevOps / Tools: Docker, Git, CI/CD concepts

Use badges or tags with subtle color-coding.


#### 4.2.5 Leadership
Purpose: Showcase AI Club President experience.

- Role: President, Artificial Intelligence Club, CSUEB.
- Dates and location.
- 3–4 bullets highlighting:
  - Community building.
  - Workshops organized.
  - Bridging research and practice.

This page signals soft skills, initiative, and mentorship potential.


#### 4.2.6 Resume
- Embed a PDF viewer or provide a **Download Resume** button.
- Optional: Provide both "Data Engineer" and "Data Analyst" versions if needed (for the future).


#### 4.2.7 Contact
- Simple form or CTA buttons:
  - "Email Me" (mailto link).
  - LinkedIn profile link.
  - GitHub profile link.
- No need for complex backend – use either a static form service or links.

---

## 5. Functional Requirements

### 5.1 Core Functional Requirements
- Responsive design: Works well on desktop, tablet, and mobile.
- Fast load times (< 2–3 seconds on decent connection).
- Clear navigation with sticky header.
- Accessible color contrast and font sizes.

### 5.2 Data Engineering Showpiece Requirements
- At least **one live or regularly updated data artifact** on the site, e.g.:
  - A chart showing your **recent GitHub activity** (commits/repos).
  - A small dashboard snippet from one of your pipelines (e.g., processed events per day, success rate, etc.).
- Data should be updated via an automated process (e.g., GitHub Actions) to demonstrate:
  - Scheduling / orchestration.
  - Data extraction and transformation.
  - Storage and serving to the static site.

### 5.3 Non-Functional Requirements
- Uptime: As high as the free hosting platform allows (GitHub Pages / similar).
- Maintainability: Content should be easy to update via Markdown or simple HTML.
- Security: No secrets stored in the frontend code; minimal or no backend.

---

## 6. Data Engineering Feature: GitHub Activity Pipeline (Example)

### 6.1 Goal
Build a lightweight but real **ETL pipeline** whose output is rendered on the portfolio site.

Example use case: "GitHub Activity Analytics"
- Extract: GitHub API for user events or contributions.
- Transform: Aggregate by day/week, compute summary stats.
- Load: Save processed data (JSON/CSV) into the repo so it can be rendered on the static site.

### 6.2 Architecture (High-Level)
- **Orchestrator**: GitHub Actions (cron workflow, e.g., once per day).
- **Compute**: Python script executed in the CI environment.
- **Storage**: Versioned JSON/CSV file committed back to a `data/` or `assets/data/` folder in the repo.
- **Serving**: Frontend JavaScript reads the JSON and renders charts using a lightweight chart library.

### 6.3 Example Pipeline Steps
1. Scheduled GitHub Actions workflow triggers daily.
2. Python script:
   - Calls GitHub API for recent events/commits.
   - Normalizes and aggregates data (e.g., commits per day, repos touched).
   - Writes `data/github_activity.json`.
3. The site’s JS code loads this JSON and displays:
   - Bar chart: Commits per day (last 30 days).
   - Top repos by activity.

This demonstrates practical ETL, orchestration, monitoring (actions logs), and data serving for analytics.

---

## 7. Technology Stack & Hosting (Free)

### 7.1 Frontend Stack
- HTML5, CSS3, minimal JavaScript.
- Option A: Pure static HTML/CSS + vanilla JS.
- Option B: Static site generator (e.g., Jekyll or Hugo) if needed.

For simplicity and control, start with **Option A**.

### 7.2 Data Visualization
- Lightweight chart library (e.g., Chart.js or Plotly.js CDN) to render charts from JSON.

### 7.3 Hosting
Primary choice: **GitHub Pages**
- Free static hosting.
- Easy to integrate with GitHub Actions.
- Custom domain support if desired (optional).

Alternative free static hosting (if needed):
- Netlify (free tier).
- Vercel (free tier).

### 7.4 Domain
- Optional but recommended: Purchase a `.com` domain (e.g., `mohanasundaram.dev` or similar) and map it to GitHub Pages.

---

## 8. SEO & Analytics

### 8.1 SEO Basics
- Custom `<title>` and `<meta description>` for each page.
- Use semantic HTML (h1, h2, h3, section, article).
- Include keywords naturally:
  - "Data Engineer"
  - "PySpark", "Airflow", "Kafka", "Snowflake"
  - "Streaming data pipelines"

### 8.2 Schema Markup (Optional)
- Add `Person` schema for your profile.
- Add `Organization` or `EducationalOrganization` schema for universities.

### 8.3 Analytics
- Use a privacy-friendly analytics tool (e.g., Plausible, or simple Google Analytics if comfortable).
- Track:
  - Page views per section.
  - Referrers (LinkedIn, resume link, email, etc.).

---

## 9. Content Plan

### 9.1 Copywriting Guidelines
- Focus on **impact and outcomes**, not just tools.
- Keep paragraphs short; use bullet points.
- Use consistent tense and voice.

### 9.2 Sections to Draft
- Hero summary (2–3 sentences about you as a data engineer).
- 2–3 sentence intros for each main project.
- Longer case study style write-ups (optional blog-style pages) for:
  - ThreatIntel.
  - Cloud Capacity Forecasting.
  - GitHub Activity Analytics (or other new portfolio project).

---

## 10. Implementation Phases

### Phase 1 – Foundation (1–2 days)
- Set up GitHub repo for the portfolio.
- Decide structure: `index.html`, `projects.html`, `experience.html`, etc.
- Implement base layout, navigation, and theme (colors, typography).

### Phase 2 – Core Content (2–4 days)
- Implement Home, Experience, Projects, Tech Stack, Leadership, Resume, and Contact sections.
- Populate with existing resume content and refined copy.

### Phase 3 – Data Engineering Feature (2–3 days)
- Implement GitHub Actions workflow and Python script.
- Generate and store JSON/CSV data.
- Implement frontend chart rendering.

### Phase 4 – Polish & Launch (1–2 days)
- Test responsiveness and performance.
- Add favicon, Open Graph meta tags (for nice link previews).
- Connect custom domain (if applicable).
- Final review and publish.

---

## 11. Risks & Mitigations

- **Risk**: Over-complicating the stack.
  - **Mitigation**: Start with plain static HTML/CSS/JS; only add complexity when needed.

- **Risk**: Pipeline or GitHub Actions workflow fails.
  - **Mitigation**: Start with a simple API call and logging; add retries or error notifications later.

- **Risk**: Content becomes outdated.
  - **Mitigation**: Keep content mostly evergreen and schedule a quarterly review.

---

## 12. Future Enhancements (Optional)

- Add blog section for deep-dives into data engineering topics.
- Add more live data widgets (e.g., streaming demo metrics, mini dashboards from your projects).
- Integrate a small search feature across projects and posts.
- Add light/dark mode toggle for developer-friendly UX.

---

**End of PRD – Data Engineering Portfolio Website**
