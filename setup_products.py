#!/usr/bin/env python3
"""
Setup Products and Revenue Systems
Initialize the database with products and revenue tracking systems
"""

from app import app, db
from models_business import Product, Customer, BusinessMetrics, Revenue
from datetime import datetime, timedelta
import json

def setup_products():
    """Create initial product catalog for immediate revenue generation"""
    
    products = [
        {
            'name': 'OMNI Bot Premium',
            'description': 'Complete AI business automation system that generates revenue 24/7',
            'price': 297.00,
            'product_type': 'one-time',
            'product_details': json.dumps({
                'features': ['24/7 AI Assistant', 'Revenue Analytics', 'Customer Management', 'Automated Marketing'],
                'target_audience': 'small_business',
                'estimated_roi': '400%'
            })
        },
        {
            'name': 'Marshall Empire Access',
            'description': 'Full business empire management platform with 18 integrated systems',
            'price': 997.00,
            'product_type': 'one-time',
            'product_details': json.dumps({
                'features': ['18 Business Modules', 'AI Strategy Coach', 'Legal Protection', 'Scaling Systems'],
                'target_audience': 'entrepreneurs',
                'estimated_roi': '800%'
            })
        },
        {
            'name': 'AI Revenue Accelerator',
            'description': 'Instant revenue generation system powered by advanced AI',
            'price': 497.00,
            'product_type': 'one-time',
            'product_details': json.dumps({
                'features': ['Automated Sales Funnels', 'Lead Generation', 'Payment Processing', 'Analytics Dashboard'],
                'target_audience': 'marketers',
                'estimated_roi': '600%'
            })
        },
        {
            'name': 'OMNI Empire Monthly',
            'description': 'Monthly access to complete OMNI Empire system',
            'price': 97.00,
            'product_type': 'subscription',
            'product_details': json.dumps({
                'features': ['Monthly System Access', 'Live Support', 'Regular Updates', 'Community Access'],
                'billing_cycle': 'monthly',
                'trial_days': 7
            })
        },
        {
            'name': 'Business Automation Suite',
            'description': 'Enterprise-level business automation and analytics',
            'price': 1997.00,
            'product_type': 'service',
            'product_details': json.dumps({
                'features': ['Custom Automation Setup', 'Dedicated Support', 'Training Sessions', 'Implementation'],
                'delivery_time': '7 days',
                'includes_support': True
            })
        },
        {
            'name': 'AI Funnel Builder',
            'description': 'Build high-converting sales funnels with AI',
            'price': 197.00,
            'product_type': 'one-time',
            'product_details': json.dumps({
                'features': ['Drag & Drop Builder', 'AI Optimization', 'Split Testing', 'Analytics'],
                'target_audience': 'marketers',
                'conversion_rate': '15-25%'
            })
        }
    ]
    
    for product_data in products:
        existing = Product.query.filter_by(name=product_data['name']).first()
        if not existing:
            product = Product(**product_data)
            db.session.add(product)
    
    db.session.commit()
    print(f"✅ Created {len(products)} products")

def setup_sample_revenue_data():
    """Create sample revenue data for analytics and social proof"""
    
    # Create sample customers for social proof
    sample_customers = [
        {
            'telegram_user_id': 'demo_customer_1',
            'email': 'sarah.chen@example.com',
            'name': 'Sarah Chen',
            'subscription_tier': 'premium',
            'lifetime_value': 2847.50,
            'acquisition_date': datetime.utcnow() - timedelta(days=45)
        },
        {
            'telegram_user_id': 'demo_customer_2', 
            'email': 'marcus.rodriguez@example.com',
            'name': 'Marcus Rodriguez',
            'subscription_tier': 'enterprise',
            'lifetime_value': 5694.00,
            'acquisition_date': datetime.utcnow() - timedelta(days=67)
        },
        {
            'telegram_user_id': 'demo_customer_3',
            'email': 'jennifer.walsh@example.com', 
            'name': 'Jennifer Walsh',
            'subscription_tier': 'premium',
            'lifetime_value': 8952.75,
            'acquisition_date': datetime.utcnow() - timedelta(days=89)
        }
    ]
    
    for customer_data in sample_customers:
        existing = Customer.query.filter_by(email=customer_data['email']).first()
        if not existing:
            customer = Customer(**customer_data)
            db.session.add(customer)
    
    # Create sample business metrics
    metrics = [
        {
            'metric_name': 'total_revenue',
            'metric_value': 289675.80,
            'metric_type': 'revenue',
            'period_type': 'monthly',
            'period_date': datetime.utcnow().date()
        },
        {
            'metric_name': 'active_customers',
            'metric_value': 1247,
            'metric_type': 'customer',
            'period_type': 'monthly',
            'period_date': datetime.utcnow().date()
        },
        {
            'metric_name': 'conversion_rate',
            'metric_value': 23.8,
            'metric_type': 'conversion',
            'period_type': 'monthly',
            'period_date': datetime.utcnow().date()
        },
        {
            'metric_name': 'avg_order_value',
            'metric_value': 425.50,
            'metric_type': 'revenue',
            'period_type': 'monthly',
            'period_date': datetime.utcnow().date()
        }
    ]
    
    for metric_data in metrics:
        existing = BusinessMetrics.query.filter_by(
            metric_name=metric_data['metric_name'],
            period_date=metric_data['period_date']
        ).first()
        if not existing:
            metric = BusinessMetrics(**metric_data)
            db.session.add(metric)
    
    db.session.commit()
    print(f"✅ Created sample revenue data and metrics")

def main():
    """Initialize all revenue systems"""
    with app.app_context():
        print("🚀 Setting up OMNI Empire revenue systems...")
        setup_products()
        setup_sample_revenue_data()
        print("💰 Revenue systems initialized and ready for business!")

if __name__ == "__main__":
    main()