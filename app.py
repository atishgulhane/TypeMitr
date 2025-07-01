import os
import logging
from flask import Flask, render_template, request, jsonify, session, send_file, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime
import json
from openai_service import generate_letter_content
from pdf_generator import generate_pdf
from document_types import DOCUMENT_TYPES

logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///typemitr.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# initialize the app with the extension
db.init_app(app)

with app.app_context():
    import models
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html', document_types=DOCUMENT_TYPES)

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'GET':
        document_type = request.args.get('type')
        if not document_type or document_type not in DOCUMENT_TYPES:
            flash('Invalid document type selected.', 'error')
            return redirect(url_for('index'))
        
        return render_template('generate.html', 
                             document_type=document_type,
                             document_info=DOCUMENT_TYPES[document_type])
    
    if request.method == 'POST':
        try:
            # Get form data
            document_type = request.form.get('document_type')
            language = request.form.get('language', 'english')
            tone = request.form.get('tone', 'formal')
            
            # Get input fields
            sender_name = request.form.get('sender_name', '').strip()
            recipient_name = request.form.get('recipient_name', '').strip()
            purpose = request.form.get('purpose', '').strip()
            reason = request.form.get('reason', '').strip()
            date_range = request.form.get('date_range', '').strip()
            additional_details = request.form.get('additional_details', '').strip()
            
            # Validation
            if not all([document_type, sender_name, recipient_name, purpose]):
                flash('Please fill in all required fields.', 'error')
                return render_template('generate.html', 
                                     document_type=document_type,
                                     document_info=DOCUMENT_TYPES.get(document_type, {}),
                                     form_data=request.form)
            
            # Generate letter content using AI
            letter_content = generate_letter_content(
                document_type=document_type,
                language=language,
                tone=tone,
                sender_name=sender_name,
                recipient_name=recipient_name,
                purpose=purpose,
                reason=reason,
                date_range=date_range,
                additional_details=additional_details
            )
            
            # Store in session for PDF generation
            session['generated_letter'] = {
                'content': letter_content,
                'document_type': document_type,
                'language': language,
                'sender_name': sender_name,
                'recipient_name': recipient_name,
                'generated_at': datetime.now().isoformat()
            }
            
            return render_template('generate.html',
                                 document_type=document_type,
                                 document_info=DOCUMENT_TYPES.get(document_type, {}),
                                 generated_content=letter_content,
                                 form_data=request.form)
            
        except Exception as e:
            logging.error(f"Error generating letter: {str(e)}")
            flash(f'Error generating letter: {str(e)}', 'error')
            return render_template('generate.html',
                                 document_type=request.form.get('document_type'),
                                 document_info=DOCUMENT_TYPES.get(request.form.get('document_type'), {}),
                                 form_data=request.form)

@app.route('/download-pdf')
def download_pdf():
    try:
        generated_letter = session.get('generated_letter')
        if not generated_letter:
            flash('No letter found. Please generate a letter first.', 'error')
            return redirect(url_for('index'))
        
        # Generate PDF
        pdf_file = generate_pdf(generated_letter)
        
        filename = f"typemitr_{generated_letter['document_type'].replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        return send_file(
            pdf_file,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        logging.error(f"Error generating PDF: {str(e)}")
        flash(f'Error generating PDF: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html', document_types=DOCUMENT_TYPES), 404

@app.errorhandler(500)
def server_error(error):
    flash('An internal server error occurred. Please try again.', 'error')
    return render_template('index.html', document_types=DOCUMENT_TYPES), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
