from app import db
from datetime import datetime
import json

class GeneratedDocument(db.Model):
    __tablename__ = 'generated_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    document_type = db.Column(db.String(100), nullable=False, index=True)
    category = db.Column(db.String(50), nullable=False, index=True)
    language = db.Column(db.String(20), nullable=False, default='english')
    tone = db.Column(db.String(20), nullable=False, default='formal')
    sender_name = db.Column(db.String(100), nullable=False)
    recipient_name = db.Column(db.String(100), nullable=False)
    purpose = db.Column(db.Text, nullable=False)
    reason = db.Column(db.Text)
    date_range = db.Column(db.String(100))
    additional_details = db.Column(db.Text)
    generated_content = db.Column(db.Text, nullable=False)
    edited_content = db.Column(db.Text)  # For storing user edits
    is_demo = db.Column(db.Boolean, default=False)  # Track if generated via demo mode
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<GeneratedDocument {self.id}: {self.document_type}>'
    
    def to_dict(self):
        """Convert document to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'document_type': self.document_type,
            'category': self.category,
            'language': self.language,
            'tone': self.tone,
            'sender_name': self.sender_name,
            'recipient_name': self.recipient_name,
            'purpose': self.purpose,
            'reason': self.reason,
            'date_range': self.date_range,
            'additional_details': self.additional_details,
            'generated_content': self.generated_content,
            'edited_content': self.edited_content,
            'is_demo': self.is_demo,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @property
    def final_content(self):
        """Return edited content if available, otherwise generated content"""
        return self.edited_content if self.edited_content else self.generated_content


class DocumentStats(db.Model):
    __tablename__ = 'document_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    document_type = db.Column(db.String(100), nullable=False, index=True)
    category = db.Column(db.String(50), nullable=False, index=True)
    language = db.Column(db.String(20), nullable=False, index=True)
    generation_count = db.Column(db.Integer, default=1)
    last_generated = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<DocumentStats {self.document_type}: {self.generation_count} generations>'


class UserSession(db.Model):
    __tablename__ = 'user_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    documents_generated = db.Column(db.Integer, default=0)
    first_visit = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    preferred_language = db.Column(db.String(20), default='english')
    preferred_tone = db.Column(db.String(20), default='formal')
    
    def __repr__(self):
        return f'<UserSession {self.session_id}: {self.documents_generated} docs>'
