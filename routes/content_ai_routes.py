from flask import Blueprint, request, jsonify, render_template
import asyncio
import json
from datetime import datetime
from ai_content_engine import get_ai_content_suggestions, analyze_content_performance
import logging

content_ai_bp = Blueprint('content_ai', __name__)
logger = logging.getLogger(__name__)

@content_ai_bp.route('/content-ai')
def content_ai_dashboard():
    """AI Content Suggestion Dashboard"""
    return render_template('content_ai/dashboard.html')

@content_ai_bp.route('/api/content-suggestions', methods=['POST'])
def generate_content_suggestions():
    """Generate AI-powered content suggestions"""
    try:
        data = request.get_json()
        content_type = data.get('content_type', 'social_media')
        campaign_goal = data.get('campaign_goal', 'lead_generation')
        target_audience = data.get('target_audience', 'entrepreneurs')
        
        # Run async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        suggestions = loop.run_until_complete(
            get_ai_content_suggestions(content_type, campaign_goal, target_audience)
        )
        loop.close()
        
        return jsonify({
            'status': 'success',
            'suggestions': suggestions,
            'generated_at': datetime.now().isoformat(),
            'count': len(suggestions)
        })
        
    except Exception as e:
        logger.error(f"Content generation error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@content_ai_bp.route('/api/content-performance/<content_id>')
def get_content_performance(content_id):
    """Get performance analysis for specific content"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        performance = loop.run_until_complete(analyze_content_performance(content_id))
        loop.close()
        
        return jsonify({
            'status': 'success',
            'performance': performance
        })
        
    except Exception as e:
        logger.error(f"Performance analysis error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@content_ai_bp.route('/content-calendar')
def content_calendar():
    """Content calendar with AI suggestions"""
    
    # Sample calendar data with AI-generated content
    calendar_data = {
        'today': datetime.now().strftime('%Y-%m-%d'),
        'scheduled_content': [
            {
                'date': '2025-08-09',
                'time': '09:00',
                'platform': 'LinkedIn',
                'content_type': 'Success Story',
                'content': '🚀 Sarah M. generated $12K in 21 days using OMNI Bot Premium! The automation engine was a game-changer. Who\'s ready to replicate this success? #Success #AI',
                'status': 'scheduled',
                'predicted_engagement': 8.7
            },
            {
                'date': '2025-08-09', 
                'time': '13:00',
                'platform': 'Twitter',
                'content_type': 'Educational',
                'content': '🎯 Business TIP: Automate your lead generation first, then scale. This single change helped 1,247+ entrepreneurs increase revenue by 234%. Try it today! #BusinessTips',
                'status': 'scheduled',
                'predicted_engagement': 12.3
            },
            {
                'date': '2025-08-09',
                'time': '17:00', 
                'platform': 'Facebook',
                'content_type': 'Urgency',
                'content': '🔥 FLASH INSIGHT: Only 23% of businesses are using AI automation effectively. Early adopters are seeing 300% faster growth. Don\'t get left behind! #Innovation',
                'status': 'scheduled',
                'predicted_engagement': 15.8
            }
        ]
    }
    
    return render_template('content_ai/calendar.html', calendar=calendar_data)

@content_ai_bp.route('/content-templates')
def content_templates():
    """Content template library with AI optimization"""
    
    template_categories = {
        'social_media': {
            'success_stories': [
                {
                    'name': 'Customer Success Highlight',
                    'template': '🚀 {customer_name} generated ${revenue}K in {timeframe} days using {product_name}! The {key_feature} was a game-changer. Who\'s ready to replicate this success?',
                    'performance_score': 87,
                    'best_platforms': ['LinkedIn', 'Facebook', 'Twitter']
                },
                {
                    'name': 'Business Growth Story',
                    'template': '📊 CASE STUDY: {business_type} owner went from ${start_revenue}K to ${end_revenue}K monthly using our {solution_type}. The secret? {winning_strategy}.',
                    'performance_score': 92,
                    'best_platforms': ['LinkedIn', 'Facebook']
                }
            ],
            'educational_content': [
                {
                    'name': 'Industry Tip',
                    'template': '🎯 {industry} TIP: {insight_text} This single change helped {customer_count}+ entrepreneurs increase revenue by {avg_increase}%. Try it today!',
                    'performance_score': 84,
                    'best_platforms': ['LinkedIn', 'Twitter', 'Instagram']
                }
            ]
        },
        'email_marketing': {
            'welcome_series': [
                {
                    'name': 'Welcome Email 1',
                    'subject': 'Welcome to your {product_name} journey, {first_name}!',
                    'template': 'You\'ve made an excellent decision joining {customer_count}+ entrepreneurs who are transforming their businesses with {key_benefit}...',
                    'open_rate': 34.2,
                    'click_rate': 8.9
                }
            ]
        }
    }
    
    return render_template('content_ai/templates.html', templates=template_categories)

@content_ai_bp.route('/content-analytics')
def content_analytics():
    """Content performance analytics dashboard"""
    
    analytics_data = {
        'overview': {
            'total_content_pieces': 847,
            'avg_engagement_rate': 12.8,
            'top_performing_platform': 'LinkedIn',
            'content_roi': 4.2
        },
        'platform_performance': {
            'LinkedIn': {'engagement': 15.3, 'reach': 12500, 'conversions': 34},
            'Facebook': {'engagement': 11.7, 'reach': 18900, 'conversions': 42},
            'Twitter': {'engagement': 8.9, 'reach': 8700, 'conversions': 18},
            'Instagram': {'engagement': 18.4, 'reach': 6200, 'conversions': 23}
        },
        'content_type_performance': {
            'Success Stories': {'avg_engagement': 16.2, 'conversion_rate': 4.1},
            'Educational Content': {'avg_engagement': 12.8, 'conversion_rate': 2.7},
            'Urgency Content': {'avg_engagement': 14.5, 'conversion_rate': 5.3},
            'Behind the Scenes': {'avg_engagement': 9.8, 'conversion_rate': 1.9}
        },
        'trending_topics': [
            {'topic': 'AI Automation', 'mentions': 156, 'engagement_lift': '+23%'},
            {'topic': 'Revenue Generation', 'mentions': 134, 'engagement_lift': '+18%'},
            {'topic': 'Business Empire', 'mentions': 98, 'engagement_lift': '+15%'}
        ]
    }
    
    return render_template('content_ai/analytics.html', analytics=analytics_data)

@content_ai_bp.route('/api/optimize-content', methods=['POST'])
def optimize_existing_content():
    """Optimize existing content using AI suggestions"""
    try:
        data = request.get_json()
        original_content = data.get('content', '')
        content_type = data.get('content_type', 'social_media')
        goal = data.get('goal', 'engagement')
        
        # AI optimization suggestions
        optimizations = {
            'original_content': original_content,
            'optimization_score': 78,
            'suggestions': [
                {
                    'type': 'length',
                    'suggestion': 'Reduce content length by 20% for better social media performance',
                    'impact': 'medium'
                },
                {
                    'type': 'emotional_trigger',
                    'suggestion': 'Add urgency elements like "limited time" or "exclusive"',
                    'impact': 'high'
                },
                {
                    'type': 'social_proof',
                    'suggestion': 'Include specific numbers: "Join 1,247+ entrepreneurs"',
                    'impact': 'high'
                },
                {
                    'type': 'call_to_action',
                    'suggestion': 'Make CTA more specific: "Download free guide" vs "Learn more"',
                    'impact': 'medium'
                }
            ],
            'optimized_versions': [
                {
                    'version': 'A',
                    'content': original_content + ' Join 1,247+ successful entrepreneurs! 🚀',
                    'predicted_improvement': '+15% engagement'
                },
                {
                    'version': 'B', 
                    'content': '⚡ LIMITED TIME: ' + original_content + ' Get instant access →',
                    'predicted_improvement': '+23% conversions'
                }
            ]
        }
        
        return jsonify({
            'status': 'success',
            'optimizations': optimizations
        })
        
    except Exception as e:
        logger.error(f"Content optimization error: {str(e)}")
        return jsonify({'error': str(e)}), 500