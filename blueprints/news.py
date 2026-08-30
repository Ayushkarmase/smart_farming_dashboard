from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from blueprints.auth import login_required
from models.sentiment_model import analyze_sentiment
from database.db_init import get_db_connection

news_bp = Blueprint('news', __name__, url_prefix='/news')

@news_bp.route('/')
@login_required
def index():
    category = request.args.get('category', 'all')
    sentiment = request.args.get('sentiment', 'all')
    search = request.args.get('q', '').strip()

    conn = get_db_connection()
    query = "SELECT * FROM news_articles WHERE 1=1"
    params = []

    if category != 'all':
        query += " AND category = ?"
        params.append(category)

    if sentiment != 'all':
        query += " AND sentiment = ?"
        params.append(sentiment)

    if search:
        query += " AND (title LIKE ? OR summary LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    query += " ORDER BY published_date DESC, id DESC"
    articles = conn.execute(query, params).fetchall()

    # Get distinct categories for filter buttons
    categories = [row[0] for row in conn.execute("SELECT DISTINCT category FROM news_articles").fetchall()]
    
    # Sentiment breakdown stats
    total_count = conn.execute("SELECT COUNT(*) FROM news_articles").fetchone()[0]
    pos_count = conn.execute("SELECT COUNT(*) FROM news_articles WHERE sentiment = 'Positive'").fetchone()[0]
    neu_count = conn.execute("SELECT COUNT(*) FROM news_articles WHERE sentiment = 'Neutral'").fetchone()[0]
    neg_count = conn.execute("SELECT COUNT(*) FROM news_articles WHERE sentiment = 'Negative'").fetchone()[0]
    
    conn.close()

    return render_template(
        'news/index.html',
        articles=articles,
        categories=categories,
        selected_category=category,
        selected_sentiment=sentiment,
        search_query=search,
        stats={
            'total': total_count,
            'positive': pos_count,
            'neutral': neu_count,
            'negative': neg_count
        }
    )

@news_bp.route('/analyze-live', methods=['POST'])
@login_required
def analyze_live():
    """Live interactive sentiment analysis API endpoint"""
    data = request.get_json() or {}
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'Please provide text to analyze'}), 400
    
    result = analyze_sentiment(text)
    return jsonify(result)

@news_bp.route('/add', methods=['POST'])
@login_required
def add_article():
    if session.get('user_role') != 'admin':
        flash('Only administrators can publish news articles.', 'danger')
        return redirect(url_for('news.index'))

    title = request.form.get('title', '').strip()
    summary = request.form.get('summary', '').strip()
    category = request.form.get('category', 'Market')
    source = request.form.get('source', 'Fritz-Haber Agritech Desk')
    pub_date = request.form.get('published_date', '')

    if not title or not summary:
        flash('Title and Summary are required.', 'warning')
        return redirect(url_for('news.index'))

    # Run AI sentiment classification automatically
    ai_result = analyze_sentiment(title, summary)

    conn = get_db_connection()
    conn.execute("""
        INSERT INTO news_articles (title, summary, category, sentiment, sentiment_score, source, published_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, summary, category, ai_result['sentiment'], ai_result['score'], source, pub_date or 'Today'))
    conn.commit()
    conn.close()

    flash(f"Article published! AI classified sentiment as: {ai_result['sentiment']} ({ai_result['score']:+.2f})", 'success')
    return redirect(url_for('news.index'))
