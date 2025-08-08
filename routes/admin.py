from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from models import Plugin, UpdateHistory, SystemMetrics, BotConfig
from plugin_manager import PluginManager  
from update_manager import UpdateManager
from app import db
import logging

admin_bp = Blueprint('admin', __name__)
logger = logging.getLogger(__name__)

@admin_bp.route('/')
def dashboard():
    """Admin dashboard"""
    # Get system metrics
    plugin_count = Plugin.query.count()
    active_plugins = Plugin.query.filter_by(enabled=True).count()
    
    recent_updates = UpdateHistory.query.order_by(
        UpdateHistory.started_at.desc()
    ).limit(5).all()
    
    # Get recent metrics
    recent_metrics = SystemMetrics.query.order_by(
        SystemMetrics.timestamp.desc()
    ).limit(50).all()
    
    return render_template('admin/dashboard.html',
                         plugin_count=plugin_count,
                         active_plugins=active_plugins,
                         recent_updates=recent_updates,
                         recent_metrics=recent_metrics)

@admin_bp.route('/plugins')
def plugins():
    """Plugin management page"""
    all_plugins = Plugin.query.all()
    plugin_manager = PluginManager()
    active_plugins = plugin_manager.get_active_plugins()
    
    return render_template('admin/plugins.html',
                         plugins=all_plugins,
                         active_plugins=active_plugins)

@admin_bp.route('/plugins/<plugin_name>/toggle', methods=['POST'])
def toggle_plugin(plugin_name):
    """Toggle plugin enabled/disabled state"""
    try:
        plugin_manager = PluginManager()
        plugin = Plugin.query.filter_by(name=plugin_name).first()
        
        if not plugin:
            return jsonify({'error': 'Plugin not found'}), 404
        
        if plugin.enabled:
            success = plugin_manager.disable_plugin(plugin_name)
            action = 'disabled'
        else:
            success = plugin_manager.enable_plugin(plugin_name)
            action = 'enabled'
        
        if success:
            return jsonify({'status': 'success', 'action': action})
        else:
            return jsonify({'error': f'Failed to {action} plugin'}), 500
            
    except Exception as e:
        logger.error(f"Error toggling plugin {plugin_name}: {e}")
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/plugins/<plugin_name>/reload', methods=['POST'])
def reload_plugin(plugin_name):
    """Reload a specific plugin"""
    try:
        plugin_manager = PluginManager()
        success = plugin_manager.reload_plugin(plugin_name)
        
        if success:
            return jsonify({'status': 'success'})
        else:
            return jsonify({'error': 'Failed to reload plugin'}), 500
            
    except Exception as e:
        logger.error(f"Error reloading plugin {plugin_name}: {e}")
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/updates')
def updates():
    """Update management page"""
    update_manager = UpdateManager()
    update_history = update_manager.get_update_history()
    
    # Check for available updates
    update_check = update_manager.check_for_updates()
    
    return render_template('admin/updates.html',
                         update_history=update_history,
                         update_check=update_check,
                         current_version=update_manager.current_version)

@admin_bp.route('/updates/check', methods=['POST'])
def check_updates():
    """Check for available updates"""
    try:
        update_manager = UpdateManager()
        result = update_manager.check_for_updates()
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error checking for updates: {e}")
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/updates/apply', methods=['POST'])
def apply_update():
    """Apply available updates"""
    try:
        update_manager = UpdateManager()
        result = update_manager.perform_update()
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error applying update: {e}")
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/updates/rollback/<int:update_id>', methods=['POST'])
def rollback_update(update_id):
    """Rollback to a specific update"""
    try:
        update_record = UpdateHistory.query.get(update_id)
        if not update_record or not update_record.backup_path:
            return jsonify({'error': 'Backup not found'}), 404
        
        update_manager = UpdateManager()
        update_manager.rollback_update(update_record.backup_path)
        
        return jsonify({'status': 'success'})
    except Exception as e:
        logger.error(f"Error rolling back update {update_id}: {e}")
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/telegram')
def telegram():
    """Telegram bot management"""
    return render_template('admin/telegram.html')

@admin_bp.route('/config')
def config():
    """Configuration management"""
    configs = BotConfig.query.all()
    return render_template('admin/config.html', configs=configs)

@admin_bp.route('/config/update', methods=['POST'])
def update_config():
    """Update configuration values"""
    try:
        key = request.form.get('key')
        value = request.form.get('value')
        encrypted = request.form.get('encrypted') == 'on'
        
        if not key or value is None:
            flash('Key and value are required', 'error')
            return redirect(url_for('admin.config'))
        
        config_item = BotConfig.query.filter_by(key=key).first()
        if config_item:
            config_item.value = value
            config_item.encrypted = encrypted
        else:
            config_item = BotConfig(key=key, value=value, encrypted=encrypted)
            db.session.add(config_item)
        
        db.session.commit()
        flash(f'Configuration {key} updated successfully', 'success')
        
    except Exception as e:
        logger.error(f"Error updating config: {e}")
        flash(f'Error updating configuration: {str(e)}', 'error')
    
    return redirect(url_for('admin.config'))

@admin_bp.route('/api/metrics')
def api_metrics():
    """API endpoint for real-time metrics"""
    try:
        from utils.health_monitor import HealthMonitor
        monitor = HealthMonitor()
        status = monitor.get_system_status()
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
