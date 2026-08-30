import time
import math
import random

def get_live_sensor_telemetry():
    """
    Simulates real-time IoT node telemetry from field sensors.
    Updates dynamically each second with realistic physical ranges.
    """
    now = time.time()
    
    # Smooth oscillatory mathematical wave with small random physical noise
    base_sine = math.sin(now / 15.0)
    
    moisture = round(52.0 + (base_sine * 8.0) + (random.random() * 1.5), 1)
    soil_temp = round(26.5 + (base_sine * 2.5) + (random.random() * 0.4), 1)
    ph = round(6.5 + (math.cos(now / 20.0) * 0.25) + (random.random() * 0.05), 2)
    ec = round(1.25 + (base_sine * 0.15), 2) # dS/m
    
    nitrogen = round(48.0 + (math.sin(now / 30.0) * 4.0) + random.randint(-1, 1), 1)
    phosphorus = round(24.5 + (math.cos(now / 35.0) * 2.0) + (random.random() * 0.5), 1)
    potassium = round(38.0 + (math.sin(now / 25.0) * 3.0) + random.randint(-1, 1), 1)

    # Health status interpretation
    if moisture < 35.0:
        moisture_status = "Dry - Irrigation Trigger Required"
        moisture_level = "warning"
    elif moisture > 75.0:
        moisture_status = "High Saturation - Risk of Waterlogging"
        moisture_level = "warning"
    else:
        moisture_status = "Optimal Root Zone Moisture"
        moisture_level = "success"

    return {
        'status': 'online',
        'node_id': 'AGRI-IOT-NODE-04',
        'timestamp': time.strftime('%H:%M:%S'),
        'battery_pct': 94,
        'signal_rssi': '-68 dBm (Strong 4G LTE)',
        'sensors': {
            'moisture': {
                'value': moisture,
                'unit': '%',
                'status': moisture_status,
                'level': moisture_level
            },
            'soil_temp': {
                'value': soil_temp,
                'unit': '°C',
                'status': 'Optimal Root Temperature'
            },
            'ph': {
                'value': ph,
                'unit': 'pH',
                'status': 'Neutral Range (Bio-available)'
            },
            'ec': {
                'value': ec,
                'unit': 'dS/m',
                'status': 'Non-Saline Optimal'
            },
            'npk': {
                'n': nitrogen,
                'p': phosphorus,
                'k': potassium,
                'unit': 'mg/kg'
            }
        }
    }
