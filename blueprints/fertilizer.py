from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from blueprints.auth import login_required
from models.fertilizer_model import predict_fertilizer, CROP_NUTRIENT_TARGETS, SOIL_FACTORS
from database.db_init import get_db_connection
from services.weather_service import get_live_weather, CITIES_COORDS

fertilizer_bp = Blueprint('fertilizer', __name__, url_prefix='/fertilizer')

@fertilizer_bp.route('/', methods=['GET', 'POST'])
@login_required
def recommend():
    if request.method == 'POST':
        try:
            soil_type = request.form.get('soil_type', 'Loamy')
            crop_type = request.form.get('crop_type', 'Rice (Paddy)')
            
            n = float(request.form.get('nitrogen', 50))
            p = float(request.form.get('phosphorus', 30))
            k = float(request.form.get('potassium', 40))
            ph = float(request.form.get('ph', 6.5))
            
            temp = float(request.form.get('temperature', 28.0))
            humidity = float(request.form.get('humidity', 70.0))
            rainfall = float(request.form.get('rainfall', 120.0))

            # AI Model Inference
            result = predict_fertilizer(
                crop_type=crop_type,
                soil_type=soil_type,
                n=n,
                p=p,
                k=k,
                ph=ph,
                temp=temp,
                humidity=humidity,
                rainfall=rainfall
            )

            # Save to Database
            user_id = session.get('user_id')
            conn = get_db_connection()
            timing_summary = " | ".join([f"{s['stage']}: {s['details']}" for s in result['application_stages']])
            
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO fertilizer_history (
                    user_id, soil_type, crop_type, nitrogen, phosphorus, potassium, ph,
                    rainfall, temperature, humidity, recommended_fertilizer, dosage_kg_per_acre,
                    timing_schedule, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id, soil_type, crop_type, n, p, k, ph,
                rainfall, temp, humidity, result['primary_fertilizer'], result['dosage_kg_per_acre'],
                timing_summary, result['explanation']
            ))
            conn.commit()
            record_id = cursor.lastrowid
            conn.close()

            flash('AI Fertilizer Recommendation successfully computed and saved to history!', 'success')
            return render_template('fertilizer/result.html', result=result, n=n, p=p, k=k, ph=ph, temp=temp, humidity=humidity, rainfall=rainfall, record_id=record_id)

        except Exception as e:
            flash(f"Error calculating recommendation: {str(e)}", 'danger')
            return redirect(url_for('fertilizer.recommend'))

    crops = list(CROP_NUTRIENT_TARGETS.keys())
    soils = list(SOIL_FACTORS.keys())
    cities = list(CITIES_COORDS.keys())

    return render_template('fertilizer/form.html', crops=crops, soils=soils, cities=cities)
