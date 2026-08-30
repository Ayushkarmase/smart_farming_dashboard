from flask import Blueprint, render_template, request, flash

info_bp = Blueprint('info', __name__)

@info_bp.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        flash('Thank you for reaching out to Fritz-Haber Agritech! Our agronomy support team will get in touch shortly.', 'success')
    return render_template('info/about.html')

@info_bp.route('/know-more')
def know_more():
    return render_template('info/know_more.html')
