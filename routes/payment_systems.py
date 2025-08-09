from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
import stripe
import os
import json
import logging
from datetime import datetime

payment_systems_bp = Blueprint('payment_systems', __name__)
logger = logging.getLogger(__name__)

# Configure Stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

@payment_systems_bp.route('/payment-dashboard')
def payment_dashboard():
    """Complete payment systems dashboard"""
    return render_template('payment_systems/dashboard.html')

@payment_systems_bp.route('/create-stripe-session', methods=['POST'])
def create_stripe_session():
    """Create Stripe checkout session for any product"""
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        product_name = data.get('product_name', 'OMNI Empire Product')
        amount = int(data.get('amount', 29700))  # Amount in cents
        
        YOUR_DOMAIN = os.environ.get('REPLIT_DEV_DOMAIN') if os.environ.get('REPLIT_DEPLOYMENT') != '' else os.environ.get('REPLIT_DOMAINS', 'localhost:5000').split(',')[0]
        
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product_name,
                        'description': f'Premium {product_name} from OMNI Empire'
                    },
                    'unit_amount': amount,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f'https://{YOUR_DOMAIN}/payment-success?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=f'https://{YOUR_DOMAIN}/empire',
            metadata={
                'product_id': product_id,
                'product_name': product_name
            }
        )
        
        return jsonify({'checkout_url': checkout_session.url})
        
    except Exception as e:
        logger.error(f"Stripe session creation error: {str(e)}")
        return jsonify({'error': str(e)}), 400

@payment_systems_bp.route('/payment-success')
def payment_success():
    """Handle successful payments"""
    session_id = request.args.get('session_id')
    
    if session_id:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            
            # Record revenue (import models within function to avoid circular imports)
            from app import db
            from models_business import Revenue
            
            revenue = Revenue(
                amount=session.amount_total / 100,  # Convert from cents
                currency='USD',
                source='stripe',
                transaction_id=session.payment_intent,
                product_name=session.metadata.get('product_name', 'Unknown'),
                created_at=datetime.utcnow()
            )
            db.session.add(revenue)
            db.session.commit()
            
            return render_template('payment_systems/success.html', session=session)
            
        except Exception as e:
            logger.error(f"Payment success handling error: {str(e)}")
            flash('Payment completed but there was an issue recording it.', 'warning')
    
    return redirect(url_for('revenue_landing.empire'))

@payment_systems_bp.route('/crypto-payment', methods=['POST'])
def crypto_payment():
    """Handle cryptocurrency payments"""
    try:
        data = request.get_json()
        crypto_type = data.get('crypto_type', 'bitcoin')
        amount = data.get('amount')
        product_name = data.get('product_name')
        
        # Generate crypto payment address (simplified - in production use proper crypto payment processor)
        crypto_addresses = {
            'bitcoin': '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
            'ethereum': '0x742d35Cc6634C0532925a3b8D4Ff3c74BF5fE99C',
            'usdt': '0x742d35Cc6634C0532925a3b8D4Ff3c74BF5fE99C',
            'usdc': '0x742d35Cc6634C0532925a3b8D4Ff3c74BF5fE99C'
        }
        
        payment_address = crypto_addresses.get(crypto_type)
        
        return jsonify({
            'payment_address': payment_address,
            'amount': amount,
            'crypto_type': crypto_type,
            'qr_code_url': f'/generate-crypto-qr?address={payment_address}&amount={amount}&crypto={crypto_type}'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@payment_systems_bp.route('/paypal-payment', methods=['POST'])
def paypal_payment():
    """Handle PayPal payments"""
    try:
        data = request.get_json()
        amount = data.get('amount')
        product_name = data.get('product_name')
        
        # PayPal payment setup (simplified)
        paypal_data = {
            'business_email': 'payments@omnimpire.com',
            'amount': amount,
            'item_name': product_name,
            'return_url': f"{request.host_url}payment-success",
            'cancel_return': f"{request.host_url}empire"
        }
        
        return jsonify(paypal_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@payment_systems_bp.route('/apple-pay', methods=['POST'])
def apple_pay():
    """Handle Apple Pay payments"""
    try:
        data = request.get_json()
        amount = data.get('amount')
        
        # Apple Pay integration (requires Apple Pay certificate and merchant ID)
        apple_pay_data = {
            'merchant_id': 'merchant.com.omnimpire.payments',
            'amount': amount,
            'currency': 'USD',
            'supported_networks': ['visa', 'masterCard', 'amex', 'discover']
        }
        
        return jsonify(apple_pay_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@payment_systems_bp.route('/google-pay', methods=['POST'])
def google_pay():
    """Handle Google Pay payments"""
    try:
        data = request.get_json()
        amount = data.get('amount')
        
        # Google Pay integration
        google_pay_data = {
            'merchant_id': 'omnimpire_payments',
            'amount': amount,
            'currency': 'USD',
            'gateway': 'stripe',
            'gateway_merchant_id': os.environ.get('STRIPE_PUBLISHABLE_KEY', '').split('_')[1] if os.environ.get('STRIPE_PUBLISHABLE_KEY') else 'test'
        }
        
        return jsonify(google_pay_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@payment_systems_bp.route('/bank-transfer', methods=['POST'])
def bank_transfer():
    """Handle bank transfer payments"""
    try:
        data = request.get_json()
        amount = data.get('amount')
        product_name = data.get('product_name')
        
        # Bank transfer details
        bank_details = {
            'bank_name': 'OMNI Empire Business Account',
            'account_number': 'OMNI-****-****-1234',
            'routing_number': '123456789',
            'swift_code': 'OMNIBUS1',
            'reference': f'OMNI-{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'amount': amount,
            'instructions': f'Please include reference number in transfer memo for {product_name}'
        }
        
        return jsonify(bank_details)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@payment_systems_bp.route('/payment-plans', methods=['POST'])
def payment_plans():
    """Create installment payment plans"""
    try:
        data = request.get_json()
        total_amount = data.get('total_amount')
        plan_type = data.get('plan_type', '3_months')
        
        plan_options = {
            '3_months': {'installments': 3, 'fee': 0.05},
            '6_months': {'installments': 6, 'fee': 0.08},
            '12_months': {'installments': 12, 'fee': 0.12}
        }
        
        plan = plan_options.get(plan_type)
        if plan:
            fee_amount = total_amount * plan['fee']
            total_with_fee = total_amount + fee_amount
            monthly_payment = total_with_fee / plan['installments']
            
            return jsonify({
                'plan_type': plan_type,
                'total_amount': total_amount,
                'fee_amount': fee_amount,
                'total_with_fee': total_with_fee,
                'monthly_payment': round(monthly_payment, 2),
                'installments': plan['installments']
            })
        
        return jsonify({'error': 'Invalid payment plan'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@payment_systems_bp.route('/webhook/stripe', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhooks"""
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        # Verify webhook signature (you'll need to set STRIPE_WEBHOOK_SECRET)
        webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')
        if webhook_secret:
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        else:
            event = json.loads(payload)
        
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            
            # Record successful payment
            from app import db
            from models_business import Revenue
            
            revenue = Revenue(
                amount=session['amount_total'] / 100,
                currency='USD',
                source='stripe_webhook',
                transaction_id=session['payment_intent'],
                product_name=session.get('metadata', {}).get('product_name', 'Unknown'),
                created_at=datetime.utcnow()
            )
            db.session.add(revenue)
            db.session.commit()
            
            logger.info(f"Payment recorded: ${revenue.amount} for {revenue.product_name}")
        
        return jsonify({'status': 'success'})
        
    except Exception as e:
        logger.error(f"Stripe webhook error: {str(e)}")
        return jsonify({'error': str(e)}), 400

@payment_systems_bp.route('/payment-analytics')
def payment_analytics():
    """Payment systems analytics"""
    try:
        from app import db
        from models_business import Revenue
        
        # Get payment statistics
        total_revenue = db.session.query(db.func.sum(Revenue.amount)).scalar() or 0
        payment_count = Revenue.query.count()
        avg_payment = total_revenue / payment_count if payment_count > 0 else 0
        
        # Revenue by source
        revenue_by_source = db.session.query(
            Revenue.source, 
            db.func.sum(Revenue.amount), 
            db.func.count(Revenue.id)
        ).group_by(Revenue.source).all()
        
        analytics_data = {
            'total_revenue': round(total_revenue, 2),
            'payment_count': payment_count,
            'average_payment': round(avg_payment, 2),
            'revenue_by_source': [
                {'source': source, 'amount': float(amount), 'count': count}
                for source, amount, count in revenue_by_source
            ]
        }
        
        return jsonify(analytics_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400