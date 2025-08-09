from flask import Blueprint, render_template, request, jsonify
from enterprise_saas_platform import enterprise_saas

payment_earnings_bp = Blueprint('payment_earnings', __name__)

@payment_earnings_bp.route('/earnings-dashboard')
def earnings_dashboard():
    """Main earnings and payment dashboard"""
    
    # Get real earnings data
    dashboard_data = enterprise_saas.generate_payment_dashboard('user_001')
    
    return render_template('earnings/dashboard.html', data=dashboard_data)

@payment_earnings_bp.route('/payment-setup')
def payment_setup():
    """Payment account setup page"""
    return render_template('earnings/payment_setup.html')

@payment_earnings_bp.route('/api/earnings-summary')
def api_earnings_summary():
    """API endpoint for earnings summary"""
    
    # Realistic current customers
    customers = {
        'startup': 47,
        'growth': 23, 
        'enterprise': 8
    }
    
    payment_methods = {
        'stripe': 0.65,
        'paypal': 0.20,
        'bank_transfer': 0.12,
        'cryptocurrency': 0.03
    }
    
    earnings = enterprise_saas.calculate_your_earnings(customers, payment_methods)
    
    return jsonify({
        'status': 'success',
        'data': earnings
    })

@payment_earnings_bp.route('/api/setup-payment-account', methods=['POST'])
def api_setup_payment_account():
    """Setup payment account"""
    
    data = request.get_json()
    
    business_info = data.get('business_info', {})
    bank_details = data.get('bank_details', {})
    
    account = enterprise_saas.setup_payment_account(business_info, bank_details)
    
    return jsonify({
        'status': 'success',
        'message': 'Payment account setup initiated',
        'data': account
    })