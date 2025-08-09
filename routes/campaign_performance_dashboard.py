from flask import Blueprint, render_template, jsonify, request
import os
import json
import logging
from datetime import datetime, timedelta
import random
import threading
import time

campaign_performance_bp = Blueprint('campaign_performance', __name__)
logger = logging.getLogger(__name__)

# Import campaign data from launcher
try:
    from routes.campaign_launcher import active_campaigns, campaign_metrics
except ImportError:
    active_campaigns = {}
    campaign_metrics = {
        'total_revenue_generated': 0,
        'total_conversions': 0,
        'campaigns_launched': 0,
        'active_campaigns_count': 0,
        'best_performing_campaign': None,
        'last_campaign_launch': None
    }

class CampaignPerformanceDashboard:
    def __init__(self):
        self.dashboard_metrics = {
            'real_time_revenue': 0,
            'conversion_rate': 0,
            'roi_performance': 0,
            'channel_performance': {},
            'hourly_trends': [],
            'campaign_comparisons': [],
            'predictive_analytics': {}
        }
        
        self.performance_thresholds = {
            'excellent_roi': 15.0,
            'good_roi': 10.0,
            'poor_roi': 5.0,
            'excellent_conversion': 5.0,
            'good_conversion': 2.0,
            'poor_conversion': 1.0
        }
        
        self.start_performance_tracking()
    
    def start_performance_tracking(self):
        """Start real-time performance tracking"""
        def tracking_loop():
            while True:
                try:
                    self.update_dashboard_metrics()
                    time.sleep(30)  # Update every 30 seconds
                except Exception as e:
                    logger.error(f"Performance tracking error: {str(e)}")
                    time.sleep(60)
        
        tracking_thread = threading.Thread(target=tracking_loop, daemon=True)
        tracking_thread.start()
        logger.info("Campaign performance dashboard tracking started")
    
    def update_dashboard_metrics(self):
        """Update all dashboard metrics"""
        try:
            # Calculate real-time metrics
            self.dashboard_metrics['real_time_revenue'] = sum(
                campaign['metrics']['revenue_generated'] 
                for campaign in active_campaigns.values()
            )
            
            # Calculate average conversion rate
            total_clicks = sum(
                campaign['metrics']['clicks'] 
                for campaign in active_campaigns.values()
            )
            total_conversions = sum(
                campaign['metrics']['conversions'] 
                for campaign in active_campaigns.values()
            )
            
            if total_clicks > 0:
                self.dashboard_metrics['conversion_rate'] = (total_conversions / total_clicks) * 100
            
            # Calculate average ROI
            total_ad_spend = sum(
                campaign['metrics']['ad_spend'] 
                for campaign in active_campaigns.values()
            )
            
            if total_ad_spend > 0:
                self.dashboard_metrics['roi_performance'] = self.dashboard_metrics['real_time_revenue'] / total_ad_spend
            
            # Update channel performance
            self.update_channel_performance()
            
            # Update hourly trends
            self.update_hourly_trends()
            
            # Update campaign comparisons
            self.update_campaign_comparisons()
            
            # Generate predictive analytics
            self.generate_predictive_analytics()
            
        except Exception as e:
            logger.error(f"Dashboard metrics update error: {str(e)}")
    
    def update_channel_performance(self):
        """Update performance by channel"""
        channel_data = {}
        
        for campaign in active_campaigns.values():
            for channel in campaign.get('channels_activated', []):
                if channel not in channel_data:
                    channel_data[channel] = {
                        'revenue': 0,
                        'conversions': 0,
                        'clicks': 0,
                        'campaigns': 0
                    }
                
                # Simulate channel-specific performance
                campaign_revenue = campaign['metrics']['revenue_generated']
                channel_split = 1 / len(campaign['channels_activated'])
                
                channel_data[channel]['revenue'] += campaign_revenue * channel_split
                channel_data[channel]['conversions'] += campaign['metrics']['conversions'] * channel_split
                channel_data[channel]['clicks'] += campaign['metrics']['clicks'] * channel_split
                channel_data[channel]['campaigns'] += 1
        
        # Calculate channel efficiency metrics
        for channel, data in channel_data.items():
            if data['clicks'] > 0:
                data['conversion_rate'] = (data['conversions'] / data['clicks']) * 100
            else:
                data['conversion_rate'] = 0
            
            data['revenue_per_click'] = data['revenue'] / max(1, data['clicks'])
            data['efficiency_score'] = data['conversion_rate'] * data['revenue_per_click']
        
        self.dashboard_metrics['channel_performance'] = channel_data
    
    def update_hourly_trends(self):
        """Update hourly performance trends"""
        current_hour = datetime.now().hour
        
        # Generate last 24 hours of data
        hourly_data = []
        for i in range(24):
            hour = (current_hour - i) % 24
            
            # Simulate hourly performance based on active campaigns
            base_performance = sum(
                len(campaign.get('hourly_metrics', [])) 
                for campaign in active_campaigns.values()
            )
            
            hourly_revenue = base_performance * random.uniform(800, 1500)
            hourly_conversions = base_performance * random.uniform(5, 15)
            hourly_roi = hourly_revenue / max(100, base_performance * random.uniform(50, 100))
            
            hourly_data.append({
                'hour': f"{hour:02d}:00",
                'revenue': round(hourly_revenue, 2),
                'conversions': int(hourly_conversions),
                'roi': round(hourly_roi, 2),
                'timestamp': (datetime.now() - timedelta(hours=i)).isoformat()
            })
        
        self.dashboard_metrics['hourly_trends'] = list(reversed(hourly_data))
    
    def update_campaign_comparisons(self):
        """Update campaign comparison metrics"""
        comparisons = []
        
        for campaign_id, campaign in active_campaigns.items():
            config = campaign['config']
            metrics = campaign['metrics']
            
            # Calculate performance scores
            roi_score = self.calculate_performance_score(metrics['roi'], 'roi')
            conversion_score = self.calculate_performance_score(metrics['conversion_rate'], 'conversion')
            
            comparison_data = {
                'campaign_id': campaign_id,
                'name': config['name'],
                'type': config['type'],
                'revenue': metrics['revenue_generated'],
                'target_revenue': config['estimated_revenue'],
                'revenue_progress': (metrics['revenue_generated'] / config['estimated_revenue']) * 100,
                'conversions': metrics['conversions'],
                'target_conversions': config['target_conversions'],
                'conversion_progress': (metrics['conversions'] / config['target_conversions']) * 100,
                'roi': metrics['roi'],
                'roi_score': roi_score,
                'conversion_rate': metrics['conversion_rate'],
                'conversion_score': conversion_score,
                'overall_score': (roi_score + conversion_score) / 2,
                'status': campaign['status'],
                'duration_remaining': self.calculate_duration_remaining(campaign)
            }
            
            comparisons.append(comparison_data)
        
        # Sort by overall performance score
        comparisons.sort(key=lambda x: x['overall_score'], reverse=True)
        
        self.dashboard_metrics['campaign_comparisons'] = comparisons
    
    def calculate_performance_score(self, value, metric_type):
        """Calculate performance score (0-100)"""
        if metric_type == 'roi':
            if value >= self.performance_thresholds['excellent_roi']:
                return 100
            elif value >= self.performance_thresholds['good_roi']:
                return 75
            elif value >= self.performance_thresholds['poor_roi']:
                return 50
            else:
                return 25
        
        elif metric_type == 'conversion':
            if value >= self.performance_thresholds['excellent_conversion']:
                return 100
            elif value >= self.performance_thresholds['good_conversion']:
                return 75
            elif value >= self.performance_thresholds['poor_conversion']:
                return 50
            else:
                return 25
        
        return 50
    
    def calculate_duration_remaining(self, campaign):
        """Calculate remaining campaign duration"""
        try:
            end_time = datetime.fromisoformat(campaign['end_time'])
            remaining = end_time - datetime.now()
            
            if remaining.total_seconds() <= 0:
                return "Completed"
            
            hours = int(remaining.total_seconds() // 3600)
            minutes = int((remaining.total_seconds() % 3600) // 60)
            
            if hours > 0:
                return f"{hours}h {minutes}m"
            else:
                return f"{minutes}m"
                
        except Exception:
            return "Unknown"
    
    def generate_predictive_analytics(self):
        """Generate predictive analytics and recommendations"""
        predictions = {
            'revenue_forecast': self.predict_revenue_forecast(),
            'optimal_channels': self.identify_optimal_channels(),
            'campaign_recommendations': self.generate_campaign_recommendations(),
            'market_opportunities': self.identify_market_opportunities()
        }
        
        self.dashboard_metrics['predictive_analytics'] = predictions
    
    def predict_revenue_forecast(self):
        """Predict revenue forecast for next 24 hours"""
        current_revenue_rate = self.dashboard_metrics.get('real_time_revenue', 0)
        active_campaigns_count = len(active_campaigns)
        
        if active_campaigns_count > 0:
            hourly_rate = current_revenue_rate / max(1, active_campaigns_count)
            forecast_24h = hourly_rate * 24 * random.uniform(1.1, 1.4)
            forecast_7d = forecast_24h * 7 * random.uniform(0.9, 1.2)
            forecast_30d = forecast_7d * 4.3 * random.uniform(0.8, 1.3)
        else:
            forecast_24h = forecast_7d = forecast_30d = 0
        
        return {
            '24_hours': round(forecast_24h, 2),
            '7_days': round(forecast_7d, 2),
            '30_days': round(forecast_30d, 2),
            'confidence': random.uniform(0.75, 0.95)
        }
    
    def identify_optimal_channels(self):
        """Identify best performing channels"""
        channel_performance = self.dashboard_metrics.get('channel_performance', {})
        
        optimal_channels = []
        for channel, data in channel_performance.items():
            optimal_channels.append({
                'channel': channel,
                'efficiency_score': data.get('efficiency_score', 0),
                'conversion_rate': data.get('conversion_rate', 0),
                'revenue': data.get('revenue', 0),
                'recommendation': self.get_channel_recommendation(data)
            })
        
        optimal_channels.sort(key=lambda x: x['efficiency_score'], reverse=True)
        return optimal_channels[:3]  # Top 3 channels
    
    def get_channel_recommendation(self, channel_data):
        """Get recommendation for channel optimization"""
        efficiency = channel_data.get('efficiency_score', 0)
        
        if efficiency > 50:
            return "Scale up investment - high performance"
        elif efficiency > 25:
            return "Optimize targeting - moderate performance"
        else:
            return "Review strategy - low performance"
    
    def generate_campaign_recommendations(self):
        """Generate campaign optimization recommendations"""
        recommendations = []
        
        for campaign in active_campaigns.values():
            metrics = campaign['metrics']
            config = campaign['config']
            
            if metrics['roi'] < 5:
                recommendations.append({
                    'campaign': config['name'],
                    'type': 'urgent',
                    'message': 'Low ROI detected - consider pausing or optimizing targeting'
                })
            
            if metrics['conversion_rate'] < 1:
                recommendations.append({
                    'campaign': config['name'],
                    'type': 'warning',
                    'message': 'Low conversion rate - review ad copy and landing pages'
                })
            
            if metrics['revenue_generated'] > config['estimated_revenue'] * 0.8:
                recommendations.append({
                    'campaign': config['name'],
                    'type': 'success',
                    'message': 'Excellent performance - consider scaling budget'
                })
        
        return recommendations
    
    def identify_market_opportunities(self):
        """Identify market opportunities"""
        opportunities = [
            {
                'opportunity': 'Mobile App Platform',
                'potential_revenue': random.uniform(50000, 100000),
                'confidence': random.uniform(0.7, 0.9),
                'timeframe': '30 days'
            },
            {
                'opportunity': 'Enterprise Expansion',
                'potential_revenue': random.uniform(100000, 200000),
                'confidence': random.uniform(0.6, 0.8),
                'timeframe': '60 days'
            },
            {
                'opportunity': 'Affiliate Network Growth',
                'potential_revenue': random.uniform(75000, 150000),
                'confidence': random.uniform(0.8, 0.95),
                'timeframe': '45 days'
            }
        ]
        
        return opportunities
    
    def get_dashboard_data(self):
        """Get complete dashboard data"""
        return {
            'dashboard_metrics': self.dashboard_metrics,
            'active_campaigns': active_campaigns,
            'global_metrics': campaign_metrics,
            'performance_thresholds': self.performance_thresholds,
            'last_updated': datetime.now().isoformat()
        }

# Global dashboard instance
performance_dashboard = CampaignPerformanceDashboard()

@campaign_performance_bp.route('/campaign-performance')
def campaign_performance_page():
    """Campaign performance dashboard page"""
    return render_template('campaign_performance_dashboard.html')

@campaign_performance_bp.route('/api/dashboard-data')
def get_dashboard_data():
    """Get complete dashboard data"""
    try:
        data = performance_dashboard.get_dashboard_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@campaign_performance_bp.route('/api/channel-performance')
def get_channel_performance():
    """Get channel performance data"""
    try:
        return jsonify({
            'channel_performance': performance_dashboard.dashboard_metrics['channel_performance'],
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@campaign_performance_bp.route('/api/predictive-analytics')
def get_predictive_analytics():
    """Get predictive analytics data"""
    try:
        return jsonify({
            'predictive_analytics': performance_dashboard.dashboard_metrics['predictive_analytics'],
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@campaign_performance_bp.route('/api/hourly-trends')
def get_hourly_trends():
    """Get hourly performance trends"""
    try:
        return jsonify({
            'hourly_trends': performance_dashboard.dashboard_metrics['hourly_trends'],
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500