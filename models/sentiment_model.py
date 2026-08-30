import re

POSITIVE_AGRI_KEYWORDS = {
    'record', 'surge', 'boom', 'subsidy', 'favorable', 'bumper', 'growth', 'profit', 'yield',
    'increase', 'support', 'advance', 'benefit', 'breakthrough', 'high', 'boost', 'innovation',
    'relief', 'plentiful', 'normal', 'good', 'success', 'gain', 'opportunity', 'rise', 'improved',
    'incentive', 'thrive', 'flourish', 'robust', 'abundant', 'stable', 'uptick', 'milestone'
}

NEGATIVE_AGRI_KEYWORDS = {
    'drought', 'pest', 'loss', 'crisis', 'decline', 'drop', 'inflation', 'deficit', 'infestation',
    'damage', 'fall', 'shortage', 'struggle', 'flood', 'adverse', 'hike', 'slash', 'cut', 'slump',
    'risk', 'delay', 'low', 'threat', 'disease', 'blight', 'decay', 'failure', 'poor', 'curtail',
    'warning', 'scarcity', 'escalate', 'penalty', 'strain'
}

def clean_text(text):
    if not text:
        return ""
    # Lowercase & remove non-alphanumeric
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    return text.strip()

def analyze_sentiment(title, content=""):
    """
    Performs NLP sentiment classification on agricultural news headlines and text summaries.
    Returns:
      sentiment: 'Positive' | 'Neutral' | 'Negative'
      score: float between -1.0 and 1.0
      confidence: percentage integer (e.g. 85%)
    """
    combined = clean_text(f"{title} {content}")
    words = combined.split()
    
    if not words:
        return {'sentiment': 'Neutral', 'score': 0.0, 'confidence': 50}

    pos_hits = sum(1 for w in words if w in POSITIVE_AGRI_KEYWORDS)
    neg_hits = sum(1 for w in words if w in NEGATIVE_AGRI_KEYWORDS)

    total_relevant = pos_hits + neg_hits

    if total_relevant == 0:
        return {'sentiment': 'Neutral', 'score': 0.0, 'confidence': 60}

    raw_score = (pos_hits - neg_hits) / max(1, total_relevant)
    # Scale score smoothly
    score = round(max(-1.0, min(1.0, raw_score * 0.9)), 2)

    if score >= 0.2:
        sentiment = 'Positive'
        confidence = int(min(98, 65 + (score * 35)))
    elif score <= -0.2:
        sentiment = 'Negative'
        confidence = int(min(98, 65 + (abs(score) * 35)))
    else:
        sentiment = 'Neutral'
        confidence = int(max(60, 85 - (abs(score) * 40)))

    return {
        'sentiment': sentiment,
        'score': score,
        'confidence': confidence,
        'keyword_metrics': {
            'positive_terms': pos_hits,
            'negative_terms': neg_hits
        }
    }
