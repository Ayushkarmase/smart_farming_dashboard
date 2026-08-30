from flask import Blueprint, render_template, session, jsonify, request
from blueprints.auth import login_required
from database.db_init import get_db_connection
from services.weather_service import get_live_weather, CITIES_COORDS
from services.mandi_service import get_live_mandi_prices
from services.iot_sensor_service import get_live_sensor_telemetry

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    user_id = session.get('user_id')
    user_role = session.get('user_role')

    conn = get_db_connection()

    # User statistics
    total_recs = conn.execute('SELECT COUNT(*) FROM fertilizer_history WHERE user_id = ?', (user_id,)).fetchone()[0]
    total_forecasts = conn.execute('SELECT COUNT(*) FROM forecast_history WHERE user_id = ?', (user_id,)).fetchone()[0]
    total_news = conn.execute('SELECT COUNT(*) FROM news_articles').fetchone()[0]

    # Recent recommendations
    recent_recs = conn.execute("""
        SELECT * FROM fertilizer_history 
        WHERE user_id = ? 
        ORDER BY created_at DESC LIMIT 3
    """, (user_id,)).fetchall()

    # Recent forecasts
    recent_forecasts = conn.execute("""
        SELECT * FROM forecast_history 
        WHERE user_id = ? 
        ORDER BY created_at DESC LIMIT 2
    """, (user_id,)).fetchall()

    # Notifications
    notifications = conn.execute("""
        SELECT * FROM notifications 
        ORDER BY created_at DESC LIMIT 4
    """).fetchall()

    # News previews
    recent_news = conn.execute("""
        SELECT * FROM news_articles 
        ORDER BY created_at DESC LIMIT 3
    """).fetchall()

    conn.close()

    # Initial live telemetry snapshot
    default_weather = get_live_weather(16.9902, 73.3120, "Ratnagiri")
    mandi_data = get_live_mandi_prices()
    sensor_data = get_live_sensor_telemetry()

    return render_template(
        'dashboard/index.html',
        total_recs=total_recs,
        total_forecasts=total_forecasts,
        total_news=total_news,
        recent_recs=recent_recs,
        recent_forecasts=recent_forecasts,
        notifications=notifications,
        recent_news=recent_news,
        weather=default_weather,
        mandi=mandi_data,
        sensors=sensor_data,
        cities=list(CITIES_COORDS.keys())
    )

# --- Real-Time Live API Endpoints ---

@dashboard_bp.route('/api/live-weather')
def api_live_weather():
    city = request.args.get('city', 'Ratnagiri')
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if lat and lon:
        try:
            weather = get_live_weather(float(lat), float(lon), city_name=city or "GPS Location")
            return jsonify(weather)
        except Exception:
            pass

    coords = CITIES_COORDS.get(city, CITIES_COORDS['Ratnagiri'])
    weather = get_live_weather(coords['lat'], coords['lon'], city_name=city)
    return jsonify(weather)

@dashboard_bp.route('/api/live-mandi')
def api_live_mandi():
    return jsonify(get_live_mandi_prices())

@dashboard_bp.route('/api/live-sensors')
def api_live_sensors():
    return jsonify(get_live_sensor_telemetry())
