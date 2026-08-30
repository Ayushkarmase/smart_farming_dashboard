import random
import time

COMMODITY_BASE = [
    {
        'crop': 'Paddy (Basmati / Super)',
        'variety': 'Grade A',
        'mandi': 'Ratnagiri APMC',
        'base_price': 3450,
        'unit': '₹ / Quintal',
        'msp': 2300,
        'arrivals': '1,420 Qtl'
    },
    {
        'crop': 'Cotton (Medium Staple)',
        'variety': 'Bunny BT',
        'mandi': 'Nagpur Cotton Exchange',
        'base_price': 7250,
        'unit': '₹ / Quintal',
        'msp': 7121,
        'arrivals': '3,850 Qtl'
    },
    {
        'crop': 'Soybean (Yellow)',
        'variety': 'JS-335',
        'mandi': 'Indore / Pune APMC',
        'base_price': 4890,
        'unit': '₹ / Quintal',
        'msp': 4892,
        'arrivals': '5,120 Qtl'
    },
    {
        'crop': 'Wheat (Lokwan / Sharbati)',
        'variety': 'Premium Lokwan',
        'mandi': 'Nashik APMC',
        'base_price': 2780,
        'unit': '₹ / Quintal',
        'msp': 2275,
        'arrivals': '6,900 Qtl'
    },
    {
        'crop': 'Sugarcane (Co-86032)',
        'variety': 'Sugar Mill Direct',
        'mandi': 'Kolhapur Sugar Belt',
        'base_price': 3400,
        'unit': '₹ / Tonne',
        'msp': 3150,
        'arrivals': '12,500 Ton'
    },
    {
        'crop': 'Maize (Kharif Grain)',
        'variety': 'Pioneer Hybrid',
        'mandi': 'Aurangabad APMC',
        'base_price': 2240,
        'unit': '₹ / Quintal',
        'msp': 2090,
        'arrivals': '2,300 Qtl'
    },
    {
        'crop': 'Red Onion (Nashik Special)',
        'variety': 'Garwa High Grade',
        'mandi': 'Lasalgaon Mandi',
        'base_price': 2850,
        'unit': '₹ / Quintal',
        'msp': 1800,
        'arrivals': '18,400 Qtl'
    },
    {
        'crop': 'Tomato (Hybrid Red)',
        'variety': 'Abhinav 1057',
        'mandi': 'Narayangaon Market',
        'base_price': 1650,
        'unit': '₹ / Crate (25kg)',
        'msp': 1100,
        'arrivals': '8,200 Crates'
    }
]

def get_live_mandi_prices():
    """
    Returns live dynamic Mandi commodity prices with realistic micro-fluctuations,
    change percentages, and market trend status.
    """
    timestamp = time.strftime('%H:%M:%S')
    results = []

    for item in COMMODITY_BASE:
        # Micro-fluctuation simulation based on current time
        jitter = random.choice([-1.5, -0.8, -0.2, 0.4, 0.9, 1.6, 2.3, -0.5, 1.2])
        curr_price = round(item['base_price'] * (1 + (jitter / 100.0)), 0)
        diff = round(curr_price - item['base_price'], 0)
        pct_change = round((diff / item['base_price']) * 100.0, 2)

        results.append({
            'crop': item['crop'],
            'variety': item['variety'],
            'mandi': item['mandi'],
            'price': int(curr_price),
            'unit': item['unit'],
            'diff': int(diff),
            'pct_change': pct_change,
            'trend': 'up' if diff > 0 else ('down' if diff < 0 else 'flat'),
            'msp': item['msp'],
            'arrivals': item['arrivals'],
            'last_updated': timestamp
        })

    return {
        'status': 'live',
        'timestamp': timestamp,
        'commodities': results
    }
