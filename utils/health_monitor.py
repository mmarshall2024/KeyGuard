import psutil
import requests
import logging
from datetime import datetime
from models import SystemMetrics
from app import db
from config import config

logger = logging.getLogger(__name__)

class HealthMonitor:
    """Monitor system health and performance"""
    
    def __init__(self):
        self.checks = {
            'bot_online': self._check_bot_status,
            'stripe_api': self._check_stripe_api,
            'devto_api': self._check_devto_api,
            'database': self._check_database,
            'disk_space': self._check_disk_space,
            'memory_usage': self._check_memory_usage,
            'cpu_usage': self._check_cpu_usage,
        }
    
    def get_system_status(self):
        """Get complete system health status"""
        status = {
            'healthy': True,
            'timestamp': datetime.utcnow().isoformat(),
            'checks': {},
            'metrics': {},
            'response_time': 0
        }
        
        start_time = datetime.utcnow()
        
        # Run all health checks
        for check_name, check_func in self.checks.items():
            try:
                result = check_func()
                status['checks'][check_name] = result
                
                if not result.get('healthy', True):
                    status['healthy'] = False
                    
            except Exception as e:
                logger.error(f"Health check {check_name} failed: {e}")
                status['checks'][check_name] = {
                    'healthy': False,
                    'error': str(e)
                }
                status['healthy'] = False
        
        # Calculate response time
        end_time = datetime.utcnow()
        response_time = (end_time - start_time).total_seconds() * 1000
        status['response_time'] = round(response_time, 2)
        
        # Store metrics
        self._store_metrics(status)
        
        return status
    
    def _check_bot_status(self):
        """Check if Telegram bot is responding"""
        try:
            # Simple check - try to get bot info
            url = f"https://api.telegram.org/bot{config.telegram_token}/getMe"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'healthy': data.get('ok', False),
                    'bot_username': data.get('result', {}).get('username'),
                    'last_check': datetime.utcnow().isoformat()
                }
            else:
                return {
                    'healthy': False,
                    'error': f"HTTP {response.status_code}"
                }
                
        except Exception as e:
            return {
                'healthy': False,
                'error': str(e)
            }
    
    def _check_stripe_api(self):
        """Check Stripe API connectivity"""
        try:
            import stripe
            stripe.api_key = config.stripe_secret_key
            
            # Try to retrieve account info
            account = stripe.Account.retrieve()
            
            return {
                'healthy': True,
                'account_id': account.id,
                'charges_enabled': account.charges_enabled,
                'last_check': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                'healthy': False,
                'error': str(e)
            }
    
    def _check_devto_api(self):
        """Check DEV.to API connectivity"""
        try:
            headers = {"api-key": config.devto_key}
            response = requests.get("https://dev.to/api/users/me", headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'healthy': True,
                    'username': data.get('username'),
                    'name': data.get('name'),
                    'last_check': datetime.utcnow().isoformat()
                }
            else:
                return {
                    'healthy': False,
                    'error': f"HTTP {response.status_code}"
                }
                
        except Exception as e:
            return {
                'healthy': False,
                'error': str(e)
            }
    
    def _check_database(self):
        """Check database connectivity and basic operations"""
        try:
            # Try a simple database operation
            from models import BotConfig
            count = BotConfig.query.count()
            
            return {
                'healthy': True,
                'config_count': count,
                'last_check': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                'healthy': False,
                'error': str(e)
            }
    
    def _check_disk_space(self):
        """Check available disk space"""
        try:
            disk_usage = psutil.disk_usage('.')
            free_percent = (disk_usage.free / disk_usage.total) * 100
            
            return {
                'healthy': free_percent > 10,  # Alert if less than 10% free
                'free_percent': round(free_percent, 2),
                'free_gb': round(disk_usage.free / (1024**3), 2),
                'total_gb': round(disk_usage.total / (1024**3), 2),
                'warning': free_percent < 20  # Warning if less than 20% free
            }
            
        except Exception as e:
            return {
                'healthy': False,
                'error': str(e)
            }
    
    def _check_memory_usage(self):
        """Check memory usage"""
        try:
            memory = psutil.virtual_memory()
            
            return {
                'healthy': memory.percent < 90,  # Alert if over 90%
                'used_percent': round(memory.percent, 2),
                'available_gb': round(memory.available / (1024**3), 2),
                'total_gb': round(memory.total / (1024**3), 2),
                'warning': memory.percent > 80  # Warning if over 80%
            }
            
        except Exception as e:
            return {
                'healthy': False,
                'error': str(e)
            }
    
    def _check_cpu_usage(self):
        """Check CPU usage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            return {
                'healthy': cpu_percent < 90,  # Alert if over 90%
                'usage_percent': round(cpu_percent, 2),
                'cpu_count': cpu_count,
                'load_avg': list(psutil.getloadavg()) if hasattr(psutil, 'getloadavg') else None,
                'warning': cpu_percent > 70  # Warning if over 70%
            }
            
        except Exception as e:
            return {
                'healthy': False,
                'error': str(e)
            }
    
    def _store_metrics(self, status):
        """Store metrics in database for historical analysis"""
        try:
            # Store key metrics
            metrics_to_store = [
                ('response_time', status['response_time']),
                ('system_healthy', 1 if status['healthy'] else 0)
            ]
            
            # Add resource metrics if available
            if 'cpu_usage' in status['checks']:
                cpu_data = status['checks']['cpu_usage']
                if 'usage_percent' in cpu_data:
                    metrics_to_store.append(('cpu_usage', cpu_data['usage_percent']))
            
            if 'memory_usage' in status['checks']:
                memory_data = status['checks']['memory_usage']
                if 'used_percent' in memory_data:
                    metrics_to_store.append(('memory_usage', memory_data['used_percent']))
            
            if 'disk_space' in status['checks']:
                disk_data = status['checks']['disk_space']
                if 'free_percent' in disk_data:
                    metrics_to_store.append(('disk_free_percent', disk_data['free_percent']))
            
            # Save metrics to database
            for metric_name, metric_value in metrics_to_store:
                metric = SystemMetrics(
                    metric_name=metric_name,
                    metric_value=float(metric_value),
                    timestamp=datetime.utcnow()
                )
                db.session.add(metric)
            
            db.session.commit()
            
        except Exception as e:
            logger.error(f"Failed to store metrics: {e}")
            db.session.rollback()
    
    def get_historical_metrics(self, metric_name, hours=24, limit=100):
        """Get historical metrics for analysis"""
        try:
            from datetime import timedelta
            
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            
            metrics = SystemMetrics.query.filter(
                SystemMetrics.metric_name == metric_name,
                SystemMetrics.timestamp >= cutoff_time
            ).order_by(SystemMetrics.timestamp.desc()).limit(limit).all()
            
            return [{
                'value': metric.metric_value,
                'timestamp': metric.timestamp.isoformat()
            } for metric in metrics]
            
        except Exception as e:
            logger.error(f"Failed to get historical metrics: {e}")
            return []
    
    def get_alerts(self):
        """Get current system alerts"""
        status = self.get_system_status()
        alerts = []
        
        for check_name, check_result in status['checks'].items():
            if not check_result.get('healthy', True):
                alerts.append({
                    'type': 'error',
                    'source': check_name,
                    'message': check_result.get('error', 'Health check failed'),
                    'timestamp': datetime.utcnow().isoformat()
                })
            elif check_result.get('warning', False):
                alerts.append({
                    'type': 'warning',
                    'source': check_name,
                    'message': f'{check_name} is approaching limits',
                    'timestamp': datetime.utcnow().isoformat()
                })
        
        return alerts
