from flask import Blueprint, render_template, request, jsonify, session, Response
from blueprints.auth import login_required
from models.forecast_model import generate_forecast, PRODUCT_BASELINES
from database.db_init import get_db_connection
import json
import csv
import io

forecasting_bp = Blueprint('forecasting', __name__, url_prefix='/forecasting')

@forecasting_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    products = list(PRODUCT_BASELINES.keys())
    selected_product = request.args.get('product', products[0])
    horizon = int(request.args.get('horizon', 6))

    if request.method == 'POST':
        selected_product = request.form.get('product_type', products[0])
        horizon = int(request.form.get('horizon_months', 6))

    forecast_result = generate_forecast(selected_product, horizon_months=horizon)

    # Save to history if generated via POST
    if request.method == 'POST':
        user_id = session.get('user_id')
        conn = get_db_connection()
        conn.execute("""
            INSERT INTO forecast_history (
                user_id, product_type, duration_months, total_projected_demand,
                avg_growth_rate, forecast_data_json
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            selected_product,
            horizon,
            forecast_result['total_projected_demand'],
            forecast_result['avg_growth_rate'],
            json.dumps(forecast_result)
        ))
        conn.commit()
        conn.close()

    return render_template(
        'forecasting/index.html',
        products=products,
        selected_product=selected_product,
        selected_horizon=horizon,
        forecast=forecast_result
    )

@forecasting_bp.route('/export-csv')
@login_required
def export_csv():
    product = request.args.get('product', 'Urea (46% Nitrogen)')
    horizon = int(request.args.get('horizon', 6))
    
    forecast_data = generate_forecast(product, horizon_months=horizon)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Fritz-Haber Agritech - Demand & Sales Forecasting Report'])
    writer.writerow(['Product', product])
    writer.writerow(['Horizon', f"{horizon} Months"])
    writer.writerow(['Total Projected Demand (MT)', forecast_data['total_projected_demand']])
    writer.writerow(['Projected Growth Rate', f"{forecast_data['avg_growth_rate']}%"])
    writer.writerow(['Model Accuracy Metrics', f"MAE: {forecast_data['metrics']['mae']}, RMSE: {forecast_data['metrics']['rmse']}, R2 Score: {forecast_data['metrics']['r2_score']}"])
    writer.writerow([])
    writer.writerow(['Month', 'Projected Demand (MT)', 'Lower Confidence Limit (MT)', 'Upper Confidence Limit (MT)', 'Estimated Turnover'])

    for row in forecast_data['breakdown_table']:
        writer.writerow([row['month'], row['forecast_tonnes'], row['range_min'], row['range_max'], row['expected_turnover']])

    output.seek(0)
    filename = f"forecast_{product.replace(' ', '_')}_{horizon}M.csv"

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename={filename}"}
    )
