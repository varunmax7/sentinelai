# 🌊 CoastalAlert - Disaster Management & Environmental Protection Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3.5-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A comprehensive crowdsourced hazard reporting and environmental tracking platform focused on coastal community safety and sustainability.**

[Features](#-features) • [Tech Stack](#%EF%B8%8F-tech-stack) • [Installation](#-installation) • [Impact](#-project-impact) • [Screenshots](#-screenshots)

</div>

---

## 📖 Overview

**CoastalAlert** is an innovative disaster management platform designed to protect coastal communities through crowdsourced hazard reporting, real-time alerts, AI-powered analysis, and environmental sustainability tracking. The platform empowers citizens, officials, and analysts to collaborate in identifying, verifying, and responding to coastal hazards while promoting eco-friendly practices.

---

## ✨ Features

### 🚨 Hazard Reporting & Alert System
- **Crowdsourced Hazard Reports**: Users can report various coastal hazards (tsunamis, storm surges, high waves, coastal flooding, abnormal tides)
- **AI-Powered Analysis**: Automatic confidence scoring and credibility analysis of reports
- **Location-Based Alerts**: GPS-based hazard alerts with configurable radius for each hazard type
- **Real-Time Notifications**: Push notifications and in-app alerts for users in danger zones
- **Media Support**: Photo and video evidence upload (supports PNG, JPG, GIF, MP4, MOV, AVI)

### 🗺️ Interactive Dashboard & Maps
- **Real-Time Hazard Map**: Interactive map showing all reported hazards with filtering options
- **Status Tracking**: Pending, verified, and rejected report management
- **Analytics Dashboard**: Charts and graphs for hazard distribution, timeline analysis, and user engagement

### 👥 User Management & Gamification
- **Multi-Role Support**: Citizens, Officials, and Analysts with different permissions
- **Points & Rewards System**: Earn points for reporting hazards and eco-activities
- **Badge Achievement System**: Unlock badges based on activity and contributions
- **Leaderboard**: Community rankings based on contributions and eco activities
- **Social Features**: Follow/unfollow users, likes, comments, and sharing

### 🌐 Multilingual Support
- **6 Languages**: English, Tamil (தமிழ்), Hindi (हिंदी), Telugu (తెలుగు), Malayalam (മലയാളം), Kannada (ಕನ್ನಡ)
- **Automatic Language Detection**: Based on geographic location
- **User Language Preference**: Set and save preferred language

### ♻️ Eco Tracker - Environmental Sustainability
- **Plastic Reduction Tracking**: Log and verify plastic reduction activities with photo proof
- **Carbon Savings Calculator**: Track carbon footprint reduction from various activities
- **AI Image Verification**: Automatic verification of eco-activity evidence
- **Environmental Impact Metrics**: Trees equivalent, car miles saved, energy savings
- **Eco Leaderboard**: Separate rankings for environmental contributions


### 🏛️ Government-NGO Coordination Platform
- **Unified Command Center**: Dashboard for coordinating disaster response
- **Agency Management**: Register and manage government agencies and NGOs
- **Emergency Event Tracking**: Create and manage emergency events
- **Resource Allocation**: Track and allocate resources across agencies
- **Volunteer Management**: Skill-based volunteer matching and assignment
- **Situation Reports**: Real-time situation reporting during emergencies

### 📱 Instagram-Style Reels View
- **Engaging Content Format**: Swipeable reel-style viewing of hazard reports
- **Social Interactions**: Like, comment, and share reports
- **Media-Rich Experience**: View photos and videos in immersive format

---

## 🛠️ Tech Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.9+ | Primary programming language |
| **Flask** | 2.3.5 | Web framework |
| **Flask-SQLAlchemy** | 3.0.4 | ORM for database operations |
| **Flask-Login** | 0.6.3 | User session management |
| **Flask-WTF** | 1.1.1 | Form handling and validation |
| **Flask-Migrate** | 4.0.4 | Database migrations |
| **Werkzeug** | 2.3.8 | WSGI utilities and security |
| **APScheduler** | 3.10.5 | Background task scheduling |

### Data Analysis & AI
| Technology | Version | Purpose |
|------------|---------|---------|
| **NumPy** | 1.27.5 | Numerical computations |
| **Matplotlib** | 3.8.0 | Chart and graph generation |
| **TextBlob** | 0.18.0 | Text analysis and sentiment detection |
| **NLTK** | 3.8.1 | Natural language processing |
| **Pillow** | 10.0.0 | Image processing |

### External Services
| Technology | Purpose |
|------------|---------|
| **Requests** | 2.31.0 | API calls for weather data |
| **python-dotenv** | 1.0.0 | Environment variable management |
| **Cloudflare Tunnel** | Secure external access |

### Database
| Technology | Purpose |
|------------|---------|
| **SQLite** | Development database |
| **SQLAlchemy ORM** | Database abstraction layer |

### Frontend
| Technology | Purpose |
|------------|---------|
| **HTML5/CSS3** | Page structure and styling |
| **JavaScript** | Interactive features |
| **Jinja2** | Server-side templating |
| **Leaflet.js** | Interactive maps |
| **Chart.js** | Data visualization |

---

## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/disaster_management.git
   cd disaster_management
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables** (optional)
   ```bash
   # Create a .env file
   echo "SECRET_KEY=your-secret-key-here" > .env
   echo "DATABASE_URL=sqlite:///site.db" >> .env
   ```

5. **Initialize the database**
   ```bash
   flask db upgrade
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

---

## 🌍 Project Impact

### 🎯 Problem Statement
Coastal communities face increasing threats from natural hazards like tsunamis, storm surges, and coastal flooding. Traditional warning systems often fail to provide timely, localized alerts, leaving communities vulnerable. Additionally, environmental degradation continues to accelerate due to plastic pollution and carbon emissions.

### 💡 Solution
CoastalAlert addresses these challenges through:

#### 1. **Community-Powered Early Warning**
- Real-time crowdsourced hazard reporting enables faster response times
- AI-powered verification ensures accuracy while maintaining speed
- Location-based alerts reach only those in danger zones, reducing alert fatigue

#### 2. **Democratized Safety Information**
- Multilingual support ensures accessibility for diverse coastal communities
- Mobile-responsive design works on any device
- Simple, intuitive reporting interface enables participation from all age groups

#### 3. **Environmental Sustainability**
- Gamified eco-tracking encourages sustainable behaviors
- Visual impact metrics make environmental contributions tangible
- Community leaderboards foster healthy competition for sustainability

#### 4. **Improved Disaster Coordination**
- Unified platform for government agencies and NGOs
- Real-time resource tracking prevents duplication of efforts
- Skill-based volunteer matching ensures effective deployment

### 📊 Potential Impact Metrics

| Metric | Potential Impact |
|--------|-----------------|
| **Response Time** | Up to 70% faster hazard detection through crowdsourcing |
| **Alert Accuracy** | 90%+ precision through AI verification and corroboration |
| **Community Reach** | 6 languages covering 500M+ potential users in coastal India |
| **Environmental** | Track and reduce plastic consumption at individual and community levels |
| **Coordination** | Centralized platform reducing response fragmentation |

### 🏆 Key Benefits

- **For Citizens**: Real-time safety alerts, community engagement, eco-rewards
- **For Officials**: Verified reports, analytics dashboard, early warning capabilities
- **For Analysts**: Data visualization, trend analysis, weather integration
- **For NGOs**: Volunteer coordination, resource management, situation awareness
- **For Environment**: Plastic reduction tracking, carbon footprint monitoring, sustainability promotion

---

## 📸 Screenshots

*Screenshots would be added here showing:*
- Dashboard with hazard map
- Report submission form
- Eco tracker dashboard
- Coordination platform
- Leaderboard

---

## 📁 Project Structure

```
disaster_management/
├── app.py              # Main Flask application (3000+ lines)
├── models.py           # SQLAlchemy database models
├── forms.py            # WTForms form definitions
├── config.py           # Application configuration
├── utils.py            # Utility functions
├── translations.py     # Multilingual translations
├── requirements.txt    # Python dependencies
├── static/             # Static assets (CSS, JS, uploads)
├── templates/          # Jinja2 HTML templates (37 files)
├── migrations/         # Database migration files
└── instance/           # Instance-specific files
```

---

## 🗃️ Database Models

| Model | Description |
|-------|-------------|
| **User** | User accounts with roles, points, location, preferences |
| **Report** | Hazard reports with location, media, verification status |
| **PlasticUsage** | Plastic reduction entries with verification |
| **CarbonSavings** | Carbon saving activities and calculations |
| **Agency** | Government/NGO agency profiles |
| **EmergencyEvent** | Active emergency events |
| **ResourceAllocation** | Resource distribution tracking |
| **Volunteer** | Volunteer profiles and skills |
| **Notification** | User notifications and alerts |
| **Badge** | Achievement badges |
| **Like/Comment** | Social interaction data |

---

## 🔐 User Roles

| Role | Permissions |
|------|-------------|
| **Citizen** | Report hazards, view dashboard, track eco activities |
| **Official** | All citizen permissions + verify/reject reports, manage emergencies |
| **Analyst** | All permissions + advanced analytics, weather data, simulations |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Varun Ramavath**

---

## 🙏 Acknowledgments

- Flask community for the excellent web framework
- OpenStreetMap and Leaflet.js for mapping capabilities
- All contributors and testers who helped improve this platform

---

<div align="center">

**Made with ❤️ for Coastal Community Safety and Environmental Sustainability**

⭐ Star this repository if you find it helpful!

</div>
