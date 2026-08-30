from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from blueprints.auth import admin_required
from database.db_init import get_db_connection

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@admin_required
def index():
    conn = get_db_connection()

    # System Metrics
    total_users = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    total_recs = conn.execute('SELECT COUNT(*) FROM fertilizer_history').fetchone()[0]
    total_forecasts = conn.execute('SELECT COUNT(*) FROM forecast_history').fetchone()[0]
    total_news = conn.execute('SELECT COUNT(*) FROM news_articles').fetchone()[0]

    # Users list
    users = conn.execute('SELECT * FROM users ORDER BY created_at DESC').fetchall()

    # Recent System Activity
    recent_recs = conn.execute("""
        SELECT fh.*, u.name as user_name, u.email as user_email 
        FROM fertilizer_history fh
        LEFT JOIN users u ON fh.user_id = u.id
        ORDER BY fh.created_at DESC LIMIT 5
    """).fetchall()

    notifications = conn.execute('SELECT * FROM notifications ORDER BY created_at DESC').fetchall()

    conn.close()

    return render_template(
        'admin/index.html',
        total_users=total_users,
        total_recs=total_recs,
        total_forecasts=total_forecasts,
        total_news=total_news,
        users=users,
        recent_recs=recent_recs,
        notifications=notifications
    )

@admin_bp.route('/user/toggle-status/<int:user_id>', methods=['POST'])
@admin_required
def toggle_user_status(user_id):
    if user_id == session.get('user_id'):
        flash('You cannot change your own account status.', 'warning')
        return redirect(url_for('admin.index'))

    conn = get_db_connection()
    user = conn.execute('SELECT status FROM users WHERE id = ?', (user_id,)).fetchone()
    if user:
        new_status = 'inactive' if user['status'] == 'active' else 'active'
        conn.execute('UPDATE users SET status = ? WHERE id = ?', (new_status, user_id))
        conn.commit()
        flash(f"User status updated to {new_status}.", 'success')
    conn.close()
    return redirect(url_for('admin.index'))

@admin_bp.route('/user/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    if user_id == session.get('user_id'):
        flash('You cannot delete your own admin account.', 'danger')
        return redirect(url_for('admin.index'))

    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    flash('User and related historical logs deleted successfully.', 'info')
    return redirect(url_for('admin.index'))

@admin_bp.route('/notification/create', methods=['POST'])
@admin_required
def create_notification():
    title = request.form.get('title', '').strip()
    message = request.form.get('message', '').strip()
    notif_type = request.form.get('type', 'info')

    if not title or not message:
        flash('Notification title and message cannot be empty.', 'warning')
        return redirect(url_for('admin.index'))

    conn = get_db_connection()
    conn.execute("""
        INSERT INTO notifications (title, message, type, created_by)
        VALUES (?, ?, ?, ?)
    """, (title, message, notif_type, session.get('user_id')))
    conn.commit()
    conn.close()

    flash('Broadcast announcement published to all active dashboards.', 'success')
    return redirect(url_for('admin.index'))

@admin_bp.route('/notification/delete/<int:notif_id>', methods=['POST'])
@admin_required
def delete_notification(notif_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM notifications WHERE id = ?', (notif_id,))
    conn.commit()
    conn.close()
    flash('Notification removed.', 'info')
    return redirect(url_for('admin.index'))
