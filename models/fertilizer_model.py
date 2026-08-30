import numpy as np

# Agronomic optimal NPK reference targets per crop (kg/acre)
CROP_NUTRIENT_TARGETS = {
    'Rice (Paddy)': {'N': 100, 'P': 50, 'K': 50, 'ideal_ph': (5.5, 7.0), 'water_req': 'High'},
    'Wheat': {'N': 120, 'P': 60, 'K': 40, 'ideal_ph': (6.0, 7.5), 'water_req': 'Medium'},
    'Cotton': {'N': 120, 'P': 60, 'K': 60, 'ideal_ph': (6.5, 8.0), 'water_req': 'Medium'},
    'Maize (Corn)': {'N': 120, 'P': 60, 'K': 40, 'ideal_ph': (5.8, 7.2), 'water_req': 'Medium'},
    'Sugarcane': {'N': 250, 'P': 100, 'K': 120, 'ideal_ph': (6.0, 7.5), 'water_req': 'High'},
    'Soybean (Pulses)': {'N': 30, 'P': 60, 'K': 40, 'ideal_ph': (6.0, 7.0), 'water_req': 'Medium'},
    'Groundnut / Oilseeds': {'N': 25, 'P': 50, 'K': 75, 'ideal_ph': (6.0, 6.8), 'water_req': 'Medium'},
    'Tomato / Vegetables': {'N': 100, 'P': 80, 'K': 100, 'ideal_ph': (6.0, 7.0), 'water_req': 'High'},
    'Potato / Tuber Crops': {'N': 150, 'P': 100, 'K': 150, 'ideal_ph': (5.2, 6.5), 'water_req': 'High'},
    'Banana / Fruit Orchards': {'N': 200, 'P': 70, 'K': 300, 'ideal_ph': (6.0, 7.5), 'water_req': 'High'},
    'Millets / Jowar / Bajra': {'N': 60, 'P': 30, 'K': 30, 'ideal_ph': (6.0, 7.5), 'water_req': 'Low'}
}

# Soil type nutrient retention and correction factors
SOIL_FACTORS = {
    'Sandy': {'leaching_risk': 'High', 'retention': 'Low', 'recommended_dosage_adj': 1.15},
    'Loamy': {'leaching_risk': 'Medium', 'retention': 'High', 'recommended_dosage_adj': 1.0},
    'Clayey': {'leaching_risk': 'Low', 'retention': 'Very High', 'recommended_dosage_adj': 0.9},
    'Black Soil (Regur)': {'leaching_risk': 'Low', 'retention': 'High', 'recommended_dosage_adj': 0.95},
    'Red Soil': {'leaching_risk': 'Medium', 'retention': 'Medium', 'recommended_dosage_adj': 1.05},
    'Alluvial Soil': {'leaching_risk': 'Medium', 'retention': 'High', 'recommended_dosage_adj': 1.0}
}

def predict_fertilizer(crop_type, soil_type, n, p, k, ph=6.5, temp=28.0, humidity=70.0, rainfall=100.0):
    """
    AI-driven Agro-Intelligence Recommendation System
    Evaluates soil nutrient deficit against crop-specific agronomic targets,
    adjusts for soil physics and climate factors, and yields prescriptive fertilizer blend, dosage,
    and application schedule.
    """
    crop_profile = CROP_NUTRIENT_TARGETS.get(crop_type, CROP_NUTRIENT_TARGETS['Rice (Paddy)'])
    soil_profile = SOIL_FACTORS.get(soil_type, SOIL_FACTORS['Loamy'])

    target_n = crop_profile['N']
    target_p = crop_profile['P']
    target_k = crop_profile['K']

    diff_n = target_n - n
    diff_p = target_p - p
    diff_k = target_k - k

    # Nutrient Status Assessment
    status_n = 'Deficient' if diff_n > 15 else ('Optimal' if abs(diff_n) <= 15 else 'Excess')
    status_p = 'Deficient' if diff_p > 10 else ('Optimal' if abs(diff_p) <= 10 else 'Excess')
    status_k = 'Deficient' if diff_k > 10 else ('Optimal' if abs(diff_k) <= 10 else 'Excess')

    # Recommendation Selection Logic
    rec_list = []
    primary_fertilizer = ""
    dosage_kg = 50.0

    if diff_n > 20 and diff_p > 15 and diff_k > 15:
        primary_fertilizer = "NPK 19:19:19 (Complex Fertilizer) + Organic Compost"
        dosage_kg = max(50.0, (diff_n + diff_p + diff_k) * 0.45 * soil_profile['recommended_dosage_adj'])
        explanation = "Balanced multi-nutrient deficit detected. A balanced NPK complex will rapidly restore fundamental soil fertility."
    elif diff_n > 20 and diff_p > 20:
        primary_fertilizer = "DAP (Di-Ammonium Phosphate 18:46:0) + Urea Top-Dressing"
        dosage_kg = max(45.0, (diff_p * 2.1) * soil_profile['recommended_dosage_adj'])
        explanation = "High requirement of Nitrogen and Phosphorus. DAP supplies immediate plant-available orthophosphate along with ammoniacal nitrogen."
    elif diff_p > 20 and diff_k > 15:
        primary_fertilizer = "NPK 10:26:26 + Single Super Phosphate (SSP)"
        dosage_kg = max(55.0, (diff_p * 1.8) * soil_profile['recommended_dosage_adj'])
        explanation = "Crucial Phosphorus and Potassium deficit. Essential for robust root architecture and disease resistance."
    elif diff_n > 25:
        primary_fertilizer = "Neem Coated Urea (46% N) with Split Application"
        dosage_kg = max(40.0, (diff_n * 1.6) * soil_profile['recommended_dosage_adj'])
        explanation = "Severe Nitrogen deficit detected. Urea with neem coating slows nitrogen release, preventing leaching and ammonia volatilization."
    elif diff_p > 20:
        primary_fertilizer = "SSP (Single Super Phosphate 16% P2O5 + 11% Sulphur)"
        dosage_kg = max(60.0, (diff_p * 2.5) * soil_profile['recommended_dosage_adj'])
        explanation = "Phosphorus deficit. SSP provides high water-soluble phosphate plus essential sulphur for chlorophyll development."
    elif diff_k > 20:
        primary_fertilizer = "MOP (Muriate of Potash 60% K2O)"
        dosage_kg = max(35.0, (diff_k * 1.4) * soil_profile['recommended_dosage_adj'])
        explanation = "Potassium deficiency. MOP enhances drought tolerance, stalk strength, and grain/fruit weight."
    else:
        primary_fertilizer = "Bio-Fertilizer (Azotobacter / PSB) + Farmyard Manure (FYM)"
        dosage_kg = 25.0
        explanation = "Soil macro-nutrients are at near-optimal balance. Organic bio-stimulants will preserve microbial soil health and maintain yield equilibrium."

    dosage_kg = round(dosage_kg, 1)

    # pH Condition Analysis
    min_ph, max_ph = crop_profile['ideal_ph']
    ph_advice = "Optimal for nutrient uptake."
    if ph < min_ph:
        ph_advice = f"Soil is acidic (pH {ph} < {min_ph}). Consider applying agricultural lime (calcium carbonate) at 100-150 kg/acre."
    elif ph > max_ph:
        ph_advice = f"Soil is alkaline (pH {ph} > {max_ph}). Apply gypsum (calcium sulphate) or elemental sulphur to facilitate micro-nutrient availability."

    # Stage-wise application schedule
    application_stages = [
        {"stage": "Basal Application (At Sowing / Transplanting)", "share": "40% - 50%", "details": "Apply all Phosphorus (DAP/SSP) and Potash (MOP) along with 30% of total Nitrogen."},
        {"stage": "Vegetative Growth (25-35 Days after sowing)", "share": "25% - 30%", "details": "Top-dress with Neem Coated Urea during active tillering or branching."},
        {"stage": "Flowering / Grain Formation (45-60 Days)", "share": "20% - 25%", "details": "Foliar spray of 1% NPK 13:0:45 or 0:52:34 for enhanced grain filling and fruit size."}
    ]

    eco_tips = [
        "Incorporate organic compost or green manure to boost water holding capacity.",
        "Perform foliar nutrient sprays in the early morning or late afternoon to maximize leaf stomatal absorption.",
        "Maintain optimal soil moisture before fertilizer top-dressing to prevent root scorching.",
        "Use bio-fertilizers such as Rhizobium or Mycorrhiza to unlock fixed soil phosphorus."
    ]

    return {
        'crop_type': crop_type,
        'soil_type': soil_type,
        'primary_fertilizer': primary_fertilizer,
        'dosage_kg_per_acre': dosage_kg,
        'explanation': explanation,
        'nutrients_status': {
            'N': {'current': n, 'target': target_n, 'status': status_n, 'diff': diff_n},
            'P': {'current': p, 'target': target_p, 'status': status_p, 'diff': diff_p},
            'K': {'current': k, 'target': target_k, 'status': status_k, 'diff': diff_k}
        },
        'ph_assessment': ph_advice,
        'application_stages': application_stages,
        'eco_tips': eco_tips
    }
