from flask import Blueprint, render_template, jsonify, request
import os
import json
import logging
from datetime import datetime
from sqlalchemy import func

setup_checklist_bp = Blueprint('setup_checklist', __name__)
logger = logging.getLogger(__name__)

@setup_checklist_bp.route('/setup-checklist')
def setup_checklist():
    """Interactive setup checklist dashboard"""
    return render_template('setup_checklist.html')

@setup_checklist_bp.route('/api/checklist-categories')
def checklist_categories():
    """Get all setup checklist categories"""
    try:
        categories = [
            {
                'category_id': 'payment_systems',
                'name': 'Payment Systems Setup',
                'icon': 'fas fa-credit-card',
                'priority': 'high',
                'description': 'Configure all payment processors and merchant accounts',
                'estimated_time': '2-4 hours',
                'items': [
                    {
                        'id': 'stripe_setup',
                        'name': 'Stripe Account Setup',
                        'status': 'completed',
                        'description': 'Create Stripe account and configure API keys',
                        'required_info': ['Business details', 'Bank account', 'Tax ID'],
                        'links': ['https://stripe.com/connect', '/payment-methods'],
                        'notes': 'STRIPE_SECRET_KEY already configured'
                    },
                    {
                        'id': 'paypal_setup',
                        'name': 'PayPal Business Account',
                        'status': 'pending',
                        'description': 'Setup PayPal business account for payments',
                        'required_info': ['Business verification', 'Bank linking'],
                        'links': ['https://paypal.com/business', '/payment-setup-guide'],
                        'notes': 'Need to integrate PayPal API'
                    },
                    {
                        'id': 'crypto_wallet',
                        'name': 'Cryptocurrency Wallets',
                        'status': 'pending',
                        'description': 'Setup Bitcoin and Ethereum wallets',
                        'required_info': ['Wallet addresses', 'Private keys (secure)'],
                        'links': ['https://metamask.io', 'https://blockchain.com'],
                        'notes': 'For customer crypto payment option'
                    },
                    {
                        'id': 'bank_integration',
                        'name': 'Bank Transfer Integration',
                        'status': 'pending',
                        'description': 'Direct bank transfer setup',
                        'required_info': ['Bank routing', 'Account verification'],
                        'links': ['/payment-methods'],
                        'notes': 'For high-value transactions'
                    }
                ]
            },
            {
                'category_id': 'social_accounts',
                'name': 'Social Media Accounts',
                'icon': 'fas fa-share-alt',
                'priority': 'high',
                'description': 'Setup and link all social media business accounts',
                'estimated_time': '3-5 hours',
                'items': [
                    {
                        'id': 'facebook_business',
                        'name': 'Facebook Business Manager',
                        'status': 'pending',
                        'description': 'Create Facebook Business Manager account',
                        'required_info': ['Business verification', 'Ad account setup'],
                        'links': ['https://business.facebook.com'],
                        'notes': 'Essential for Facebook/Instagram ads'
                    },
                    {
                        'id': 'instagram_business',
                        'name': 'Instagram Business Account',
                        'status': 'pending',
                        'description': 'Convert to business account and link to Facebook',
                        'required_info': ['Business category', 'Contact info'],
                        'links': ['https://business.instagram.com'],
                        'notes': 'Link to Facebook Business Manager'
                    },
                    {
                        'id': 'linkedin_company',
                        'name': 'LinkedIn Company Page',
                        'status': 'pending',
                        'description': 'Create LinkedIn company page for B2B marketing',
                        'required_info': ['Company details', 'Logo', 'Description'],
                        'links': ['https://linkedin.com/company/setup'],
                        'notes': 'Critical for enterprise customers'
                    },
                    {
                        'id': 'twitter_business',
                        'name': 'Twitter Business Account',
                        'status': 'pending',
                        'description': 'Setup Twitter for business with verified status',
                        'required_info': ['Business verification', 'Contact details'],
                        'links': ['https://business.twitter.com'],
                        'notes': 'For real-time engagement'
                    },
                    {
                        'id': 'youtube_channel',
                        'name': 'YouTube Business Channel',
                        'status': 'pending',
                        'description': 'Create YouTube channel for video marketing',
                        'required_info': ['Channel art', 'Brand guidelines'],
                        'links': ['https://youtube.com/create'],
                        'notes': 'For educational content and demos'
                    },
                    {
                        'id': 'tiktok_business',
                        'name': 'TikTok Business Account',
                        'status': 'pending',
                        'description': 'Setup TikTok for viral marketing',
                        'required_info': ['Business verification', 'Content strategy'],
                        'links': ['https://ads.tiktok.com'],
                        'notes': 'High engagement potential'
                    }
                ]
            },
            {
                'category_id': 'email_marketing',
                'name': 'Email Marketing Platforms',
                'icon': 'fas fa-envelope',
                'priority': 'high',
                'description': 'Setup email marketing and automation platforms',
                'estimated_time': '2-3 hours',
                'items': [
                    {
                        'id': 'mailchimp_setup',
                        'name': 'Mailchimp Account',
                        'status': 'pending',
                        'description': 'Setup Mailchimp for email campaigns',
                        'required_info': ['Business details', 'Domain verification'],
                        'links': ['https://mailchimp.com'],
                        'notes': 'For newsletter and automated sequences'
                    },
                    {
                        'id': 'sendgrid_api',
                        'name': 'SendGrid API',
                        'status': 'pending',
                        'description': 'Configure SendGrid for transactional emails',
                        'required_info': ['API keys', 'Domain authentication'],
                        'links': ['https://sendgrid.com'],
                        'notes': 'For system emails and notifications'
                    },
                    {
                        'id': 'convertkit_setup',
                        'name': 'ConvertKit Integration',
                        'status': 'pending',
                        'description': 'Setup ConvertKit for creator marketing',
                        'required_info': ['Creator account', 'Landing pages'],
                        'links': ['https://convertkit.com'],
                        'notes': 'Advanced automation features'
                    }
                ]
            },
            {
                'category_id': 'analytics_tracking',
                'name': 'Analytics & Tracking',
                'icon': 'fas fa-chart-line',
                'priority': 'medium',
                'description': 'Setup comprehensive analytics and tracking systems',
                'estimated_time': '2-3 hours',
                'items': [
                    {
                        'id': 'google_analytics',
                        'name': 'Google Analytics 4',
                        'status': 'pending',
                        'description': 'Setup GA4 for website analytics',
                        'required_info': ['Website verification', 'Goal setup'],
                        'links': ['https://analytics.google.com'],
                        'notes': 'Essential for tracking conversions'
                    },
                    {
                        'id': 'facebook_pixel',
                        'name': 'Facebook Pixel',
                        'status': 'pending',
                        'description': 'Install Facebook Pixel for ad tracking',
                        'required_info': ['Pixel ID', 'Event setup'],
                        'links': ['https://business.facebook.com/events_manager'],
                        'notes': 'Critical for Facebook ad optimization'
                    },
                    {
                        'id': 'google_tag_manager',
                        'name': 'Google Tag Manager',
                        'status': 'pending',
                        'description': 'Setup GTM for advanced tracking',
                        'required_info': ['Container setup', 'Tag configuration'],
                        'links': ['https://tagmanager.google.com'],
                        'notes': 'Centralized tag management'
                    },
                    {
                        'id': 'hotjar_heatmaps',
                        'name': 'Hotjar Heatmaps',
                        'status': 'pending',
                        'description': 'Install Hotjar for user behavior analysis',
                        'required_info': ['Site ID', 'Recording setup'],
                        'links': ['https://hotjar.com'],
                        'notes': 'Understand user behavior patterns'
                    }
                ]
            },
            {
                'category_id': 'business_accounts',
                'name': 'Business Service Accounts',
                'icon': 'fas fa-building',
                'priority': 'medium',
                'description': 'Setup essential business service accounts',
                'estimated_time': '3-4 hours',
                'items': [
                    {
                        'id': 'google_workspace',
                        'name': 'Google Workspace',
                        'status': 'pending',
                        'description': 'Setup professional email and collaboration',
                        'required_info': ['Domain verification', 'User accounts'],
                        'links': ['https://workspace.google.com'],
                        'notes': 'Professional email addresses'
                    },
                    {
                        'id': 'slack_workspace',
                        'name': 'Slack Workspace',
                        'status': 'pending',
                        'description': 'Team communication platform',
                        'required_info': ['Workspace name', 'Channel setup'],
                        'links': ['https://slack.com'],
                        'notes': 'Internal team coordination'
                    },
                    {
                        'id': 'notion_workspace',
                        'name': 'Notion Workspace',
                        'status': 'pending',
                        'description': 'Knowledge management and documentation',
                        'required_info': ['Team setup', 'Template library'],
                        'links': ['https://notion.so'],
                        'notes': 'Project management and docs'
                    },
                    {
                        'id': 'zapier_account',
                        'name': 'Zapier Automation',
                        'status': 'pending',
                        'description': 'Workflow automation platform',
                        'required_info': ['App connections', 'Zap creation'],
                        'links': ['https://zapier.com'],
                        'notes': 'Connect all tools together'
                    }
                ]
            },
            {
                'category_id': 'telegram_setup',
                'name': 'Telegram Bot Configuration',
                'icon': 'fab fa-telegram-plane',
                'priority': 'high',
                'description': 'Complete Telegram bot setup and integrations',
                'estimated_time': '1-2 hours',
                'items': [
                    {
                        'id': 'telegram_bot_token',
                        'name': 'Bot Token Configuration',
                        'status': 'pending',
                        'description': 'Configure TELEGRAM_BOT_TOKEN environment variable',
                        'required_info': ['Bot token from @BotFather'],
                        'links': ['https://t.me/BotFather'],
                        'notes': 'Required for bot functionality'
                    },
                    {
                        'id': 'telegram_group_setup',
                        'name': 'Payment Notification Group',
                        'status': 'completed',
                        'description': 'Group chat configured for payment notifications',
                        'required_info': ['Group chat ID: -1001987654321'],
                        'links': ['/telegram-payment-link'],
                        'notes': 'Group ID already configured'
                    },
                    {
                        'id': 'webhook_setup',
                        'name': 'Webhook Configuration',
                        'status': 'pending',
                        'description': 'Setup webhook for real-time bot updates',
                        'required_info': ['Domain URL', 'SSL certificate'],
                        'links': ['/webhook/telegram'],
                        'notes': 'For instant message processing'
                    }
                ]
            }
        ]
        
        # Calculate overall progress
        total_items = sum(len(cat['items']) for cat in categories)
        completed_items = sum(len([item for item in cat['items'] if item['status'] == 'completed']) for cat in categories)
        overall_progress = round((completed_items / total_items) * 100, 1) if total_items > 0 else 0
        
        return jsonify({
            'categories': categories,
            'summary': {
                'total_categories': len(categories),
                'total_items': total_items,
                'completed_items': completed_items,
                'overall_progress': overall_progress,
                'high_priority_categories': len([c for c in categories if c['priority'] == 'high']),
                'estimated_total_time': '12-20 hours'
            }
        })
        
    except Exception as e:
        logger.error(f"Checklist categories error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@setup_checklist_bp.route('/api/update-checklist-item', methods=['POST'])
def update_checklist_item():
    """Update status of a checklist item"""
    try:
        data = request.get_json()
        item_id = data.get('item_id')
        status = data.get('status')  # completed, pending, in_progress
        notes = data.get('notes', '')
        
        # In a real implementation, this would update a database
        # For now, we'll return a success response
        
        return jsonify({
            'status': 'success',
            'message': f'Item {item_id} updated to {status}',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@setup_checklist_bp.route('/api/checklist-templates')
def checklist_templates():
    """Get pre-built checklist templates for different business types"""
    try:
        templates = [
            {
                'template_id': 'ecommerce_startup',
                'name': 'E-commerce Startup',
                'description': 'Complete setup for online store and product sales',
                'categories': ['payment_systems', 'social_accounts', 'email_marketing', 'analytics_tracking'],
                'estimated_time': '8-12 hours',
                'priority_items': ['stripe_setup', 'facebook_business', 'google_analytics']
            },
            {
                'template_id': 'saas_business',
                'name': 'SaaS Business',
                'description': 'Software as a Service business setup',
                'categories': ['payment_systems', 'business_accounts', 'analytics_tracking', 'email_marketing'],
                'estimated_time': '10-15 hours',
                'priority_items': ['stripe_setup', 'google_workspace', 'sendgrid_api']
            },
            {
                'template_id': 'affiliate_marketing',
                'name': 'Affiliate Marketing',
                'description': 'Affiliate marketing business setup',
                'categories': ['social_accounts', 'email_marketing', 'analytics_tracking', 'telegram_setup'],
                'estimated_time': '6-10 hours',
                'priority_items': ['facebook_business', 'mailchimp_setup', 'telegram_bot_token']
            },
            {
                'template_id': 'consulting_service',
                'name': 'Consulting Service',
                'description': 'Professional consulting business setup',
                'categories': ['business_accounts', 'social_accounts', 'payment_systems'],
                'estimated_time': '5-8 hours',
                'priority_items': ['linkedin_company', 'google_workspace', 'stripe_setup']
            }
        ]
        
        return jsonify({
            'templates': templates,
            'total_templates': len(templates)
        })
        
    except Exception as e:
        logger.error(f"Checklist templates error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@setup_checklist_bp.route('/api/generate-setup-guide', methods=['POST'])
def generate_setup_guide():
    """Generate step-by-step setup guide for selected items"""
    try:
        data = request.get_json()
        item_ids = data.get('item_ids', [])
        
        # Generate comprehensive setup guide
        setup_guide = {
            'guide_id': f"GUIDE-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'created_at': datetime.now().isoformat(),
            'total_steps': len(item_ids),
            'estimated_time': f"{len(item_ids) * 30}-{len(item_ids) * 60} minutes",
            'steps': []
        }
        
        # Example step generation (would be more detailed in real implementation)
        for i, item_id in enumerate(item_ids, 1):
            step = {
                'step_number': i,
                'item_id': item_id,
                'title': f"Setup {item_id.replace('_', ' ').title()}",
                'estimated_time': '30-60 minutes',
                'difficulty': 'intermediate',
                'prerequisites': ['Previous steps completed'],
                'instructions': [
                    f"Navigate to the official website for {item_id}",
                    "Create new business account",
                    "Complete verification process",
                    "Configure API keys and webhooks",
                    "Test integration with OMNI Empire system"
                ],
                'common_issues': [
                    "Verification delays",
                    "API key configuration errors",
                    "Domain verification problems"
                ],
                'success_criteria': [
                    "Account successfully created",
                    "Integration working properly",
                    "Test transactions processed"
                ]
            }
            setup_guide['steps'].append(step)
        
        return jsonify({
            'status': 'success',
            'setup_guide': setup_guide
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500