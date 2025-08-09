from flask import Blueprint, render_template, request, jsonify
from launch_empire import empire_launch

empire_bp = Blueprint('empire', __name__)

@empire_bp.route('/ceo-dashboard')
def ceo_dashboard():
    """CEO Dashboard for OMNI Empire Holdings"""
    
    # Get complete empire data
    empire_data = empire_launch.launch_holdings_company()
    ceo_data = empire_launch.generate_ceo_dashboard()
    
    return render_template('empire/ceo_dashboard.html', 
                         empire=empire_data, 
                         ceo=ceo_data)

@empire_bp.route('/api/launch-empire')
def api_launch_empire():
    """API endpoint to launch complete empire"""
    
    empire_data = empire_launch.launch_holdings_company()
    
    return jsonify({
        'status': 'success',
        'message': 'OMNI Empire Holdings Company fully launched',
        'data': empire_data
    })

@empire_bp.route('/api/empire-metrics')
def api_empire_metrics():
    """Get real-time empire metrics"""
    
    empire_data = empire_launch.launch_holdings_company()
    
    return jsonify({
        'status': 'success',
        'metrics': empire_data['empire_metrics'],
        'instant_payments': empire_data['instant_payment_status'],
        'timestamp': empire_data['launch_details']['launch_timestamp']
    })

@empire_bp.route('/api/activate-instant-payments')
def api_activate_instant_payments():
    """Activate instant payment processing"""
    
    payment_data = empire_launch._activate_instant_payments()
    
    return jsonify({
        'status': 'success',
        'message': 'Instant payments activated across all subsidiaries',
        'data': payment_data
    })