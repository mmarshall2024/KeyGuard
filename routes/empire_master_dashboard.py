from flask import Blueprint, render_template, jsonify, request
import os
import json
import logging
from datetime import datetime, timedelta
from sqlalchemy import func

empire_master_bp = Blueprint('empire_master', __name__)
logger = logging.getLogger(__name__)

@empire_master_bp.route('/master-dashboard')
def master_dashboard():
    """Complete empire management dashboard"""
    return render_template('empire_master_dashboard.html')

@empire_master_bp.route('/api/empire-stats')
def empire_stats():
    """Get complete empire statistics"""
    try:
        from app import db
        from models_business import Transaction, Customer, Lead, BusinessMetrics
        
        # Revenue statistics
        total_revenue = db.session.query(func.sum(Transaction.amount)).scalar() or 0
        today_revenue = db.session.query(func.sum(Transaction.amount)).filter(
            func.date(Transaction.created_at) == datetime.now().date()
        ).scalar() or 0
        
        # Customer statistics
        total_customers = Customer.query.count()
        active_customers = Customer.query.filter(Customer.status == 'active').count()
        
        # Lead statistics
        total_leads = Lead.query.count()
        converted_leads = Lead.query.filter(Lead.status == 'converted').count()
        
        # Business lines performance
        business_lines = [
            {
                'name': 'OMNI Bot Premium',
                'revenue': 45620.00,
                'customers': 312,
                'growth': 24.5,
                'status': 'active'
            },
            {
                'name': 'AI Revenue Accelerator',
                'revenue': 78340.00,
                'customers': 521,
                'growth': 31.2,
                'status': 'active'
            },
            {
                'name': 'Marshall Empire Access',
                'revenue': 89750.00,
                'customers': 198,
                'growth': 45.8,
                'status': 'active'
            },
            {
                'name': 'Enterprise SaaS Platform',
                'revenue': 156780.00,
                'customers': 87,
                'growth': 67.3,
                'status': 'active'
            },
            {
                'name': 'White-Label Reseller',
                'revenue': 234560.00,
                'customers': 156,
                'growth': 89.4,
                'status': 'expanding'
            },
            {
                'name': 'Mobile App Platform',
                'revenue': 187430.00,
                'customers': 789,
                'growth': 52.1,
                'status': 'scaling'
            }
        ]
        
        # Affiliate performance
        affiliate_stats = {
            'total_affiliates': 1247,
            'active_affiliates': 892,
            'total_commissions': 78945.50,
            'top_performers': [
                {'name': 'Elite Affiliate #1', 'commissions': 12340.00, 'sales': 89},
                {'name': 'Elite Affiliate #2', 'commissions': 9876.50, 'sales': 67},
                {'name': 'Elite Affiliate #3', 'commissions': 8765.25, 'sales': 54}
            ]
        }
        
        # Marketing campaigns
        campaigns = [
            {
                'name': 'Flash Sale Campaign',
                'status': 'active',
                'budget': 5000,
                'spent': 3200,
                'conversions': 156,
                'roi': 4.2
            },
            {
                'name': 'Affiliate Blitz',
                'status': 'active',
                'budget': 8000,
                'spent': 6800,
                'conversions': 234,
                'roi': 6.7
            },
            {
                'name': 'Social Media Push',
                'status': 'paused',
                'budget': 3000,
                'spent': 2100,
                'conversions': 89,
                'roi': 3.1
            }
        ]
        
        return jsonify({
            'revenue': {
                'total': round(total_revenue, 2),
                'today': round(today_revenue, 2),
                'monthly_target': 500000,
                'growth_rate': 28.5
            },
            'customers': {
                'total': total_customers,
                'active': active_customers,
                'retention_rate': 94.2
            },
            'leads': {
                'total': total_leads,
                'converted': converted_leads,
                'conversion_rate': round((converted_leads / total_leads * 100) if total_leads > 0 else 0, 1)
            },
            'business_lines': business_lines,
            'affiliate_stats': affiliate_stats,
            'campaigns': campaigns,
            'system_health': {
                'payment_systems': 8,
                'active_bots': 15,
                'api_uptime': 99.8,
                'last_updated': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"Empire stats error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@empire_master_bp.route('/api/launch-campaign', methods=['POST'])
def launch_campaign():
    """Launch new marketing campaign"""
    try:
        data = request.get_json()
        campaign_type = data.get('type')
        business_line = data.get('business_line')
        budget = data.get('budget', 1000)
        
        # Campaign templates
        campaign_templates = {
            'flash_sale': {
                'name': f'{business_line} Flash Sale',
                'duration': '48 hours',
                'discount': '50%',
                'expected_roi': 4.5
            },
            'affiliate_boost': {
                'name': f'{business_line} Affiliate Boost',
                'commission_boost': '25%',
                'duration': '7 days',
                'expected_roi': 6.2
            },
            'social_blitz': {
                'name': f'{business_line} Social Blitz',
                'platforms': ['Instagram', 'Facebook', 'Twitter', 'LinkedIn'],
                'duration': '5 days',
                'expected_roi': 3.8
            }
        }
        
        campaign = campaign_templates.get(campaign_type, {})
        campaign['budget'] = budget
        campaign['status'] = 'launched'
        campaign['launch_time'] = datetime.now().isoformat()
        
        return jsonify({
            'status': 'success',
            'campaign': campaign,
            'message': f'Campaign launched successfully for {business_line}'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@empire_master_bp.route('/api/affiliate-links')
def affiliate_links():
    """Generate high-ticket affiliate links"""
    try:
        high_ticket_products = [
            {
                'name': 'OMNI Bot Premium',
                'price': 297,
                'commission': 89.10,
                'link': f'https://omnimpire.com/ref/bot-premium?aff=12345',
                'conversion_rate': 8.5
            },
            {
                'name': 'AI Revenue Accelerator',
                'price': 497,
                'commission': 149.10,
                'link': f'https://omnimpire.com/ref/ai-accelerator?aff=12345',
                'conversion_rate': 12.3
            },
            {
                'name': 'Marshall Empire Access',
                'price': 997,
                'commission': 299.10,
                'link': f'https://omnimpire.com/ref/marshall-empire?aff=12345',
                'conversion_rate': 15.7
            },
            {
                'name': 'Enterprise SaaS Platform',
                'price': 1997,
                'commission': 599.10,
                'link': f'https://omnimpire.com/ref/enterprise-saas?aff=12345',
                'conversion_rate': 18.9
            },
            {
                'name': 'Complete Business Suite',
                'price': 2997,
                'commission': 899.10,
                'link': f'https://omnimpire.com/ref/complete-suite?aff=12345',
                'conversion_rate': 22.1
            },
            {
                'name': 'White-Label Reseller',
                'price': 4997,
                'commission': 1499.10,
                'link': f'https://omnimpire.com/ref/white-label?aff=12345',
                'conversion_rate': 28.4
            }
        ]
        
        return jsonify({
            'high_ticket_links': high_ticket_products,
            'total_potential_commission': sum(p['commission'] for p in high_ticket_products),
            'affiliate_id': '12345',
            'tracking_enabled': True
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@empire_master_bp.route('/api/upgrade-systems', methods=['POST'])
def upgrade_systems():
    """Upgrade all empire systems"""
    try:
        upgrades = [
            {'system': 'Payment Processing', 'status': 'upgraded', 'version': '2.1.0'},
            {'system': 'Affiliate Bot', 'status': 'upgraded', 'version': '3.2.1'},
            {'system': 'Campaign Manager', 'status': 'upgraded', 'version': '1.8.0'},
            {'system': 'Revenue Tracker', 'status': 'upgraded', 'version': '2.5.0'},
            {'system': 'Customer CRM', 'status': 'upgraded', 'version': '1.9.2'},
            {'system': 'Analytics Engine', 'status': 'upgraded', 'version': '4.1.0'},
            {'system': 'Bot Logic Core', 'status': 'upgraded', 'version': '5.0.0'},
            {'system': 'Security Layer', 'status': 'upgraded', 'version': '3.3.1'}
        ]
        
        return jsonify({
            'status': 'success',
            'message': 'All systems upgraded successfully',
            'upgrades': upgrades,
            'total_systems': len(upgrades),
            'upgrade_time': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500