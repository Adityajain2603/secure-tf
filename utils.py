import os
from werkzeug.utils import secure_filename
from flask_mail import Message
from cryptography.fernet import Fernet
from flask import current_app, url_for
from app import mail

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def send_verification_email(user):
    token = Fernet.generate_key().decode()
    verify_url = url_for('email_verify', token=token, _external=True)
    msg = Message('Verify Your Email', sender=current_app.config['MAIL_USERNAME'], recipients=[user.email])
    msg.body = f'Click the following link to verify your email: {verify_url}'
    mail.send(msg)
    # Save the token for future verification
    user.email_token = token
    user.save()

def encrypt_url(url):
    key = Fernet.generate_key()
    cipher = Fernet(key)
    encrypted_url = cipher.encrypt(url.encode()).decode()
    return encrypted_url

def decrypt_url(encrypted_url, key):
    cipher = Fernet(key)
    decrypted_url = cipher.decrypt(encrypted_url.encode()).decode()
    return decrypted_url
