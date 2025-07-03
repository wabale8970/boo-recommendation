from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required
from flask_mail import Message
from app import mail
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('main/index.html')

@main_bp.route('/about')
def about():
    return render_template('main/about.html')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message_text = request.form.get('message')
        
        # Validate form inputs
        if not all([name, email, subject, message_text]):
            flash('Please fill out all fields', 'danger')
            return render_template('main/contact.html')
        
        try:
            # Create email message
            recipient = os.getenv('MAIL_RECIPIENT', '   ')
            msg = Message(
                subject=f"Book Recommendation Contact: {subject}",
                recipients=[recipient]
            )
            
            # Email body in HTML format
            msg.html = f"""
            <h3>New Contact Form Submission</h3>
            <p><strong>From:</strong> {name} ({email})</p>
            <p><strong>Subject:</strong> {subject}</p>
            <p><strong>Message:</strong></p>
            <p>{message_text}</p>
            """
            
            # Send email
            mail.send(msg)
            
            # Send confirmation email to user
            confirmation = Message(
                subject="Thank you for contacting Book Recommendation System",
                recipients=[email]
            )
            
            confirmation.html = f"""
            <h3>Thank you for contacting us, {name}!</h3>
            <p>We have received your message regarding "{subject}" and will get back to you as soon as possible.</p>
            <p>For your records, here is a copy of your message:</p>
            <p><em>{message_text}</em></p>
            <p>Best regards,<br>Book Recommendation Team</p>
            """
            
            mail.send(confirmation)
            
            flash('Your message has been sent successfully! We will get back to you soon.', 'success')
            return redirect(url_for('main.contact'))
            
        except Exception as e:
            print(f"Email error: {str(e)}")
            flash('There was an error sending your message. Please try again later.', 'danger')
    
    return render_template('main/contact.html') 