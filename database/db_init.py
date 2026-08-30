import sqlite3
import os
import json
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(BASE_DIR, 'database', 'agritech.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'database', 'schema.sql')

def get_db_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    
    cursor = conn.cursor()

    # Seed Admin User if not exists
    cursor.execute("SELECT id FROM users WHERE email = ?", ('admin@agritech.com',))
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO users (name, email, password_hash, role, status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            'Ayush Karmase (Admin)',
            'admin@agritech.com',
            generate_password_hash('Admin@123'),
            'admin',
            'active'
        ))

    # Seed Demo Farmer User if not exists
    cursor.execute("SELECT id FROM users WHERE email = ?", ('farmer@agritech.com',))
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO users (name, email, password_hash, role, status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            'Ramesh Patil (Farmer)',
            'farmer@agritech.com',
            generate_password_hash('Farmer@123'),
            'user',
            'active'
        ))

    # Seed Initial Notifications
    cursor.execute("SELECT COUNT(*) FROM notifications")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO notifications (title, message, type, created_by)
            VALUES 
            ('Kharif Sowing Advisory 2024-25', 'Prepare soil bed with balanced basal NPK application before monsoon onset.', 'success', 1),
            ('Soil Health Card Subsidy Update', 'Subsidized soil testing kits are now available at regional Agritech centers.', 'info', 1),
            ('Fertilizer Price Alert', 'Urea supply stabilized with subsidized rate capping under PM-PRANAM scheme.', 'warning', 1)
        """)

    # Seed Sample News Articles
    cursor.execute("SELECT COUNT(*) FROM news_articles")
    if cursor.fetchone()[0] == 0:
        sample_news = [
            (
                "Government Announces Mega Subsidy for Nano DAP and Bio-fertilizers",
                "The Union Agriculture Ministry has increased incentives for farmers adopting nano-urea and organic fertilizers, boosting soil microbiomes while reducing environmental footprint.",
                "Subsidies",
                "Positive",
                0.88,
                "AgriNews Daily",
                "2024-06-10"
            ),
            (
                "Monsoon Rains Projected Normal Across Maharashtra and Central India",
                "IMD weather models forecast favorable rainfall patterns, encouraging early planting of paddy, cotton, and soybean crops with optimal soil moisture index.",
                "Weather",
                "Positive",
                0.79,
                "Krishi Jagran",
                "2024-06-08"
            ),
            (
                "Pest Outbreak Alert: Fall Armyworm Spotted in Coastal Maize Belts",
                "Agricultural officers urge farmers to employ pheromone traps and targeted neem-based bio-pesticides immediately to avoid crop yield loss.",
                "Advisory",
                "Negative",
                -0.65,
                "Farm Tech Review",
                "2024-06-05"
            ),
            (
                "Fertilizer Supply Chain Stabilizes Across Regional Cooperatives",
                "Buffer stocks of MOP and Single Super Phosphate (SSP) have been deployed across distribution hubs to avoid peak-season shortages.",
                "Market",
                "Neutral",
                0.15,
                "Rural Agro Times",
                "2024-06-02"
            ),
            (
                "AI-Driven Soil Sensor Systems Increase Crop Yield by 28%",
                "Smart farming trials utilizing real-time NPK monitoring and automated fertigation systems report drastic improvements in nutrient use efficiency.",
                "Technology",
                "Positive",
                0.92,
                "Fritz-Haber Agritech Insights",
                "2024-05-28"
            ),
            (
                "Rising Raw Material Costs Impact Non-Subsidized Complex Fertilizers",
                "Global phosphate pricing increases put pressure on import quotas, though government intervention cushions farmer impact.",
                "Market",
                "Negative",
                -0.45,
                "Global Agro Economic Weekly",
                "2024-05-20"
            )
        ]
        cursor.executemany("""
            INSERT INTO news_articles (title, summary, category, sentiment, sentiment_score, source, published_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, sample_news)

    # Seed Sample Recommendation History for Demo
    cursor.execute("SELECT COUNT(*) FROM fertilizer_history")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO fertilizer_history 
            (user_id, soil_type, crop_type, nitrogen, phosphorus, potassium, ph, rainfall, temperature, humidity, recommended_fertilizer, dosage_kg_per_acre, timing_schedule, notes)
            VALUES 
            (2, 'Clayey', 'Paddy (Rice)', 45.0, 22.0, 30.0, 6.4, 210.0, 28.5, 80.0, 'Urea + DAP (Di-Ammonium Phosphate)', 50.0, 'Split into 3 doses: Basal, Tillering, Panicle initiation', 'High nitrogen requirement during tillering phase. Ensure proper standing water level.'),
            (2, 'Loamy', 'Cotton', 70.0, 48.0, 55.0, 6.8, 120.0, 31.0, 65.0, 'NPK 10-26-26 + Micronutrient Zinc', 65.0, '50% Basal at sowing, 50% during squaring phase', 'Soil potassium levels are optimum. Supplement with boron spray during flowering.')
        """)

    # Seed Sample Forecast History
    cursor.execute("SELECT COUNT(*) FROM forecast_history")
    if cursor.fetchone()[0] == 0:
        dummy_chart_data = {
            "months": ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            "actual_past": [120, 135, 140, 110, 95, 150],
            "projected": [165, 180, 195, 160, 145, 210],
            "confidence_lower": [155, 170, 180, 148, 132, 195],
            "confidence_upper": [175, 190, 210, 172, 158, 225]
        }
        cursor.execute("""
            INSERT INTO forecast_history 
            (user_id, product_type, duration_months, total_projected_demand, avg_growth_rate, forecast_data_json)
            VALUES 
            (1, 'Urea 46% N', 6, 1055.0, 12.8, ?)
        """, (json.dumps(dummy_chart_data),))

    conn.commit()
    conn.close()
    print("Database initialized and demo data seeded successfully.")

if __name__ == '__main__':
    init_db()
