"""
Instant Money Generation Routes - Live payment processing
"""

from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import stripe
import os
import json
import logging
from datetime import datetime

instant_money = Blueprint('instant_money', __name__)
logger = logging.getLogger(__name__)

# Configure Stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

@instant_money.route('/instant-money')
def money_dashboard():
    """Instant money generation dashboard"""
    
    # Load active products
    try:
        with open('data/active_products.json', 'r') as f:
            products_data = json.load(f)
    except:
        products_data = {"products": [], "payment_links": []}
    
    return render_template('instant_money/dashboard.html', 
                         products=products_data.get('products', []),
                         payment_links=products_data.get('payment_links', []))

@instant_money.route('/buy/<product_id>')
def buy_product(product_id):
    """Direct product purchase page"""
    
    try:
        # Load product data
        with open('data/active_products.json', 'r') as f:
            products_data = json.load(f)
        
        # Find the specific product
        product = None
        for p in products_data.get('products', []):
            if p['product_id'] == product_id:
                product = p
                break
        
        if not product:
            return "Product not found", 404
        
        # Create checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': product['price_id'],
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.url_root + 'success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.url_root + 'cancel',
            automatic_tax={'enabled': True},
        )
        
        return redirect(session.url, code=303)
        
    except Exception as e:
        logger.error(f"Purchase error: {e}")
        return jsonify({"error": str(e)}), 500

@instant_money.route('/success')
def payment_success():
    """Payment success page"""
    session_id = request.args.get('session_id')
    
    if session_id:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            
            # Log the sale
            sale_data = {
                "session_id": session_id,
                "amount": session.amount_total / 100,
                "currency": session.currency,
                "customer_email": session.customer_details.email if session.customer_details else None,
                "timestamp": datetime.now().isoformat(),
                "status": "completed"
            }
            
            # Save sale record
            try:
                with open('data/sales_log.json', 'r') as f:
                    sales_log = json.load(f)
            except:
                sales_log = {"sales": []}
            
            sales_log["sales"].append(sale_data)
            
            with open('data/sales_log.json', 'w') as f:
                json.dump(sales_log, f, indent=2)
            
            return render_template('instant_money/success.html', 
                                 amount=sale_data['amount'],
                                 session=session)
                                 
        except Exception as e:
            logger.error(f"Success page error: {e}")
    
    return render_template('instant_money/success.html')

@instant_money.route('/cancel')
def payment_cancel():
    """Payment cancelled page"""
    return render_template('instant_money/cancel.html')

@instant_money.route('/api/sales-data')
def get_sales_data():
    """Get real sales data"""
    try:
        with open('data/sales_log.json', 'r') as f:
            sales_data = json.load(f)
        
        total_sales = len(sales_data.get('sales', []))
        total_revenue = sum(sale.get('amount', 0) for sale in sales_data.get('sales', []))
        
        return jsonify({
            "total_sales": total_sales,
            "total_revenue": total_revenue,
            "recent_sales": sales_data.get('sales', [])[-10:],  # Last 10 sales
            "last_updated": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "total_sales": 0,
            "total_revenue": 0,
            "recent_sales": [],
            "error": str(e)
        })

@instant_money.route('/api/create-instant-product', methods=['POST'])
def create_instant_product():
    """Create a new product instantly"""
    try:
        data = request.get_json()
        
        # Create Stripe product
        product = stripe.Product.create(
            name=data['name'],
            description=data.get('description', ''),
            type="service"
        )
        
        # Create price
        price = stripe.Price.create(
            unit_amount=int(data['price'] * 100),  # Convert to cents
            currency='usd',
            product=product.id
        )
        
        # Create payment link
        payment_link = stripe.PaymentLink.create(
            line_items=[{"price": price.id, "quantity": 1}]
        )
        
        product_data = {
            "product_id": product.id,
            "price_id": price.id,
            "payment_link": payment_link.url,
            "name": data['name'],
            "price_display": f"${data['price']:.0f}",
            "created_at": datetime.now().isoformat()
        }
        
        return jsonify({
            "success": True,
            "product": product_data,
            "message": "Product created successfully"
        })
        
    except Exception as e:
        logger.error(f"Product creation error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@instant_money.route('/webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhooks for real-time sales tracking"""
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        # Verify webhook signature (in production, use webhook secret)
        event = stripe.Event.construct_from(
            json.loads(payload), sig_header
        )
    except ValueError:
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError:
        return "Invalid signature", 400
    
    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Log the completed purchase
        sale_data = {
            "session_id": session['id'],
            "amount": session['amount_total'] / 100,
            "currency": session['currency'],
            "customer_email": session.get('customer_details', {}).get('email'),
            "timestamp": datetime.now().isoformat(),
            "status": "webhook_confirmed"
        }
        
        # Update sales log
        try:
            with open('data/sales_log.json', 'r') as f:
                sales_log = json.load(f)
        except:
            sales_log = {"sales": []}
        
        sales_log["sales"].append(sale_data)
        
        with open('data/sales_log.json', 'w') as f:
            json.dump(sales_log, f, indent=2)
        
        logger.info(f"New sale confirmed: ${sale_data['amount']}")
    
    return jsonify(success=True)