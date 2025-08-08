from app import db
from datetime import datetime
import json

class BotConfig(db.Model):
    """Store bot configuration and API keys"""
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)
    encrypted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Plugin(db.Model):
    """Track installed plugins"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    version = db.Column(db.String(50), nullable=False)
    enabled = db.Column(db.Boolean, default=True)
    module_path = db.Column(db.String(200), nullable=False)
    config = db.Column(db.Text)  # JSON config
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UpdateHistory(db.Model):
    """Track system updates"""
    id = db.Column(db.Integer, primary_key=True)
    version_from = db.Column(db.String(50))
    version_to = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # pending, success, failed, rolled_back
    backup_path = db.Column(db.String(300))
    error_message = db.Column(db.Text)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

class SystemMetrics(db.Model):
    """Store system performance metrics"""
    id = db.Column(db.Integer, primary_key=True)
    metric_name = db.Column(db.String(100), nullable=False)
    metric_value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class UserState(db.Model):
    """Persist user states across updates"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    platform = db.Column(db.String(50), nullable=False)  # telegram, etc
    state_data = db.Column(db.Text)  # JSON data
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
