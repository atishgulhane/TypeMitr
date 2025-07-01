from flask import render_template, request, redirect, url_for, flash, session, send_file, jsonify
from app import app, db
from models import GeneratedDocument, DocumentStats, UserSession
from document_generator import generate_document_content
from pdf_generator import generate_pdf
import io
import uuid
from datetime import datetime

# Document categories and types based on uploaded files
DOCUMENT_CATEGORIES = {
    'academic': {
        'name': 'Academic & Educational',
        'icon': '🎓',
        'types': [
            'University/College Admission Application',
            'Scholarship/Financial Aid Application',
            'Bonafide Certificate Application',
            'Migration Certificate Application',
            'Character Certificate Application (School/College)',
            'Provisional Certificate Application',
            'Degree Certificate Application',
            'No Dues Certificate Application (College/Hostel)',
            'Change of Name Application (Academic Records)',
            'Re-evaluation/Re-checking Application (Exams)',
            'Duplicate Marksheet/Certificate Application',
            'Withdrawal Application (from course, college)',
            'Application for Inter-College Transfer',
            'Application for Leave of Absence (Academic)',
            'Application for Readmission',
            'Application for Industrial Training/Internship',
            'Application for Campus Placement',
            'Request for Academic Records/Transcript'
        ]
    },
    'corporate': {
        'name': 'Corporate & Business',
        'icon': '💼',
        'types': [
            'Job Application (Private Sector)',
            'Business Proposal Application',
            'Vendor/Supplier Application',
            'Franchise Application',
            'Tender Application (Private Sector Procurement)',
            'Expression of Interest (EOI) Application',
            'Partnership/Joint Venture Application',
            'Vendor Empanelment Application',
            'Dealer/Distributor Application',
            'Client Onboarding Application',
            'Application for Company Registration/Incorporation',
            'Application for Statutory Licenses',
            'Application for Tax Registration',
            'Application for Tax Refund (Corporate)',
            'Application for Environmental Clearances (Industrial)',
            'Application for Factory License',
            'Application for Export/Import Code (IEC)',
            'Request for Quotation/Proposal (RFQ/RFP)'
        ]
    },
    'government': {
        'name': 'Government & Public Service',
        'icon': '🏛️',
        'types': [
            'Aadhaar Card Application/Update/Correction',
            'PAN Card Application/Correction',
            'Passport Application',
            'Voter ID Application',
            'Birth Certificate Application/Correction',
            'Death Certificate Application/Correction',
            'Marriage Registration Application',
            'Domicile Certificate Application',
            'Caste Certificate Application',
            'Income Certificate Application',
            'Character Certificate Application (Police Clearance)',
            'Ration Card Application',
            'Driving License Application',
            'Vehicle Registration/Transfer Application',
            'Building Permit Application',
            'Trade License Application',
            'Right to Information (RTI) Application',
            'Public Grievance Application',
            'Property Registration Application',
            'Utility Connection Application'
        ]
    },
    'legal': {
        'name': 'Court & Judicial',
        'icon': '⚖️',
        'types': [
            'Writ Petition',
            'Divorce Petition',
            'Guardianship Petition',
            'Bail Application',
            'Application for Stay of Proceedings',
            'Application for Adjournment',
            'Application for Condonation of Delay',
            'Application for Amendment',
            'Application for Execution of Decree',
            'Application for Contempt of Court Proceedings',
            'Application for Review/Revision of Order',
            'Application for Transfer of Case',
            'Application for Maintenance',
            'Application for Interim Injunction',
            'Habeas Corpus Petition',
            'Mandamus Petition',
            'Consumer Complaint Application'
        ]
    },
    'general': {
        'name': 'General Applications',
        'icon': '📝',
        'types': [
            'Leave Application',
            'Refund/Reimbursement Application',
            'Club/Society Membership Application',
            'Volunteer Application',
            'Event Registration Application',
            'Pet Adoption Application',
            'Contest/Competition Entry Application',
            'Complaint Application/Form',
            'Request for Permission'
        ]
    }
}

LANGUAGES = {
    'english': 'English',
    'hindi': 'हिंदी (Hindi)',
    'marathi': 'मराठी (Marathi)'
}

TONES = {
    'formal': 'Formal',
    'semi_formal': 'Semi-formal',
    'friendly': 'Friendly'
}

@app.route('/')
def index():
    # Initialize or update user session
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        
    # Get or create user session in database
    user_session = UserSession.query.filter_by(session_id=session['session_id']).first()
    if not user_session:
        user_session = UserSession(session_id=session['session_id'])
        db.session.add(user_session)
        db.session.commit()
    else:
        user_session.last_activity = datetime.utcnow()
        db.session.commit()
    
    return render_template('index.html', 
                         categories=DOCUMENT_CATEGORIES,
                         languages=LANGUAGES,
                         tones=TONES)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Get form data
        category = request.form.get('category')
        document_type = request.form.get('document_type')
        language = request.form.get('language')
        tone = request.form.get('tone')
        sender_name = request.form.get('sender_name')
        recipient_name = request.form.get('recipient_name')
        purpose = request.form.get('purpose')
        reason = request.form.get('reason', '')
        date_from_str = request.form.get('date_from')
        date_to_str = request.form.get('date_to')
        
        # Validate required fields
        if not all([category, document_type, language, tone, sender_name, recipient_name, purpose]):
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('index'))
        
        # Parse dates
        date_from = None
        date_to = None
        if date_from_str:
            date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date()
        if date_to_str:
            date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date()
        
        # Generate document content using AI
        generated_content = generate_document_content(
            document_type=document_type,
            language=language,
            tone=tone,
            sender_name=sender_name,
            recipient_name=recipient_name,
            purpose=purpose,
            reason=reason,
            date_from=date_from,
            date_to=date_to
        )
        
        # Create date range string
        date_range = None
        if date_from and date_to:
            date_range = f"{date_from} to {date_to}"
        elif date_from:
            date_range = f"From {date_from}"
        elif date_to:
            date_range = f"Until {date_to}"
        
        # Check if this was generated in demo mode (based on content pattern)
        is_demo = "demo" in generated_content.lower() or "sample" in generated_content.lower()
        
        # Save to database
        document = GeneratedDocument(
            document_type=document_type,
            category=category,
            language=language,
            tone=tone,
            sender_name=sender_name,
            recipient_name=recipient_name,
            purpose=purpose,
            reason=reason,
            date_range=date_range,
            generated_content=generated_content,
            is_demo=is_demo
        )
        
        db.session.add(document)
        db.session.commit()
        
        # Store in session for display
        session['generated_document'] = {
            'id': document.id,
            'content': generated_content,
            'document_type': document_type,
            'sender_name': sender_name,
            'recipient_name': recipient_name
        }
        
        return render_template('generate.html', 
                             document=session['generated_document'],
                             categories=DOCUMENT_CATEGORIES,
                             languages=LANGUAGES,
                             tones=TONES)
        
    except Exception as e:
        app.logger.error(f"Error generating document: {str(e)}")
        flash(f'Error generating document: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/download_pdf/<int:document_id>')
def download_pdf(document_id):
    try:
        document = GeneratedDocument.query.get_or_404(document_id)
        
        # Generate PDF
        pdf_buffer = generate_pdf({
            'content': document.final_content,
            'document_type': document.document_type,
            'sender_name': document.sender_name,
            'recipient_name': document.recipient_name
        })
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f"{document.document_type}_{document.id}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        app.logger.error(f"Error generating PDF: {str(e)}")
        flash('Error generating PDF', 'error')
        return redirect(url_for('index'))
        
        # Create filename
        filename = f"{document.document_type.replace('/', '_').replace(' ', '_')}_{document.sender_name.replace(' ', '_')}.pdf"
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        app.logger.error(f"Error generating PDF: {str(e)}")
        flash(f'Error generating PDF: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/get_document_types/<category>')
def get_document_types(category):
    """AJAX endpoint to get document types for a category"""
    if category in DOCUMENT_CATEGORIES:
        return jsonify(DOCUMENT_CATEGORIES[category]['types'])
    return jsonify([])
