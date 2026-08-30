# Smart Farming Dashboard with AI-based Fertilizer Recommendation System
**Internship Project for Fritz-Haber Agritech LLP**  
**Submitted By:** Ayush Rajendra Karmase (PRN: 2230421995519)  
**Guided By:** Dr. S. G. Akojwar  
**Department:** Artificial Intelligence & Data Science, Government College of Engineering, Ratnagiri  
**Affiliation:** Dr. Babasaheb Ambedkar Technological University, Lonere  

---

## 🌟 Overview & Highlights

The **Smart Farming Dashboard** is a full-stack AI-driven web application built during a 12-week industry internship at **Fritz-Haber Agritech LLP**. The platform provides farmers, agronomists, and agricultural distributors with intelligent soil health analysis, scientific fertilizer dosage computation, predictive sales & inventory demand forecasting, natural language sentiment-tagged agri-news intelligence, and full administrative governance.

### Core Modules Implemented
1. **AI Fertilizer Recommendation System (Week 5 & 7)**
   - Custom agronomic decision engine computing optimal N-P-K nutrient balances based on soil test parameters (N, P, K, pH) and environmental factors (Temperature, Humidity, Rainfall).
   - Generates primary fertilizer prescriptions (Urea, DAP, SSP, MOP, 10-26-26, etc.), exact dosage (kg/acre), stage-by-stage split application schedules (Basal, Tillering, Panicle/Flowering), and ecological tips.
2. **Sales & Demand Forecasting Engine (Week 6 & 9)**
   - Linear Regression and time-series seasonality models predicting month-wise fertilizer demand (3, 6, 12 months horizon).
   - Real-time interactive Chart.js trend curves, confidence bounds (95%), model error metrics (MAE, RMSE, R² Score), and one-click CSV report export.
3. **Agri-News Feed with AI Sentiment Analysis (Week 7)**
   - Live agricultural news feed with automated NLP sentiment tone classification (Positive, Neutral, Negative).
   - Category filtering (Market, Weather, Subsidies, Technology, Advisory) and an **Interactive Live Sentiment Classifier** widget.
4. **Role-Based Access Control (RBAC) & Authentication (Week 3 & 4)**
   - Secure authentication with Werkzeug password hashing.
   - Dual roles: `Admin` (User management, status activation/deactivation, broadcast dispatcher) and `User/Farmer`.
5. **Data Audit History & Export (Week 9 & 11)**
   - Full historical logging of all fertilizer recommendations and sales forecast runs in SQLite.
   - Search, crop filter, and CSV data export capabilities.
6. **Informational Modules: "About Us" & "Know More" (Week 8)**
   - Detailed company background, project vision, interactive FAQ accordion, and inquiry form.
   - Curated knowledge center on Fertilizer Classes, Precision Farming (IoT, VRA, Fertigation), and Environmental Sustainability.

---

## 🛠️ Technology Stack

- **Backend:** Python 3.x, Flask (with Modular Blueprints Architecture), Jinja2 Templating
- **Database:** SQLite 3 with relational schema & automated seeder
- **Machine Learning & NLP:** Scikit-Learn (Linear Regression, Error Metrics), NumPy, Pandas, NLTK/Lexicon Sentiment Engine
- **Frontend & Visualization:** Vanilla HTML5, Modern CSS3 with CSS Variables & Glassmorphism, JavaScript (ES6+), Chart.js, FontAwesome 6
- **Security:** Werkzeug cryptographic password hashing, role-based route decorators

---

## 🚀 Quick Start & Installation

### 1. Navigate to Project Directory
```bash
cd "C:\Users\AYUSH\.gemini\antigravity-ide\scratch\smart_farming_dashboard"
```

### 2. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python app.py
```

### 4. Open in Browser
Open your browser and navigate to:  
👉 **`http://127.0.0.1:5000`**

---

## 🔑 Pre-Seeded Demo Accounts

| Role | Email | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **Farmer / User** | `farmer@agritech.com` | `Farmer@123` | Dashboard, AI Fertilizer Recommender, Demand Forecasting, News Sentiment, Personal History, Know More |
| **Administrator** | `admin@agritech.com` | `Admin@123` | All Farmer features + Admin Panel, User Management, Broadcast Dispatcher, Global Audit Logs |

*(You can also register a new account on the registration page at any time).*

---

## 📁 Project Directory Layout

```
smart_farming_dashboard/
├── app.py                     # Flask application factory and server entry point
├── config.py                  # Environment and database configuration
├── requirements.txt           # Python dependency specifications
├── README.md                  # Complete documentation
├── database/
│   ├── schema.sql             # Relational SQLite table definitions
│   ├── db_init.py             # Database creation and seed data loader
│   └── agritech.db            # SQLite database file (auto-generated)
├── models/
│   ├── fertilizer_model.py    # AI agronomic nutrient & fertilizer engine
│   ├── forecast_model.py      # Sales & demand regression forecasting model
│   └── sentiment_model.py     # NLP news sentiment classification engine
├── blueprints/
│   ├── auth.py                # Login, registration, session & RBAC guards
│   ├── dashboard.py           # Dashboard overview metrics & widgets
│   ├── fertilizer.py          # Fertilizer form & AI prescription routes
│   ├── forecasting.py         # Demand forecast computation & CSV export
│   ├── news.py                # News feed & live sentiment classifier API
│   ├── admin.py               # Admin control panel & user management
│   ├── history.py             # Recommendation & forecast history with CSV export
│   └── info.py                # About Us, FAQs, and Know More knowledge center
├── static/
│   ├── css/
│   │   └── style.css          # Custom modern agricultural stylesheet
│   └── js/
│       ├── main.js            # UI interactions, accordions, live NLP tester
│       └── charts.js          # Chart.js time-series & forecast charts
└── templates/
    ├── base.html              # Master layout with responsive sidebar
    ├── auth/
    │   ├── login.html         # Login page with demo credentials
    │   └── register.html      # Registration page
    ├── dashboard/
    │   └── index.html         # User dashboard overview
    ├── fertilizer/
    │   ├── form.html          # Soil & field telemetry input form
    │   └── result.html        # AI Fertilizer prescription report
    ├── forecasting/
    │   └── index.html         # Demand forecasting & interactive chart
    ├── news/
    │   └── index.html         # Agri-News feed with sentiment badges
    ├── admin/
    │   └── index.html         # Admin user management & broadcast panel
    ├── history/
    │   ├── fertilizer_history.html # Fertilizer logs with CSV download
    │   └── forecast_history.html   # Forecast historical runs
    └── info/
        ├── about.html         # About Fritz-Haber Agritech & FAQs
        └── know_more.html     # Precision agronomy knowledge base
```

---

## 🧪 Verification & Testing

To verify all components locally:
1. Run `python database/db_init.py` to confirm database connectivity and data seeding.
2. Run `python -c "from models.fertilizer_model import predict_fertilizer; print(predict_fertilizer('Rice (Paddy)', 'Loamy', 40, 20, 30))"` to verify the recommendation engine.
3. Run `python -c "from models.forecast_model import generate_forecast; print(generate_forecast('Urea (46% Nitrogen)', 6)['metrics'])"` to test the forecasting engine.
4. Run `python -c "from models.sentiment_model import analyze_sentiment; print(analyze_sentiment('Bumper wheat harvest expected with favorable monsoon'))"` to test NLP sentiment classification.
