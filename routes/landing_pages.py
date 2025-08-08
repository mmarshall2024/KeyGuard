from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, BotConfig
import json
import os
from datetime import datetime, timedelta

landing_pages_bp = Blueprint('landing_pages', __name__)

# Business niche configurations
BUSINESS_NICHES = {
    "ai_automation": {
        "title": "AI Automation Solutions",
        "tagline": "Transform Your Business with Intelligent Automation",
        "description": "Deploy AI-powered bots that automate workflows, analyze data, and optimize operations 24/7",
        "primary_color": "#6366f1",
        "secondary_color": "#8b5cf6",
        "icon": "🤖",
        "features": [
            "Custom AI Bot Development",
            "Workflow Automation",
            "Data Analysis & Insights",
            "24/7 Intelligent Monitoring"
        ],
        "pricing": {
            "starter": {"price": 99, "features": ["Basic AI Bot", "Email Support", "5 Workflows"]},
            "professional": {"price": 299, "features": ["Advanced AI Bots", "Priority Support", "25 Workflows", "API Access"]},
            "enterprise": {"price": 999, "features": ["Custom AI Solutions", "Dedicated Support", "Unlimited Workflows", "White-label Options"]}
        }
    },
    "financial_legal": {
        "title": "Financial & Legal Automation",
        "tagline": "Secure Your Assets with Smart Legal Technology",
        "description": "AI-powered legal bots for asset protection, tax optimization, and contract automation",
        "primary_color": "#059669",
        "secondary_color": "#10b981",
        "icon": "⚖️",
        "features": [
            "Asset Protection Strategies",
            "Tax Optimization Bots",
            "Contract Generation",
            "Legal Compliance Monitoring"
        ],
        "pricing": {
            "starter": {"price": 199, "features": ["Basic Legal Bot", "Contract Templates", "Tax Calculator"]},
            "professional": {"price": 599, "features": ["Advanced Legal Automation", "Asset Protection Plans", "Priority Consultation"]},
            "enterprise": {"price": 1999, "features": ["Custom Legal Solutions", "Dedicated Legal Expert", "Full Compliance Suite"]}
        }
    },
    "content_media": {
        "title": "Content & Media Automation",
        "tagline": "Create Viral Content at Scale",
        "description": "AI-powered content creation, branding, and social media automation for maximum engagement",
        "primary_color": "#dc2626",
        "secondary_color": "#f97316",
        "icon": "🎬",
        "features": [
            "Viral Content Generation",
            "Brand Identity Creation",
            "Social Media Automation",
            "Influencer Dashboard"
        ],
        "pricing": {
            "starter": {"price": 79, "features": ["Content Templates", "Basic Automation", "5 Social Accounts"]},
            "professional": {"price": 249, "features": ["AI Content Creation", "Brand Kit", "25 Social Accounts", "Analytics"]},
            "enterprise": {"price": 799, "features": ["Custom Content Strategy", "Unlimited Accounts", "Priority Support", "Agency Tools"]}
        }
    },
    "sales_marketing": {
        "title": "Sales & Marketing Automation",
        "tagline": "Convert Leads into Revenue Automatically",
        "description": "Intelligent sales funnels, automated closing, and advanced analytics for maximum conversions",
        "primary_color": "#7c3aed",
        "secondary_color": "#a855f7",
        "icon": "📈",
        "features": [
            "AI Sales Funnels",
            "Automated Lead Closing",
            "Customer Analytics",
            "Conversion Optimization"
        ],
        "pricing": {
            "starter": {"price": 149, "features": ["Basic Sales Funnel", "Lead Capture", "Email Automation"]},
            "professional": {"price": 449, "features": ["Advanced Funnels", "AI Closing Bot", "Analytics Dashboard", "A/B Testing"]},
            "enterprise": {"price": 1499, "features": ["Custom Sales Solutions", "Dedicated Account Manager", "Enterprise Integrations"]}
        }
    },
    "education_training": {
        "title": "Education & Training Platforms",
        "tagline": "Scale Learning with AI-Powered Education",
        "description": "Intelligent curriculum development, automated certification, and cohort management systems",
        "primary_color": "#0891b2",
        "secondary_color": "#06b6d4",
        "icon": "🎓",
        "features": [
            "AI Curriculum Development",
            "Automated Certification",
            "Cohort Management",
            "Progress Tracking"
        ],
        "pricing": {
            "starter": {"price": 89, "features": ["Course Templates", "Basic Tracking", "50 Students"]},
            "professional": {"price": 289, "features": ["AI Course Creation", "Certification System", "500 Students", "Analytics"]},
            "enterprise": {"price": 889, "features": ["Custom Learning Platform", "Unlimited Students", "White-label Options"]}
        }
    },
    "ecommerce_products": {
        "title": "E-commerce & Product Automation",
        "tagline": "Automate Your Online Store Operations",
        "description": "Product development, inventory management, and fulfillment automation for maximum profitability",
        "primary_color": "#ea580c",
        "secondary_color": "#f97316",
        "icon": "🛒",
        "features": [
            "Product Development Automation",
            "Inventory Management",
            "Order Fulfillment Bots",
            "Customer Service Automation"
        ],
        "pricing": {
            "starter": {"price": 69, "features": ["Basic Store Setup", "Inventory Tracking", "Order Processing"]},
            "professional": {"price": 219, "features": ["Automated Marketing", "Customer Service Bot", "Analytics Dashboard"]},
            "enterprise": {"price": 699, "features": ["Custom E-commerce Solution", "Advanced Automation", "Multi-store Management"]}
        }
    }
}

@landing_pages_bp.route('/')
def landing_home():
    """Main landing page with niche selection"""
    return render_template('landing/home.html', niches=BUSINESS_NICHES)

@landing_pages_bp.route('/niche/<niche_id>')
def niche_landing(niche_id):
    """Niche-specific landing page"""
    if niche_id not in BUSINESS_NICHES:
        flash('Business niche not found', 'error')
        return redirect(url_for('landing_pages.landing_home'))
    
    niche = BUSINESS_NICHES[niche_id]
    return render_template('landing/niche.html', niche=niche, niche_id=niche_id)

@landing_pages_bp.route('/demo/<niche_id>')
def niche_demo(niche_id):
    """Interactive demo for specific niche"""
    if niche_id not in BUSINESS_NICHES:
        return jsonify({'error': 'Niche not found'}), 404
    
    niche = BUSINESS_NICHES[niche_id]
    return render_template('landing/demo.html', niche=niche, niche_id=niche_id)

@landing_pages_bp.route('/api/demo/<niche_id>', methods=['POST'])
def api_demo(niche_id):
    """API endpoint for demo interactions"""
    if niche_id not in BUSINESS_NICHES:
        return jsonify({'error': 'Niche not found'}), 404
    
    data = request.json
    action = data.get('action')
    
    # Demo responses for each niche
    demo_responses = {
        "ai_automation": {
            "analyze_workflow": {
                "result": "🤖 AI Analysis Complete",
                "details": "Found 5 automation opportunities that could save 15 hours/week",
                "suggestions": ["Automate email responses", "Schedule social media posts", "Generate reports automatically"]
            },
            "create_automation": {
                "result": "✅ Bot Created Successfully",
                "details": "Your custom AI bot is ready with advanced natural language processing",
                "next_steps": ["Configure workflows", "Set up triggers", "Deploy to production"]
            }
        },
        "financial_legal": {
            "analyze": {
                "result": "⚖️ Asset Protection Plan Generated",
                "details": "Identified 3 key strategies to protect $500K+ in assets",
                "recommendations": ["LLC Structure", "Asset Trusts", "Offshore Accounts"]
            },
            "generate": {
                "result": "💰 Tax Savings Identified",
                "details": "Potential annual savings: $25,000 through strategic optimization",
                "strategies": ["Business deductions", "Investment structures", "Retirement planning"]
            }
        },
        "content_media": {
            "generate": {
                "result": "🎬 Viral Content Created",
                "details": "Generated 10 high-engagement posts with trending hashtags",
                "content": ["Video script ready", "Social media posts", "Blog article outline"]
            },
            "analyze": {
                "result": "🎨 Brand Strategy Complete",
                "details": "Custom brand identity with color palette and messaging guide",
                "deliverables": ["Logo concepts", "Brand guidelines", "Content calendar"]
            }
        }
    }
    
    niche_demos = demo_responses.get(niche_id, {})
    response = niche_demos.get(action, {
        "result": "✅ Demo Action Complete",
        "details": f"Successfully demonstrated {action} for {niche_id}",
        "next_steps": ["Get started with full version", "Schedule consultation", "View pricing"]
    })
    
    return jsonify(response)

@landing_pages_bp.route('/signup/<niche_id>/<plan>', methods=['POST'])
def signup(niche_id, plan):
    """Handle signup for specific niche and plan"""
    if niche_id not in BUSINESS_NICHES:
        return jsonify({'error': 'Invalid niche'}), 400
    
    niche = BUSINESS_NICHES[niche_id]
    if plan not in niche['pricing']:
        return jsonify({'error': 'Invalid plan'}), 400
    
    data = request.json
    email = data.get('email')
    name = data.get('name')
    
    if not email or not name:
        return jsonify({'error': 'Name and email required'}), 400
    
    # Store signup information
    signup_data = {
        'niche': niche_id,
        'plan': plan,
        'email': email,
        'name': name,
        'price': niche['pricing'][plan]['price'],
        'timestamp': str(db.func.now())
    }
    
    # In production, this would integrate with Stripe and email systems
    # For now, we'll store in config
    try:
        config = BotConfig.query.filter_by(key=f'signup_{niche_id}_{email}').first()
        if not config:
            config = BotConfig(key=f'signup_{niche_id}_{email}', value=json.dumps(signup_data))
            db.session.add(config)
        else:
            config.value = json.dumps(signup_data)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Signup successful! Check your email for next steps.',
            'redirect_url': f'/landing/onboarding/{niche_id}?plan={plan}&email={email}'
        })
    except Exception as e:
        return jsonify({'error': 'Signup failed, please try again'}), 500

@landing_pages_bp.route('/onboarding/<niche_id>')
def onboarding(niche_id):
    """Onboarding flow for new signups"""
    if niche_id not in BUSINESS_NICHES:
        flash('Invalid access', 'error')
        return redirect(url_for('landing_pages.landing_home'))
    
    plan = request.args.get('plan')
    email = request.args.get('email')
    
    niche = BUSINESS_NICHES[niche_id]
    return render_template('landing/onboarding.html', 
                         niche=niche, 
                         niche_id=niche_id, 
                         plan=plan, 
                         email=email)

@landing_pages_bp.route('/success/<niche_id>')
def success(niche_id):
    """Success page after completion"""
    if niche_id not in BUSINESS_NICHES:
        return redirect(url_for('landing_pages.landing_home'))
    
    niche = BUSINESS_NICHES[niche_id]
    return render_template('landing/success.html', niche=niche, niche_id=niche_id)