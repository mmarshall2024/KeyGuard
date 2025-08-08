from flask import Blueprint, render_template, request, jsonify
from datetime import datetime, timedelta
import json
import random
import math

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics')
def analytics_dashboard():
    """Main analytics dashboard route"""
    return render_template('analytics/dashboard.html')

@analytics_bp.route('/api/dashboard-data')
def get_dashboard_data():
    """API endpoint for dashboard data"""
    try:
        # Generate realistic dashboard data
        dashboard_data = generate_dashboard_data()
        return jsonify(dashboard_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/api/real-time-metrics')
def get_real_time_metrics():
    """API endpoint for real-time metrics"""
    try:
        # Generate current metrics
        current_time = datetime.now()
        
        metrics = {
            'timestamp': current_time.isoformat(),
            'revenue': {
                'current': random.uniform(45000, 55000),
                'change': random.uniform(-5, 15),
                'target': 50000
            },
            'users': {
                'current': random.randint(2400, 3200),
                'change': random.uniform(-2, 25),
                'target': 3000
            },
            'conversion': {
                'current': random.uniform(16.5, 21.2),
                'change': random.uniform(-1, 3),
                'target': 20.0
            },
            'engagement': {
                'current': random.uniform(2.8, 4.1),
                'change': random.uniform(-8, 18),
                'target': 3.5
            }
        }
        
        return jsonify(metrics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/api/predictions')
def get_predictions():
    """API endpoint for predictive analytics"""
    try:
        predictions = {
            'revenue': {
                'next_30_days': generate_prediction_series(47320, 30, 'revenue'),
                'confidence': random.uniform(82, 94),
                'trend': 'positive',
                'factors': ['Seasonal trends', 'Marketing campaigns', 'Product launches']
            },
            'users': {
                'next_30_days': generate_prediction_series(2847, 30, 'users'),
                'confidence': random.uniform(78, 91),
                'trend': 'strong_growth',
                'factors': ['Viral coefficient', 'Referral programs', 'Content quality']
            },
            'conversion': {
                'next_30_days': generate_prediction_series(18.3, 30, 'conversion'),
                'confidence': random.uniform(85, 95),
                'trend': 'improving',
                'factors': ['Funnel optimization', 'A/B test results', 'UX improvements']
            }
        }
        
        return jsonify(predictions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/api/insights')
def get_insights():
    """API endpoint for AI insights"""
    try:
        insights = [
            {
                'id': 1,
                'title': 'Revenue Acceleration Opportunity',
                'description': 'Q4 seasonal patterns suggest 35% revenue uplift possible with targeted campaigns',
                'priority': 'high',
                'confidence': 0.89,
                'impact': '$18,400 additional revenue',
                'action': 'Launch holiday marketing campaign by October 15th',
                'category': 'revenue'
            },
            {
                'id': 2,
                'title': 'User Acquisition Optimization',
                'description': 'Social media channels showing 2.3x higher conversion than paid search',
                'priority': 'medium',
                'confidence': 0.76,
                'impact': '24% reduction in acquisition costs',
                'action': 'Reallocate 40% of search budget to social platforms',
                'category': 'users'
            },
            {
                'id': 3,
                'title': 'Mobile Conversion Bottleneck',
                'description': 'Mobile checkout abandonment at 67% - significantly above industry average',
                'priority': 'high',
                'confidence': 0.92,
                'impact': '8.2% conversion rate improvement',
                'action': 'Implement one-click checkout and mobile wallet integration',
                'category': 'conversion'
            },
            {
                'id': 4,
                'title': 'Cross-Selling Potential',
                'description': 'Users purchasing Product A show 78% interest in complementary Product B',
                'priority': 'medium',
                'confidence': 0.81,
                'impact': '28% increase in average order value',
                'action': 'Create Product A + B bundle with 15% discount',
                'category': 'revenue'
            },
            {
                'id': 5,
                'title': 'Market Expansion Indicator',
                'description': 'Organic traffic from European markets increased 156% without targeting',
                'priority': 'medium',
                'confidence': 0.73,
                'impact': '25-40% total market expansion',
                'action': 'Conduct market research and launch EU expansion pilot',
                'category': 'growth'
            }
        ]
        
        return jsonify(insights)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_dashboard_data():
    """Generate comprehensive dashboard data"""
    current_date = datetime.now()
    
    # Base metrics
    base_revenue = 47320
    base_users = 2847
    base_conversion = 18.3
    base_engagement = 3.2
    
    # Generate 30-day trends
    revenue_trend = generate_trend_data(base_revenue, 30, 'revenue')
    user_trend = generate_trend_data(base_users, 30, 'users')
    conversion_trend = generate_trend_data(base_conversion, 30, 'conversion')
    engagement_trend = generate_trend_data(base_engagement, 30, 'engagement')
    
    dashboard_data = {
        'overview': {
            'revenue': {
                'current': revenue_trend[-1],
                'previous': revenue_trend[-8],  # Week ago
                'trend': revenue_trend,
                'growth': ((revenue_trend[-1] - revenue_trend[-8]) / revenue_trend[-8]) * 100,
                'target': base_revenue * 1.15,
                'unit': '$'
            },
            'users': {
                'current': user_trend[-1],
                'previous': user_trend[-8],
                'trend': user_trend,
                'growth': ((user_trend[-1] - user_trend[-8]) / user_trend[-8]) * 100,
                'target': base_users * 1.20,
                'unit': 'users'
            },
            'conversion': {
                'current': conversion_trend[-1],
                'previous': conversion_trend[-8],
                'trend': conversion_trend,
                'growth': conversion_trend[-1] - conversion_trend[-8],
                'target': base_conversion * 1.05,
                'unit': '%'
            },
            'engagement': {
                'current': engagement_trend[-1],
                'previous': engagement_trend[-8],
                'trend': engagement_trend,
                'growth': ((engagement_trend[-1] - engagement_trend[-8]) / engagement_trend[-8]) * 100,
                'target': base_engagement * 1.12,
                'unit': 'sessions'
            }
        },
        'charts': {
            'revenue_chart': {
                'labels': [(current_date - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(29, -1, -1)],
                'data': revenue_trend,
                'type': 'line',
                'color': '#10b981'
            },
            'users_chart': {
                'labels': [(current_date - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(29, -1, -1)],
                'data': user_trend,
                'type': 'line',
                'color': '#3b82f6'
            },
            'conversion_chart': {
                'labels': [(current_date - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(29, -1, -1)],
                'data': conversion_trend,
                'type': 'line',
                'color': '#f59e0b'
            },
            'engagement_chart': {
                'labels': [(current_date - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(29, -1, -1)],
                'data': engagement_trend,
                'type': 'line',
                'color': '#8b5cf6'
            }
        },
        'performance_score': calculate_performance_score(revenue_trend, user_trend, conversion_trend, engagement_trend),
        'last_updated': current_date.isoformat()
    }
    
    return dashboard_data

def generate_trend_data(base_value, days, metric_type):
    """Generate realistic trend data"""
    trend_data = []
    current_value = base_value
    
    for day in range(days):
        if metric_type == "revenue":
            daily_variation = random.uniform(-0.12, 0.20)
            seasonal_factor = 1 + 0.08 * math.sin(day * 2 * math.pi / 7)
            growth_factor = 1 + (day * 0.002)
        elif metric_type == "users":
            daily_variation = random.uniform(-0.06, 0.14)
            seasonal_factor = 1 - 0.12 if day % 7 in [5, 6] else 1
            growth_factor = 1 + (day * 0.003)
        elif metric_type == "conversion":
            daily_variation = random.uniform(-0.04, 0.07)
            seasonal_factor = 1 + 0.03 * math.sin(day * 2 * math.pi / 30)
            growth_factor = 1 + (day * 0.001)
        else:  # engagement
            daily_variation = random.uniform(-0.10, 0.16)
            seasonal_factor = 1 + 0.15 * math.sin(day * 2 * math.pi / 7)
            growth_factor = 1 + (day * 0.0015)
            
        daily_value = current_value * (1 + daily_variation) * seasonal_factor * growth_factor
        trend_data.append(round(daily_value, 2))
        current_value = daily_value
        
    return trend_data

def generate_prediction_series(base_value, days, metric_type):
    """Generate prediction series for forecasting"""
    predictions = []
    current_value = base_value
    
    for day in range(days):
        # More stable predictions than historical data
        if metric_type == "revenue":
            daily_variation = random.uniform(-0.08, 0.15)
            trend_factor = 1 + (day * 0.003)  # Slightly more optimistic
        elif metric_type == "users":
            daily_variation = random.uniform(-0.04, 0.12)
            trend_factor = 1 + (day * 0.004)
        else:  # conversion
            daily_variation = random.uniform(-0.03, 0.06)
            trend_factor = 1 + (day * 0.002)
            
        predicted_value = current_value * (1 + daily_variation) * trend_factor
        predictions.append(round(predicted_value, 2))
        current_value = predicted_value
        
    return predictions

def calculate_performance_score(revenue_trend, user_trend, conversion_trend, engagement_trend):
    """Calculate overall performance score"""
    try:
        # Calculate growth rates
        revenue_growth = (revenue_trend[-1] - revenue_trend[0]) / revenue_trend[0]
        user_growth = (user_trend[-1] - user_trend[0]) / user_trend[0]
        conversion_growth = (conversion_trend[-1] - conversion_trend[0]) / conversion_trend[0]
        engagement_growth = (engagement_trend[-1] - engagement_trend[0]) / engagement_trend[0]
        
        # Weighted score (out of 100)
        score = (
            min(max(revenue_growth * 100, -20), 30) * 0.4 +  # 40% weight
            min(max(user_growth * 100, -15), 25) * 0.3 +     # 30% weight
            min(max(conversion_growth * 50, -10), 15) * 0.2 + # 20% weight
            min(max(engagement_growth * 100, -10), 20) * 0.1  # 10% weight
        )
        
        base_score = 75  # Base performance score
        final_score = max(0, min(100, base_score + score))
        
        return {
            'score': round(final_score, 1),
            'grade': 'A' if final_score >= 90 else 'B' if final_score >= 80 else 'C' if final_score >= 70 else 'D',
            'trend': 'improving' if score > 2 else 'stable' if score > -2 else 'declining'
        }
    except:
        return {'score': 75.0, 'grade': 'B', 'trend': 'stable'}