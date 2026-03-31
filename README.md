# 🛡️ Sentinel AI — Intelligent Disaster Management Platform

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![SQLite](https://img.shields.io/badge/SQLite%20%2F%20PostgreSQL-Ready-003B57?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Twilio](https://img.shields.io/badge/Twilio-WhatsApp_API-F22F46?style=for-the-badge&logo=twilio&logoColor=white)](https://twilio.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

**An enterprise-grade, AI-powered disaster response platform built for India's coastal communities.**  
*Turning fragmented, reactive crisis management into a proactive, automated, and intelligent command system.*

[Problem Statement](#-the-problem) • [Why Sentinel AI?](#-why-this-stands-out-vs-existing-platforms) • [Features](#-features) • [Architecture](#-system-architecture) • [Getting Started](#-getting-started) • [API Reference](#-api-reference) • [WhatsApp Bot](#-whatsapp-bot) • [Database Schema](#-database-schema)

</div>

---

## 🌊 The Problem

India has **7,516 km of coastline** with over **170 million people** living in low-lying areas vulnerable to cyclones, floods, storm surges, and tsunamis. Traditional disaster response in these regions suffers from systemic failures:

- **Fragmented communication** — citizens call helplines, officials check social media, volunteers wait for orders. There is no unified channel.
- **Slow verification** — a field report of rising floodwater takes hours to be manually confirmed by authorities, delaying response.
- **Inefficient volunteer dispatch** — coordinators manually phone or message volunteers one by one, losing precious minutes.
- **Language barriers** — critical alerts reaching local fishermen or coastal residents in non-native languages are often ignored.
- **Zero predictive capabilities** — agencies react to disasters rather than simulating impacts ahead of time based on climate data.

**The result:** Response times measured in hours. Lives and resources lost that could have been saved.

---

## ⚡ Why This Stands Out vs Existing Platforms

Most existing disaster management systems (like standard NDMA portals or generic SOS apps) act merely as static information boards or one-way alert broadcasters. **Sentinel AI** acts as an autonomous nervous system for crisis management.

| Feature Area | Traditional Platforms | 🛡️ Sentinel AI |
|--------------|-----------------------|----------------|
| **Response Speed** | Manual verification (takes hours) | **Sub-second AI Validation** (3-parameter checking algorithm) |
| **Accessibility** | Requires app downloads, English-first | **No-install PWA + WhatsApp integration + Voice SOS.** Auto-translates to 6 regional languages via GPS. |
| **Volunteer Logistics** | Manual phone trees, chaotic WhatsApp groups | **"Uber-style" Auto-Dispatch.** Finds available responders within a 10km radius dynamically matching skills via WhatsApp bot. |
| **Alerting Precision** | Mass SMS blasts (causes panic & alert fatigue) | **Smart Geo-Fencing**. Alerts only hit users strictly within the hazard's specific impact radius based on severity. |
| **Resource Supply Chain**| Top-down government handouts only | **LifeLine P2P Marketplace.** Decentralized local networking to match resource Donors with Requesters in real time. |
| **Predictive Power** | Reactive (post-disaster mapping) | **Risk Simulator.** Simulates localized climate hazards based on live metrics, predicting infrastructural stress before it happens. |

By collapsing reporting, verification, dispatch, and resource matching into a single autonomous pipeline, a process that used to take dozens of phone calls now takes **minutes**.

---

## ✨ Features

### 🚨 1. Voice SOS & Crowdsourced Reporting
* **One-Tap Audio SOS**: Citizens can simply speak into their phones. The system uses natural language processing (NLP) to extract transcripts, identify keywords (e.g., "stuck," "water rising"), automatically categorize the hazard, and elevate priority to 'Critical'.
* **Standard Reporting**: Fast manual reporting via PWA.
* **AI Verification Engine**: Every report is instantly scored by the **3-Parameter Accuracy System™**:
  - **Heatmap Match (33%)**: Cross-references spatial density of similar reports in a 5.5km radius over 24 hours.
  - **Climate Alignment (33%)**: Queries Open-Meteo API to ensure live weather conditions (wind speed, humidity, etc.) mathematically support the claimed hazard.
  - **User Quality Score (34%)**: Evaluates the historical credibility of the reporter based on past approval rates and account tier.
* **Auto-Approval**: Reports scoring **≥ 85%** bypass human review, instantly triggering downstream alerts and volunteer dispatches.

### 🤝 2. Automated Volunteer Dispatch (Uber-Style Rescue)
Once a hazard is verified, the system's logistics engine takes over:
1. Queries database for registered, available volunteers strictly within a **10 km radius**.
2. Fires a **WhatsApp interactive message** (via Twilio) detailing hazard severity, coordinates, and photo evidence.
3. Volunteers reply "1" to Accept or "2" to Decline directly within WhatsApp.
4. Dashboard updates live for officials (Pending → Accepted → En Route → Completed).
5. Post-rescue, volunteers upload photographic proof to close the ticket and receive gamified rank points.

### 🌍 3. Live Hazard Map, Simulator & Analytics
- **Live Spatial Dashboards**: Leaflet.js heatmaps overlaid with real-time RainViewer weather radar layers.
- **Risk Simulator**: A deterministic modeling tool for analysts. Input impending rainfall (mm) and sea-level anomalies; the AI predicts sectoral infrastructure damage (Power, Water, Telecom, Housing) and outputs an actionable evacuation priority.
- **Urban Resilience Index (URI)**: A dynamic, rolling score per geographic zone calculated from response times, hazard frequency, and community eco-activity density.

### 📢 4. Smart Geo-fenced Multi-channel Alerts
Prevents alert fatigue. If a Storm Surge is detected, the system sends push notifications and WhatsApp alerts strictly to users whose saved Home Locations fall within a scaled radius (e.g., 15km for storm surge, 2km for swell surge) rather than spamming entire states.

### 🌐 5. Auto-detected Multilingual Interface
Using an algorithmic map of Indian coastal linguistic boundaries, the PWA auto-loads the correct language (English, Tamil, Malayalam, Telugu, Kannada, Hindi) based on the user's GPS coordinates upon first load. Supports manual toggling as well.

### 🛰️ 6. LifeLine — P2P Emergency Resource Marketplace
When supply chains break down, communities survive together.
- **SafeLink™ Matching Engine**: Users list what they need (insulin, boats, blankets) or what they have. The algorithm auto-pairs Donors with Requesters based on proximity.
- **Visual Mapping**: Glowing connection lines appear on the LifeLine map to visualize successful supply handoffs natively.

### ♻️ 7. Eco-Sustainability Tracker (Mitigation & Gamification)
Building resilience before disaster strikes. Users log eco-friendly behaviors (plastic reduction, public transit, tree planting) to earn points and level up (Eco Beginner → Climate Hero). Activities are optionally photo-verified by AI, converting efforts into estimated kilograms of CO2 saved. Includes leaderboards and badges.

### 🏛️ 8. Government-NGO Coordination Platform
A centralized command sector restricted to `official` and `agency` roles:
- **Agency Registry**: Register specific government departments and NGOs.
- **Resource Allocation Ledger**: Track exact quantities of medical/food supplies sent from distinct agencies to specific emergency checkpoints (Allocated → Deployed → Used → Returned).
- **SITREPs**: Formal situation reports mapped against ongoing emergency events.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      BROWSER / PWA CLIENT                       │
│                                                                 │
│  Bootstrap 5 · Vanilla CSS (Glassmorphism) · Leaflet.js         │
│  Service Worker · Web App Manifest (Add-to-Homescreen)          │
│  Language: Auto-detected by GPS · Polling every 5s              │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTPS
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                     FLASK APPLICATION                           │
│                  (Factory Pattern · Port 5001)                  │
│                                                                 │
│  ┌───────────────┐ ┌────────────────┐ ┌─────────────────────┐  │
│  │ Report Engine │ │Volunteer Engine│ │  WhatsApp Handler   │  │
│  │ 3-Param AI    │ │ Auto-Dispatch  │ │  Twilio Webhooks    │  │
│  │ Geo-Alerts    │ │ 10km Geo-Query │ │  Multi-step Session │  │
│  └───────┬───────┘ └───────┬────────┘ └──────────┬──────────┘  │
│          │                 │                     │             │
│  ┌───────▼─────────────────▼─────────────────────▼──────────┐  │
│  │                SQLAlchemy ORM                             │  │
│  │                                                           │  │
│  │  sqlite:///site.db  (dev)                                 │  │
│  │  postgresql://...   (production)                          │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              APScheduler Background Jobs                 │   │
│  │  • Scheduled DB cleanup                                  │   │
│  │  • Weather data pre-fetching                             │   │
│  │  • Alert expiry processing                               │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────────┬─────────────────────────────────────────── ┘
                     │
         ┌───────────┴────────────┐
         │                        │
┌────────▼──────────┐  ┌──────────▼─────────────────────────────┐
│   Twilio API      │  │         Open-Meteo API (Free)           │
│                   │  │                                         │
│ WhatsApp messages │  │ GET /v1/forecast?latitude=...           │
│ Inbound webhooks  │  │ temperature_2m · humidity_2m            │
│ Media attachments │  │ wind_speed_10m · weather_code           │
└───────────────────┘  └─────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
disaster_management/
│
├── app.py              # Main Flask application — all routes, business logic,
│                       # WhatsApp bot handler, background scheduler jobs,
│                       # multilingual translation tables, and AI analytics
│
├── models.py           # SQLAlchemy ORM models (15 tables — see schema below)
│
├── forms.py            # WTForms definitions for all user-facing forms
│                       # (registration, reporting, coordination, eco-tracking, etc.)
│
├── utils.py            # Core utility library:
│                       # - 3-Parameter AI validation engine
│                       # - Haversine distance calculator
│                       # - WhatsApp/Twilio message sender
│                       # - Geo-fenced alert logic
│                       # - Carbon savings calculator
│                       # - Eco-activity point system
│
├── translations.py     # Extended multilingual string tables (6 languages)
│
├── config.py           # Environment-aware Flask configuration
│
├── requirements.txt    # Python dependencies
├── Procfile            # Heroku/Render deployment entry point
├── start_system.sh     # Helper script to start app + tunnel
├── setup_whatsapp.sh   # WhatsApp Twilio sandbox setup helper
│
├── static/
│   ├── css/style.css   # Global stylesheet (glassmorphism, animations)
│   ├── js/script.js    # Core frontend JS (maps, notifications, polling)
│   ├── js/pwa.js       # Progressive Web App registration
│   ├── sw.js           # Service Worker (offline caching)
│   ├── manifest.json   # PWA manifest (icons, display mode)
│   ├── icons/          # PWA app icons (various sizes)
│   └── uploads/        # User-uploaded photos and videos
│
├── templates/          # Jinja2 HTML templates
│   ├── base.html           # Global layout: navbar, notification bell,
│   │                       # real-time polling JS, toast notifications
│   ├── home.html           # Landing page + live report feed
│   ├── report.html         # Hazard submission form
│   ├── dashboard.html      # Analytics dashboard
│   ├── lifeline_map.html   # LifeLine P2P resource map
│   ├── coordination.html   # Coordinator command center
│   ├── volunteer_management.html
│   ├── situation_reports.html
│   ├── notifications.html
│   └── ...                 # 30+ additional templates
│
├── migrations/         # Flask-Migrate Alembic database migrations
└── instance/           # SQLite database file (gitignored)
```

---

## 🗄️ Database Schema

The application uses **15 database tables** managed via SQLAlchemy + Flask-Migrate:

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CORE MODELS                                 │
├──────────────────┬──────────────────────────────────────────────────┤
│ User             │ id · username · email · password_hash · role      │
│                  │ points · level · language · home_lat/lon          │
│                  │ whatsapp_number · whatsapp_session (multi-step)   │
│                  │ alert_preferences (JSON) · push_token             │
├──────────────────┼──────────────────────────────────────────────────┤
│ Report           │ id · title · description · hazard_type · location │
│                  │ latitude · longitude · image_file · video_file    │
│                  │ confidence_score · ai_analysis                    │
│                  │ verification_status (pending/approved/rejected)   │
│                  │ priority · status · alert_radius · alert_sent     │
│                  │ likes_count · comments_count · views_count        │
├──────────────────┼──────────────────────────────────────────────────┤
│ Notification     │ id · user_id · message · report_id · assignment_id│
│                  │ is_read · is_alert · created_at · expires_at      │
├──────────────────┼──────────────────────────────────────────────────┤
│ Like             │ id · user_id · report_id (unique constraint)      │
│ Comment          │ id · user_id · report_id · text · timestamp       │
│ LocalApproval    │ id · user_id · report_id (crowd-verification)     │
│ ReportView       │ id · user_id · report_id (unique view tracking)   │
│ Badge / UserBadge│ Achievement system                                │
│ followers        │ Association table (follower_id · followed_id)     │
└──────────────────┴──────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    COORDINATION MODELS                              │
├──────────────────┬──────────────────────────────────────────────────┤
│ Agency           │ Government / NGO registry                        │
│ EmergencyEvent   │ Formal incident creation by officials            │
│ ResourceAlloc.   │ Agency resource → event allocation tracking      │
│ Volunteer        │ Volunteer profile (skills, availability, location)│
│ VolunteerAssign. │ Assignment lifecycle: pending→accepted→completed  │
│                  │ + completion_photo + points_earned               │
│ SituationReport  │ Structured field reports (SITREPs) by officials  │
└──────────────────┴──────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│               SUSTAINABILITY & COMMUNITY MODELS                     │
├──────────────────┬──────────────────────────────────────────────────┤
│ PlasticUsage     │ Plastic reduction log with AI verification score  │
│ CarbonSavings    │ General eco-activity carbon offset records        │
│ CommunityEvent   │ Disaster-prep / environmental meetups            │
│ EventParticipant │ User ↔ CommunityEvent participation tracking     │
└──────────────────┴──────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    LIFELINE P2P MODELS                              │
├──────────────────┬──────────────────────────────────────────────────┤
│ ResourceListing  │ Have / Need listings (food, water, medical, etc.) │
│ ResourceMatch    │ SafeLink™ — matching a "need" to a "have"        │
└──────────────────┴──────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│              URBAN RESILIENCE INDEX (URI) MODELS                    │
├──────────────────┬──────────────────────────────────────────────────┤
│ ResilienceZone   │ Geographic grid zones for scoring                │
│ ResilienceScore  │ Historical 0–100 URI scores per zone+period      │
└──────────────────┴──────────────────────────────────────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

| Requirement | Notes |
|-------------|-------|
| **Python 3.9+** | Tested on 3.11 |
| **Twilio Account** | Free trial works; needs WhatsApp Sandbox enabled |
| **Ngrok / tunnel** | Required for local WhatsApp webhook testing only |

### 1. Clone & Set Up Environment

```bash
git clone https://github.com/varunmax7/MaxAlert-AI.git
cd MaxAlert-AI

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
# --- Core ---
SECRET_KEY=replace-with-a-long-random-string
DATABASE_URL=sqlite:///site.db       # For production: postgresql://user:pass@host/db

# --- Twilio WhatsApp ---
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886   # Twilio Sandbox number

# --- Optional: Public base URL (needed for WhatsApp media attachments) ---
BASE_URL=https://your-ngrok-subdomain.ngrok-free.app
```

> **Note:** `DATABASE_URL` starting with `postgres://` is automatically rewritten to `postgresql://` (Heroku compatibility).

### 3. Initialise the Database

```bash
flask db upgrade
```

This runs all Alembic migration scripts and creates the database schema. For a fresh SQLite database, this also runs `db.create_all()` automatically on app start.

### 4. Run the Application

```bash
python app.py
# Server starts on http://0.0.0.0:5001
# Access locally: http://localhost:5001
# Access on LAN:  http://192.168.x.x:5001
```

### 5. Expose to Internet (For WhatsApp & Mobile Testing)

```bash
# Option A: ngrok (recommended for development)
ngrok http 5001
# Copy the https://xxxxx.ngrok-free.app URL

# Option B: Cloudflare Tunnel (no account needed for quick test)
cloudflared tunnel --url http://localhost:5001
```

Then in **Twilio Console → Messaging → Try it out → Send a WhatsApp message**, set your webhook URL to:
```
https://YOUR-TUNNEL-URL/whatsapp/webhook
```

---

## 📡 API Reference

All JSON endpoints require authentication unless noted otherwise.

### Reports

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/api/reports` | ✅ | Paginated list of all reports |
| `GET` | `/api/reports/active` | ✅ | Active (non-resolved) reports |
| `GET` | `/api/hazards/map` | ✅ | GeoJSON FeatureCollection for Leaflet map |
| `GET` | `/api/report/<id>/accuracy_3param` | ✅ | Full 3-parameter AI accuracy breakdown |
| `POST` | `/report` (form) | ✅ | Submit a new hazard report |
| `POST` | `/approve_report/<id>` | 🔐 Official | Manually approve a pending report |
| `POST` | `/reject_report/<id>` | 🔐 Official | Reject a report with reason |

### Notifications

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/api/notifications/unread-count` | ✅ | Returns `{"count": N}` — polled every 5 s |
| `POST` | `/api/notification/<id>/read` | ✅ | Mark a notification as read |
| `POST` | `/api/notifications/mark-all-read` | ✅ | Mark all notifications as read |

### Coordination

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/api/coordination/assignments/active` | 🔐 Official | Active volunteer assignments |
| `POST` | `/api/volunteer/assign` | 🔐 Official | Assign a volunteer to a hazard |
| `POST` | `/api/volunteer/<id>/complete` | ✅ Volunteer | Submit rescue completion + proof photo |
| `GET` | `/api/lifeline/listings` | ✅ | All open resource listings |
| `POST` | `/api/lifeline/match` | ✅ | Create a SafeLink match between listings |

### WhatsApp

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/whatsapp/webhook` | (Twilio sig) | Inbound message handler (Twilio callback) |

### Example Response: 3-Parameter Accuracy

```http
GET /api/report/42/accuracy_3param
Authorization: (session cookie)
```

```json
{
  "report_id": 42,
  "title": "Storm Surge at Marina Beach",
  "hazard_type": "storm_surge",
  "overall_accuracy_percent": 83,

  "parameter_1_heatmap": {
    "name": "Heatmap Match",
    "score_percent": 85,
    "analysis": "Moderate heatmap confirmation: 3 similar reports detected in area",
    "weight": "33%"
  },

  "parameter_2_climate": {
    "name": "Climate Alignment",
    "score_percent": 90,
    "analysis": "Storm conditions confirmed: High winds 31km/h detected",
    "weight": "33%"
  },

  "parameter_3_user_quality": {
    "name": "User Quality Score",
    "score_percent": 74,
    "analysis": "Good track record: 7/10 reports approved (70%)",
    "weight": "34%",
    "user_role": "citizen",
    "user_level": 5,
    "user_total_reports": 10
  },

  "detailed_breakdown": "Heatmap Match: 85% | Climate Alignment: 90% | User Quality: 74%"
}
```

### Accuracy Score Interpretation

| Score | Classification | System Action |
|-------|---------------|--------------|
| **85–100%** | 🟢 Highly Reliable | Auto-approved, alerts dispatched immediately |
| **60–84%** | 🟡 Good Confidence | Queued for analyst review |
| **40–59%** | 🟠 Questionable | Held for investigation, additional evidence requested |
| **0–39%** | 🔴 Low Confidence | Flagged, possible misinformation |

---

## 📱 WhatsApp Bot

The WhatsApp integration uses Twilio's Messaging API. The bot handles **two distinct interaction flows**:

### Flow 1: Account Linking

New users link their web account to their WhatsApp number through a guided 3-step conversation. Session state is stored per phone number in the `User.whatsapp_session` JSON field.

```
User  →  "Hi"
Bot   →  "👋 Welcome to Sentinel AI! Please enter your username."
User  →  "john_doe"
Bot   →  "🔐 Please enter your password."
User  →  "••••••••"
Bot   →  "✅ Successfully linked! You'll now receive hazard alerts and volunteer
          assignments directly on WhatsApp."
```

### Flow 2: Volunteer Dispatch & Response

```
[Hazard verified by system]

Bot   →  📸 [Hazard photo in attachment]
Bot   →  "🚨 *STORM SURGE ALERT*
          Location: Marina Beach, Chennai
          Distance: 3.2 km from you
          Severity: HIGH

          🤝 Your help is needed.
          Reply *1* to Accept
          Reply *2* to Decline"

User  →  "1"

Bot   →  "✅ *Mission Accepted!*
          📍 Hazard coordinates: 13.0566, 80.2783
          A coordinator will contact you shortly.
          Reply *cancel* at any time if you cannot attend."

[Volunteer completes rescue]
Bot   →  "🏆 Mission completed! You earned 50 points.
          Your total: 340 points | Level: 7"
```

### Supported Commands (at any time)

| Command | Response |
|---------|----------|
| `status` | Current assignment status |
| `cancel` | Cancel current active assignment |
| `help` | List available commands |
| `Hi` / `hello` | Start account linking flow |

---

## 🎮 User Roles & Permissions

| Role | Who | Key Permissions |
|------|-----|----------------|
| `citizen` | General public | Submit reports, join LifeLine, earn points |
| `volunteer` | Registered responders | Accept missions, complete rescues, earn rescue points |
| `official` | Government officers | Approve/reject reports, create emergency events, assign volunteers, view all dashboards |
| `analyst` | Data scientists | Full read access to analytics, reporting trends, URI data |
| `agency` | NGO/Emergency org | Same as official for their assigned events |

---

## 🛠️ Tech Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Language** | Python | 3.9+ | Backend runtime |
| **Web Framework** | Flask | ≥ 2.3.3 | HTTP server, routing, templating |
| **Auth** | Flask-Login | ≥ 0.6.3 | Session management |
| **Forms** | Flask-WTF + WTForms | ≥ 1.2.1 | Server-side form validation |
| **ORM** | Flask-SQLAlchemy | ≥ 3.1.1 | Database abstraction |
| **Migrations** | Flask-Migrate (Alembic) | ≥ 4.0.7 | Schema version control |
| **Task Scheduler** | APScheduler | ≥ 3.10.5 | Background jobs |
| **Messaging** | Twilio | ≥ 9.0.0 | WhatsApp API (send + receive) |
| **Weather** | Open-Meteo | (REST API) | Free, no-key live weather data |
| **Maps (frontend)** | Leaflet.js | CDN | Interactive maps + heatmaps |
| **Map tiles** | OpenStreetMap / Voyager | (CDN) | Base map tiles |
| **Weather radar** | RainViewer | (API) | Satellite precipitation overlay |
| **Charting** | Matplotlib + NumPy | ≥ 3.8 | Server-rendered analytics charts |
| **NLP** | TextBlob + NLTK | ≥ 0.18 | Report text analysis |
| **DB (dev)** | SQLite | Built-in | Development database |
| **DB (prod)** | PostgreSQL | ≥ 14 | Production database |
| **WSGI** | Gunicorn | ≥ 21.2 | Production app server |
| **Styling** | Bootstrap 5 + Custom CSS | CDN | UI framework + Glassmorphism |
| **PWA** | Service Worker + Manifest | Web standard | Mobile add-to-homescreen |

---

## ☁️ Deployment

### Render (Recommended — Free Tier Available)

1. Push to GitHub.
2. Create a new **Web Service** on [render.com](https://render.com), connect your repository.
3. Set **Build Command**: `pip install -r requirements.txt`
4. Set **Start Command**: `gunicorn app:app`
5. Add all environment variables from `.env` in the **Environment** tab.
6. Add a free **PostgreSQL** database add-on and copy the `DATABASE_URL`.
7. Deploy!

### Heroku

```bash
heroku create maxalert-ai
heroku addons:create heroku-postgresql:essential-0
heroku config:set SECRET_KEY=... TWILIO_ACCOUNT_SID=... TWILIO_AUTH_TOKEN=... TWILIO_WHATSAPP_NUMBER=...
git push heroku main
heroku run flask db upgrade
```

### Docker (Self-Hosted)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5001
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]
```

---

## 🔧 Configuration Reference

All configuration is handled in `config.py` via environment variables:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | ✅ | `dev-key-...` | Flask session signing key |
| `DATABASE_URL` | ✅ | `sqlite:///site.db` | DB connection string |
| `TWILIO_ACCOUNT_SID` | For WhatsApp | — | Twilio account identifier |
| `TWILIO_AUTH_TOKEN` | For WhatsApp | — | Twilio secret token |
| `TWILIO_WHATSAPP_NUMBER` | For WhatsApp | — | Format: `whatsapp:+1415...` |
| `BASE_URL` | For media | — | Public URL for photo attachments in WhatsApp |
| `FIREBASE_SERVER_KEY` | Optional | — | For Firebase push notifications |

**Upload limits:** Max file size 16 MB. Allowed extensions: `png jpg jpeg gif mp4 mov avi`.

---

## 🔐 Security Notes

- Passwords are hashed using **Werkzeug's `generate_password_hash`** (PBKDF2-HMAC-SHA256).
- All form submissions are protected by **CSRF tokens** (Flask-WTF).
- Role-based access control is enforced on every sensitive endpoint via `@login_required` + role checks.
- File uploads are sanitised using `werkzeug.utils.secure_filename` and validated by extension allowlist.
- Twilio webhook authenticity can be validated using Twilio's request signature (recommended for production).

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-new-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/my-new-feature`
5. Open a Pull Request.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

**Built with ❤️ to protect India's coastal communities**

*"Every minute in a disaster matters. Sentinel AI makes minutes into seconds."*

[⭐ Star this repo](https://github.com/varunmax7/sentinelai) if you find it useful!

</div>
