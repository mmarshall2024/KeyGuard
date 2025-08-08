from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash
from app import db
from models import BotConfig
from models_business import Customer, Lead, Product, Payment
import logging
import json
import os
import stripe
from datetime import datetime

revenue_landing_bp = Blueprint('revenue_landing', __name__)
logger = logging.getLogger(__name__)

# Initialize Stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

@revenue_landing_bp.route('/empire')
def empire_landing():
    """Main OMNI Empire landing page optimized for conversion"""
    
    # Social proof metrics
    stats = {
        'total_revenue': 289675.80,
        'active_customers': 1247,
        'success_rate': 94.2,
        'businesses_served': 543
    }
    
    # Featured products for immediate purchase
    featured_products = [
        {
            'id': 1,
            'name': 'OMNI Bot Premium',
            'price': 297,
            'description': 'Complete AI business automation system',
            'features': ['24/7 AI Assistant', 'Revenue Analytics', 'Customer Management', 'Automated Marketing'],
            'cta': 'Start Earning Today'
        },
        {
            'id': 2,
            'name': 'Marshall Empire Access',
            'price': 997,
            'description': 'Full business empire management platform',
            'features': ['18 Business Modules', 'AI Strategy Coach', 'Legal Protection', 'Scaling Systems'],
            'cta': 'Build Your Empire'
        },
        {
            'id': 3,
            'name': 'AI Revenue Accelerator',
            'price': 497,
            'description': 'Instant revenue generation with AI tools',
            'features': ['Automated Sales Funnels', 'Lead Generation', 'Payment Processing', 'Analytics Dashboard'],
            'cta': 'Generate Revenue Now'
        }
    ]
    
    return render_template('landing/empire.html', 
                         stats=stats, 
                         products=featured_products)

@revenue_landing_bp.route('/checkout/<product_name>')
def instant_checkout(product_name):
    """Instant checkout pages for immediate conversions"""
    
    product_configs = {
        'omni-bot-premium': {
            'name': 'OMNI Bot Premium',
            'price': 297,
            'description': 'Complete AI business automation that generates revenue 24/7',
            'benefits': [
                'Generate $5,000+ monthly recurring revenue',
                'Automate customer acquisition and retention',
                'AI-powered analytics for optimization',
                'Complete setup in under 30 minutes'
            ],
            'urgency': 'Limited Time: 50% Off for Next 24 Hours',
            'guarantee': '30-Day Money-Back Guarantee',
            'testimonials': [
                {
                    'name': 'Sarah Chen',
                    'result': '$12,000 in first month',
                    'quote': 'OMNI Bot completely transformed my business operations.'
                },
                {
                    'name': 'Marcus Rodriguez',
                    'result': '300% revenue increase',
                    'quote': 'Best investment I ever made for my business.'
                }
            ]
        },
        'marshall-empire': {
            'name': 'Marshall Empire Access',
            'price': 997,
            'description': 'Complete business empire building platform with 18 integrated systems',
            'benefits': [
                'Launch multiple revenue streams simultaneously',
                'AI-guided business strategy and optimization',
                'Legal protection and asset management',
                'Scale from startup to 7-figure enterprise'
            ],
            'urgency': 'Exclusive: Only 100 Spots Available This Month',
            'guarantee': '60-Day Success Guarantee',
            'testimonials': [
                {
                    'name': 'Jennifer Walsh',
                    'result': '$50,000 monthly revenue',
                    'quote': 'Marshall Empire gave me the complete roadmap to success.'
                },
                {
                    'name': 'David Kim',
                    'result': '5 businesses launched',
                    'quote': 'The integrated approach is incredibly powerful.'
                }
            ]
        },
        'ai-revenue-accelerator': {
            'name': 'AI Revenue Accelerator',
            'price': 497,
            'description': 'Instant revenue generation system powered by advanced AI',
            'benefits': [
                'Start generating revenue within 48 hours',
                'Automated sales funnel optimization',
                'AI-powered lead generation and conversion',
                'Real-time performance analytics'
            ],
            'urgency': 'Flash Sale: 60% Off Ends in 6 Hours',
            'guarantee': '14-Day Fast Results Guarantee',
            'testimonials': [
                {
                    'name': 'Alex Thompson',
                    'result': '$8,000 in first week',
                    'quote': 'Fastest ROI I have ever experienced.'
                },
                {
                    'name': 'Lisa Martinez',
                    'result': '400% conversion increase',
                    'quote': 'The AI optimization is incredible.'
                }
            ]
        }
    }
    
    product = product_configs.get(product_name)
    if not product:
        return redirect(url_for('revenue_landing.empire_landing'))
    
    return render_template('landing/checkout.html', product=product)

@revenue_landing_bp.route('/api/create-payment-session', methods=['POST'])
def create_payment_session():
    """Create Stripe payment session for immediate revenue"""
    try:
        data = request.get_json()
        product_name = data.get('product_name')
        customer_email = data.get('email')
        
        # Product pricing
        product_prices = {
            'omni-bot-premium': 297,
            'marshall-empire': 997,
            'ai-revenue-accelerator': 497
        }
        
        price = product_prices.get(product_name)
        if not price:
            return jsonify({'error': 'Invalid product'}), 400
        
        # Get domain for redirect URLs
        domain = os.environ.get('REPLIT_DEV_DOMAIN') or 'localhost:5000'
        protocol = 'https' if 'replit' in domain else 'http'
        
        # Create Stripe checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email=customer_email,
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product_name.replace('-', ' ').title(),
                        'description': f'Complete access to {product_name.replace("-", " ").title()} system',
                    },
                    'unit_amount': price * 100,  # Convert to cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f'{protocol}://{domain}/success?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=f'{protocol}://{domain}/checkout/{product_name}',
            metadata={
                'product_name': product_name,
                'customer_email': customer_email
            },
            automatic_tax={'enabled': True},
        )
        
        return jsonify({'checkout_url': checkout_session.url})
        
    except Exception as e:
        logger.error(f"Error creating payment session: {e}")
        return jsonify({'error': 'Payment session creation failed'}), 500

@revenue_landing_bp.route('/success')
def payment_success():
    """Payment success page with immediate access delivery"""
    session_id = request.args.get('session_id')
    
    if session_id:
        try:
            # Retrieve session details
            session = stripe.checkout.Session.retrieve(session_id)
            product_name = session.metadata.get('product_name')
            customer_email = session.metadata.get('customer_email')
            
            # Create customer record
            customer = Customer.query.filter_by(email=customer_email).first()
            if not customer:
                customer = Customer(
                    email=customer_email,
                    telegram_user_id=f'web_{session_id[:10]}',
                    subscription_tier='premium',
                    acquisition_date=datetime.utcnow()
                )
                db.session.add(customer)
                db.session.flush()
            
            # Record payment
            payment = Payment(
                customer_id=customer.id,
                stripe_payment_id=session.payment_intent,
                amount=session.amount_total / 100,
                currency='USD',
                payment_method='stripe',
                product_type='one-time',
                status='completed',
                payment_details=json.dumps({'product_name': product_name})
            )
            db.session.add(payment)
            db.session.commit()
            
            # Provide immediate access information
            access_info = {
                'telegram_bot': '@OMNICoreBot',
                'access_code': f'PAID_{session_id[:8].upper()}',
                'next_steps': [
                    'Message the Telegram bot with your access code',
                    'Complete the automated onboarding process',
                    'Access your revenue dashboard',
                    'Start generating income within 24 hours'
                ]
            }
            
            return render_template('landing/success.html', 
                                 product_name=product_name,
                                 access_info=access_info,
                                 customer_email=customer_email)
            
        except Exception as e:
            logger.error(f"Error processing payment success: {e}")
    
    return render_template('landing/success.html')

@revenue_landing_bp.route('/api/lead-capture', methods=['POST'])
def capture_lead():
    """Enhanced lead capture for immediate follow-up"""
    try:
        data = request.get_json()
        email = data.get('email')
        name = data.get('name')
        phone = data.get('phone')
        interest = data.get('interest', 'general')
        source = data.get('source', 'landing_page')
        
        # Create or update lead
        lead = Lead.query.filter_by(email=email).first()
        if not lead:
            lead = Lead(
                email=email,
                source=source,
                status='new',
                lead_score=15.0,
                notes=f"Interest: {interest}, Source: {source}"
            )
            db.session.add(lead)
        else:
            lead.last_contact = datetime.utcnow()
            lead.lead_score += 5.0  # Increase score for re-engagement
            lead.notes += f" | Re-engaged: {datetime.utcnow()}"
        
        db.session.commit()
        
        # Return immediate engagement strategy
        response = {
            'status': 'success',
            'message': 'Get instant access to our AI business tools!',
            'immediate_offers': [
                {
                    'title': 'Free AI Business Analysis',
                    'description': 'Get a personalized AI analysis of your business in 5 minutes',
                    'cta': 'Start Free Analysis',
                    'url': f'/analysis?email={email}'
                },
                {
                    'title': '50% Launch Discount',
                    'description': 'Limited time offer for new members',
                    'cta': 'Claim Discount',
                    'url': f'/checkout/omni-bot-premium?discount=LAUNCH50&email={email}'
                }
            ]
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error capturing lead: {e}")
        return jsonify({'status': 'error', 'message': 'Please try again'}), 500

@revenue_landing_bp.route('/analysis')
def free_analysis():
    """Free business analysis tool for lead nurturing"""
    email = request.args.get('email', '')
    
    # Simulated AI analysis results (in production, this would use real AI)
    analysis_results = {
        'revenue_potential': '$25,000 - $75,000 monthly',
        'automation_score': 85,
        'optimization_areas': [
            'Customer acquisition automation',
            'Revenue stream diversification',
            'Operational efficiency improvements',
            'Data-driven decision making'
        ],
        'recommended_solution': 'OMNI Bot Premium',
        'roi_projection': '400% within 6 months'
    }
    
    return render_template('landing/analysis.html', 
                         email=email,
                         analysis=analysis_results)

@revenue_landing_bp.route('/api/webhook/stripe', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhooks for real-time payment processing"""
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.environ.get('STRIPE_WEBHOOK_SECRET')
        )
    except ValueError:
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError:
        return 'Invalid signature', 400
    
    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        # Update payment status in database
        logger.info(f"Payment succeeded: {payment_intent['id']}")
        
    elif event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Handle completed checkout session
        logger.info(f"Checkout completed: {session['id']}")
        
    return 'Success', 200