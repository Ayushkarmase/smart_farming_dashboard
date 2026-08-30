-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user', -- 'admin' or 'user'
    status TEXT NOT NULL DEFAULT 'active', -- 'active' or 'inactive'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Fertilizer recommendations history
CREATE TABLE IF NOT EXISTS fertilizer_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    soil_type TEXT NOT NULL,
    crop_type TEXT NOT NULL,
    nitrogen REAL NOT NULL,
    phosphorus REAL NOT NULL,
    potassium REAL NOT NULL,
    ph REAL DEFAULT 6.5,
    rainfall REAL,
    temperature REAL,
    humidity REAL,
    recommended_fertilizer TEXT NOT NULL,
    dosage_kg_per_acre REAL,
    timing_schedule TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Forecast history
CREATE TABLE IF NOT EXISTS forecast_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    product_type TEXT NOT NULL,
    duration_months INTEGER NOT NULL,
    total_projected_demand REAL NOT NULL,
    avg_growth_rate REAL NOT NULL,
    forecast_data_json TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- News articles cache
CREATE TABLE IF NOT EXISTS news_articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    category TEXT NOT NULL,
    sentiment TEXT NOT NULL, -- 'Positive', 'Neutral', 'Negative'
    sentiment_score REAL NOT NULL,
    source TEXT NOT NULL,
    published_date TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Announcements / Notifications
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    type TEXT NOT NULL DEFAULT 'info', -- 'info', 'success', 'warning', 'danger'
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(created_by) REFERENCES users(id)
);
