from flask import Blueprint, render_template, request, session, Response
from blueprints.auth import login_required
from database.db_init import get_db_connection
import csv
import io

history_bp = Blueprint('history', __name__, url_prefix='/history')

@history_bp.route('/fertilizer')
@login_required
def fertilizer_history():
    user_id = session.get('user_id')
    user_role = session.get('user_role')
    search = request.args.get('q', '').strip()
    crop_filter = request.args.get('crop', 'all')

    conn = get_db_connection()
    
    # Admins see all logs; normal users see their own
    if user_role == 'admin':
        query = """
            SELECT fh.*, u.name as user_name, u.email as user_email 
            FROM fertilizer_history fh
            LEFT JOIN users u ON fh.user_id = u.id
            WHERE 1=1
        """
        params = []
    else:
        query = """
            SELECT fh.*, u.name as user_name, u.email as user_email 
            FROM fertilizer_history fh
            LEFT JOIN users u ON fh.user_id = u.id
            WHERE fh.user_id = ?
        """
        params = [user_id]

    if crop_filter != 'all':
        query += " AND fh.crop_type = ?"
        params.append(crop_filter)

    if search:
        query += " AND (fh.soil_type LIKE ? OR fh.recommended_fertilizer LIKE ? OR fh.crop_type LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])

    query += " ORDER BY fh.created_at DESC"
    records = conn.execute(query, params).fetchall()

    # Get distinct crops for filtering
    crops = [row[0] for row in conn.execute("SELECT DISTINCT crop_type FROM fertilizer_history").fetchall()]
    conn.close()

    return render_template(
        'history/fertilizer_history.html',
        records=records,
        crops=crops,
        selected_crop=crop_filter,
        search_query=search
    )

@history_bp.route('/fertilizer/export-csv')
@login_required
def export_fertilizer_csv():
    user_id = session.get('user_id')
    user_role = session.get('user_role')

    conn = get_db_connection()
    if user_role == 'admin':
        records = conn.execute("""
            SELECT fh.*, u.name as user_name, u.email as user_email 
            FROM fertilizer_history fh
            LEFT JOIN users u ON fh.user_id = u.id
            ORDER BY fh.created_at DESC
        """).fetchall()
    else:
        records = conn.execute("""
            SELECT fh.*, u.name as user_name, u.email as user_email 
            FROM fertilizer_history fh
            LEFT JOIN users u ON fh.user_id = u.id
            WHERE fh.user_id = ?
            ORDER BY fh.created_at DESC
        """, (user_id,)).fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        'Log ID', 'User Name', 'User Email', 'Crop', 'Soil Type', 'N (kg/ha)',
        'P (kg/ha)', 'K (kg/ha)', 'Soil pH', 'Temp (°C)', 'Humidity (%)',
        'Rainfall (mm)', 'Recommended Fertilizer', 'Dosage (kg/acre)', 'Timestamp'
    ])

    for r in records:
        writer.writerow([
            r['id'], r['user_name'] or 'Unknown', r['user_email'] or 'N/A',
            r['crop_type'], r['soil_type'], r['nitrogen'], r['phosphorus'], r['potassium'],
            r['ph'], r['temperature'], r['humidity'], r['rainfall'],
            r['recommended_fertilizer'], r['dosage_kg_per_acre'], r['created_at']
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=fertilizer_recommendation_history.csv"}
    )

@history_bp.route('/forecast')
@login_required
def forecast_history():
    user_id = session.get('user_id')
    user_role = session.get('user_role')

    conn = get_db_connection()
    if user_role == 'admin':
        records = conn.execute("""
            SELECT f.*, u.name as user_name, u.email as user_email 
            FROM forecast_history f
            LEFT JOIN users u ON f.user_id = u.id
            ORDER BY f.created_at DESC
        """).fetchall()
    else:
        records = conn.execute("""
            SELECT f.*, u.name as user_name, u.email as user_email 
            FROM forecast_history f
            LEFT JOIN users u ON f.user_id = u.id
            WHERE f.user_id = ?
            ORDER BY f.created_at DESC
        """, (user_id,)).fetchall()
    conn.close()

    return render_template('history/forecast_history.html', records=records)
