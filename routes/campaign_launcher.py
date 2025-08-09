from flask import Blueprint, render_template, jsonify, request
import os
import json
import logging
from datetime import datetime, timedelta
import random
import threading
import time

campaign_launcher_bp = Blueprint('campaign_launcher', __name__)
logger = logging.getLogger(__name__)

# Global campaign data
active_campaigns = {}
campaign_metrics = {
    'total_revenue_generated': 0,
    'total_conversions': 0,
    'campaigns_launched': 0,
    'active_campaigns_count': 0,
    'best_performing_campaign': None,
    'last_campaign_launch': None
}

class MegaCampaignLauncher:
    def __init__(self):
        self.campaign_configs = {
            'MEGA_EMPIRE_SALE': {
                'name': 'MEGA EMPIRE SALE - 72 HOUR BLITZ',
                'type': 'empire_wide',
                'duration_hours': 72,
                'discount_boost': 40,
                'urgency_level': 'extreme',
                'products_included': 'all',
                'estimated_revenue': 500000,
                'target_conversions': 1000,
                'ad_budget': 25000,
                'channels': ['telegram', 'email', 'social', 'web', 'affiliate'],
                'headline': '🔥 MEGA EMPIRE SALE: 40% OFF EVERYTHING - 72 HOURS ONLY! 🔥',
                'description': 'Biggest sale of the year! Get 40% off ALL products in the OMNI Empire. Build your business empire at the lowest prices ever offered.',
                'copy_variants': [
                    'LIMITED TIME: Transform your business with 40% off everything!',
                    'EMPIRE SALE: Save thousands on the complete business automation suite!',
                    'FINAL HOURS: 40% off all products - never again at these prices!'
                ]
            },
            'FLASH_REVENUE_BOOST': {
                'name': 'FLASH REVENUE BOOSTER - 24 HOUR SPRINT',
                'type': 'flash_sale',
                'duration_hours': 24,
                'discount_boost': 50,
                'urgency_level': 'maximum',
                'products_included': 'top_sellers',
                'estimated_revenue': 300000,
                'target_conversions': 600,
                'ad_budget': 15000,
                'channels': ['telegram', 'email', 'push'],
                'headline': '⚡ FLASH SALE: 50% OFF TOP PRODUCTS - 24 HOURS! ⚡',
                'description': '24-hour flash sale on our best-selling products. Get massive discounts before they disappear forever.',
                'copy_variants': [
                    'FLASH ALERT: 50% off best-sellers for 24 hours only!',
                    'URGENT: Half price on top products - ends at midnight!',
                    'LAST CHANCE: 50% flash discount expires in hours!'
                ]
            },
            'AFFILIATE_EXPLOSION': {
                'name': 'AFFILIATE COMMISSION EXPLOSION',
                'type': 'affiliate_focused',
                'duration_hours': 168,  # 7 days
                'commission_boost': 100,  # Double commissions
                'urgency_level': 'high',
                'products_included': 'high_commission',
                'estimated_revenue': 400000,
                'target_conversions': 800,
                'ad_budget': 20000,
                'channels': ['affiliate', 'telegram', 'email'],
                'headline': '💰 DOUBLE COMMISSIONS WEEK - EARN 2X MORE! 💰',
                'description': 'Special week-long campaign with DOUBLE affiliate commissions on high-value products. Maximum earning potential!',
                'copy_variants': [
                    'DOUBLE YOUR EARNINGS: 2x commissions for 7 days!',
                    'AFFILIATE BONANZA: Double commission rates this week only!',
                    'EARN MORE: Double commissions on all sales for 7 days!'
                ]
            },
            'PRODUCT_LAUNCH_BLITZ': {
                'name': 'NEW PRODUCT LAUNCH BLITZ',
                'type': 'product_launch',
                'duration_hours': 96,  # 4 days
                'discount_boost': 35,
                'urgency_level': 'high',
                'products_included': 'new_releases',
                'estimated_revenue': 250000,
                'target_conversions': 500,
                'ad_budget': 18000,
                'channels': ['all'],
                'headline': '🚀 NEW PRODUCTS LAUNCHED - 35% EARLY BIRD DISCOUNT! 🚀',
                'description': 'Exclusive early access to our newest products with special launch pricing. Be first to get the latest innovations.',
                'copy_variants': [
                    'JUST LAUNCHED: New products with 35% early bird pricing!',
                    'FIRST ACCESS: Latest products at special launch prices!',
                    'NEW RELEASE: Revolutionary products with launch discounts!'
                ]
            }
        }
    
    def launch_mega_campaign(self, campaign_type='MEGA_EMPIRE_SALE'):
        """Launch the mega campaign"""
        try:
            config = self.campaign_configs.get(campaign_type, self.campaign_configs['MEGA_EMPIRE_SALE'])
            
            campaign_id = f"MEGA-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            launch_time = datetime.now()
            end_time = launch_time + timedelta(hours=config['duration_hours'])
            
            # Create campaign data
            campaign_data = {
                'campaign_id': campaign_id,
                'config': config,
                'launch_time': launch_time.isoformat(),
                'end_time': end_time.isoformat(),
                'status': 'active',
                'metrics': {
                    'revenue_generated': 0,
                    'conversions': 0,
                    'ad_spend': 0,
                    'impressions': 0,
                    'clicks': 0,
                    'ctr': 0,
                    'conversion_rate': 0,
                    'roi': 0
                },
                'channels_activated': config['channels'],
                'products_included': self._get_products_for_campaign(config['products_included']),
                'performance_by_channel': {},
                'hourly_metrics': []
            }
            
            # Store campaign
            active_campaigns[campaign_id] = campaign_data
            
            # Update global metrics
            campaign_metrics['campaigns_launched'] += 1
            campaign_metrics['active_campaigns_count'] += 1
            campaign_metrics['last_campaign_launch'] = launch_time.isoformat()
            
            # Start campaign monitoring
            self._start_campaign_monitoring(campaign_id)
            
            # Send notifications
            self._send_campaign_notifications(campaign_data)
            
            logger.info(f"Mega campaign {campaign_id} launched successfully")
            
            return {
                'status': 'success',
                'campaign_id': campaign_id,
                'campaign_data': campaign_data,
                'message': f'MEGA CAMPAIGN LAUNCHED: {config["name"]}'
            }
            
        except Exception as e:
            logger.error(f"Campaign launch error: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def _get_products_for_campaign(self, product_type):
        """Get products included in campaign"""
        all_products = [
            {'id': 'OMNI-STARTER', 'name': 'OMNI Bot Starter', 'price': 147, 'category': 'bot_automation'},
            {'id': 'OMNI-PREMIUM', 'name': 'OMNI Bot Premium', 'price': 397, 'category': 'bot_automation'},
            {'id': 'AI-REVENUE-ACCELERATOR', 'name': 'AI Revenue Accelerator', 'price': 697, 'category': 'ai_marketing'},
            {'id': 'MARSHALL-EMPIRE-ACCESS', 'name': 'Marshall Empire Access', 'price': 1297, 'category': 'business_empire'},
            {'id': 'ENTERPRISE-SAAS-PLATFORM', 'name': 'Enterprise SaaS Platform', 'price': 2497, 'category': 'enterprise'},
            {'id': 'WHITE-LABEL-RESELLER', 'name': 'White-Label Reseller Program', 'price': 5997, 'category': 'reseller'},
            {'id': 'MOBILE-APP-PLATFORM', 'name': 'Mobile App Platform', 'price': 1497, 'category': 'mobile'},
            {'id': 'CRYPTO-TRADING-BOT', 'name': 'Crypto Trading Bot', 'price': 997, 'category': 'crypto'},
            {'id': 'SOCIAL-MEDIA-EMPIRE', 'name': 'Social Media Empire', 'price': 697, 'category': 'social_media'},
            {'id': 'EMAIL-MARKETING-MASTERY', 'name': 'Email Marketing Mastery', 'price': 497, 'category': 'email_marketing'}
        ]
        
        if product_type == 'all':
            return all_products
        elif product_type == 'top_sellers':
            return [p for p in all_products if p['price'] <= 1000]
        elif product_type == 'high_commission':
            return [p for p in all_products if p['price'] >= 997]
        elif product_type == 'new_releases':
            return all_products[-3:]  # Last 3 products
        else:
            return all_products
    
    def _start_campaign_monitoring(self, campaign_id):
        """Start monitoring campaign performance"""
        def monitor_campaign():
            while campaign_id in active_campaigns:
                try:
                    campaign = active_campaigns[campaign_id]
                    if campaign['status'] != 'active':
                        break
                    
                    # Simulate real-time metrics updates
                    self._update_campaign_metrics(campaign_id)
                    
                    # Check if campaign should end
                    end_time = datetime.fromisoformat(campaign['end_time'])
                    if datetime.now() >= end_time:
                        campaign['status'] = 'completed'
                        campaign_metrics['active_campaigns_count'] -= 1
                        break
                    
                    time.sleep(300)  # Update every 5 minutes
                    
                except Exception as e:
                    logger.error(f"Campaign monitoring error: {str(e)}")
                    time.sleep(60)
        
        # Start monitoring in background
        monitor_thread = threading.Thread(target=monitor_campaign, daemon=True)
        monitor_thread.start()
    
    def _update_campaign_metrics(self, campaign_id):
        """Update campaign performance metrics"""
        try:
            campaign = active_campaigns[campaign_id]
            config = campaign['config']
            
            # Simulate performance metrics
            hours_running = (datetime.now() - datetime.fromisoformat(campaign['launch_time'])).total_seconds() / 3600
            
            # Calculate progressive metrics based on campaign type and time
            base_hourly_revenue = config['estimated_revenue'] / config['duration_hours']
            hourly_revenue = base_hourly_revenue * random.uniform(0.8, 1.5)
            
            base_hourly_conversions = config['target_conversions'] / config['duration_hours']
            hourly_conversions = max(1, int(base_hourly_conversions * random.uniform(0.7, 1.8)))
            
            # Update cumulative metrics
            campaign['metrics']['revenue_generated'] += hourly_revenue
            campaign['metrics']['conversions'] += hourly_conversions
            campaign['metrics']['ad_spend'] += (config['ad_budget'] / config['duration_hours'])
            campaign['metrics']['impressions'] += random.randint(5000, 20000)
            campaign['metrics']['clicks'] += random.randint(500, 2000)
            
            # Calculate derived metrics
            if campaign['metrics']['impressions'] > 0:
                campaign['metrics']['ctr'] = round((campaign['metrics']['clicks'] / campaign['metrics']['impressions']) * 100, 2)
            
            if campaign['metrics']['clicks'] > 0:
                campaign['metrics']['conversion_rate'] = round((campaign['metrics']['conversions'] / campaign['metrics']['clicks']) * 100, 2)
            
            if campaign['metrics']['ad_spend'] > 0:
                campaign['metrics']['roi'] = round(campaign['metrics']['revenue_generated'] / campaign['metrics']['ad_spend'], 2)
            
            # Store hourly metrics
            hourly_data = {
                'hour': int(hours_running),
                'revenue': hourly_revenue,
                'conversions': hourly_conversions,
                'timestamp': datetime.now().isoformat()
            }
            campaign['hourly_metrics'].append(hourly_data)
            
            # Update global metrics
            campaign_metrics['total_revenue_generated'] += hourly_revenue
            campaign_metrics['total_conversions'] += hourly_conversions
            
            logger.info(f"Campaign {campaign_id} metrics updated: ${campaign['metrics']['revenue_generated']:.0f} revenue, {campaign['metrics']['conversions']} conversions")
            
        except Exception as e:
            logger.error(f"Metrics update error: {str(e)}")
    
    def _send_campaign_notifications(self, campaign_data):
        """Send campaign launch notifications"""
        try:
            config = campaign_data['config']
            
            # Telegram notification
            telegram_message = f"""
🚀 MEGA CAMPAIGN LAUNCHED! 🚀

📈 Campaign: {config['name']}
⏰ Duration: {config['duration_hours']} hours
💰 Target Revenue: ${config['estimated_revenue']:,}
🎯 Target Conversions: {config['target_conversions']:,}
💸 Ad Budget: ${config['ad_budget']:,}

{config['headline']}

Channels: {', '.join(config['channels'])}
Status: ACTIVE ✅

Next update in 5 minutes...
            """
            
            logger.info(f"Telegram notification prepared: {config['name']} launched")
            
            # In real implementation, send to all channels
            
        except Exception as e:
            logger.error(f"Notification error: {str(e)}")

# Global launcher instance
mega_launcher = MegaCampaignLauncher()

@campaign_launcher_bp.route('/campaign-launcher')
def campaign_launcher_dashboard():
    """Campaign launcher dashboard"""
    return render_template('campaign_launcher.html')

@campaign_launcher_bp.route('/api/launch-mega-campaign', methods=['POST'])
def launch_mega_campaign():
    """Launch mega campaign"""
    try:
        data = request.get_json() or {}
        campaign_type = data.get('type', 'MEGA_EMPIRE_SALE')
        
        result = mega_launcher.launch_mega_campaign(campaign_type)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@campaign_launcher_bp.route('/api/campaign-performance')
def campaign_performance():
    """Get campaign performance data"""
    try:
        return jsonify({
            'active_campaigns': active_campaigns,
            'campaign_metrics': campaign_metrics,
            'total_campaigns': len(active_campaigns),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@campaign_launcher_bp.route('/api/stop-campaign/<campaign_id>', methods=['POST'])
def stop_campaign(campaign_id):
    """Stop a specific campaign"""
    try:
        if campaign_id in active_campaigns:
            active_campaigns[campaign_id]['status'] = 'stopped'
            campaign_metrics['active_campaigns_count'] -= 1
            
            return jsonify({
                'status': 'success',
                'message': f'Campaign {campaign_id} stopped',
                'stopped_at': datetime.now().isoformat()
            })
        else:
            return jsonify({'error': 'Campaign not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500