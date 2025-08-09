from app import db
from datetime import datetime
from sqlalchemy import event
import json

class Customer(db.Model):
    """Customer management for revenue tracking"""
    id = db.Column(db.Integer, primary_key=True)
    telegram_user_id = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    subscription_tier = db.Column(db.String(50), default='free')
    lifetime_value = db.Column(db.Float, default=0.0)
    acquisition_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')  # active, inactive, churned
    additional_data = db.Column(db.Text)  # JSON for additional data
    
    # Relationships
    payments = db.relationship('Payment', backref='customer', lazy=True)
    interactions = db.relationship('CustomerInteraction', backref='customer', lazy=True)

class Payment(db.Model):
    """Payment tracking for revenue analytics"""
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    stripe_payment_id = db.Column(db.String(200), unique=True)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    payment_method = db.Column(db.String(50))  # stripe, crypto, paypal
    product_type = db.Column(db.String(100))  # subscription, one-time, service
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed, refunded
    processed_at = db.Column(db.DateTime, default=datetime.utcnow)
    payment_details = db.Column(db.Text)  # JSON for payment details

class Revenue(db.Model):
    """Daily revenue aggregation for analytics"""
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, unique=True)
    total_revenue = db.Column(db.Float, default=0.0)
    subscription_revenue = db.Column(db.Float, default=0.0)
    one_time_revenue = db.Column(db.Float, default=0.0)
    refunds = db.Column(db.Float, default=0.0)
    net_revenue = db.Column(db.Float, default=0.0)
    transaction_count = db.Column(db.Integer, default=0)
    new_customers = db.Column(db.Integer, default=0)
    churned_customers = db.Column(db.Integer, default=0)

class CustomerInteraction(db.Model):
    """Track customer interactions for engagement analytics"""
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    interaction_type = db.Column(db.String(50), nullable=False)  # chat, command, payment, support
    interaction_data = db.Column(db.Text)  # JSON data
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    value_score = db.Column(db.Float, default=0.0)  # Engagement scoring

class Product(db.Model):
    """Product catalog for monetization"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    product_type = db.Column(db.String(50))  # subscription, one-time, service
    stripe_price_id = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    product_details = db.Column(db.Text)  # JSON for additional product data

class Lead(db.Model):
    """Lead management for funnel tracking"""
    id = db.Column(db.Integer, primary_key=True)
    telegram_user_id = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    source = db.Column(db.String(100))  # organic, ad, referral, etc.
    status = db.Column(db.String(20), default='new')  # new, contacted, qualified, converted, lost
    lead_score = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_contact = db.Column(db.DateTime)
    converted_at = db.Column(db.DateTime)
    notes = db.Column(db.Text)

class Transaction(db.Model):
    """Individual transaction tracking for payment processing"""
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    source = db.Column(db.String(50), nullable=False)  # stripe, crypto, paypal, etc.
    transaction_id = db.Column(db.String(200), unique=True)
    product_name = db.Column(db.String(200))
    customer_email = db.Column(db.String(120))
    status = db.Column(db.String(20), default='completed')  # completed, pending, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class BusinessMetrics(db.Model):
    """Business KPI tracking"""
    id = db.Column(db.Integer, primary_key=True)
    metric_name = db.Column(db.String(100), nullable=False)
    metric_value = db.Column(db.Float, nullable=False)
    metric_type = db.Column(db.String(50))  # revenue, customer, engagement, conversion
    period_type = db.Column(db.String(20))  # daily, weekly, monthly
    period_date = db.Column(db.Date, nullable=False)
    calculated_at = db.Column(db.DateTime, default=datetime.utcnow)

# Event listeners for automatic calculations
@event.listens_for(Payment, 'after_insert')
def update_customer_ltv(mapper, connection, target):
    """Update customer lifetime value when payment is added"""
    if target.status == 'completed':
        customer = Customer.query.get(target.customer_id)
        if customer:
            total_payments = db.session.query(db.func.sum(Payment.amount)).filter(
                Payment.customer_id == target.customer_id,
                Payment.status == 'completed'
            ).scalar() or 0
            customer.lifetime_value = total_payments
            db.session.commit()