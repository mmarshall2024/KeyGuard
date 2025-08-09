"""
OMNI White Label Reseller System
Complete white-label solution for agencies and resellers
"""

import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

class WhiteLabelSystem:
    def __init__(self):
        self.reseller_tiers = {
            'starter': {
                'monthly_fee': 99,
                'commission_rate': 30,
                'max_clients': 10,
                'features': [
                    'Basic OMNI branding customization',
                    'Client management dashboard', 
                    'Basic automation tools',
                    'Email support'
                ],
                'white_label_level': 'Basic'
            },
            'professional': {
                'monthly_fee': 249,
                'commission_rate': 40,
                'max_clients': 50,
                'features': [
                    'Full OMNI system white-labeling',
                    'Custom domain and branding',
                    'Advanced automation suite',
                    'Client reporting dashboard',
                    'Priority support',
                    'Training materials'
                ],
                'white_label_level': 'Advanced'
            },
            'enterprise': {
                'monthly_fee': 429,
                'commission_rate': 50,
                'max_clients': 'unlimited',
                'features': [
                    'Complete system white-labeling',
                    'Custom development options',
                    'Multi-tenant architecture',
                    'API access and integrations',
                    'Dedicated account manager',
                    'Custom training programs',
                    'Reseller marketing materials'
                ],
                'white_label_level': 'Complete'
            }
        }
        
        self.customization_options = {
            'branding': [
                'Logo replacement',
                'Color scheme customization',
                'Font selection',
                'Custom CSS styling',
                'Favicon and images'
            ],
            'features': [
                'Module selection',
                'Feature toggling',
                'Custom workflows',
                'Integration preferences',
                'User permissions'
            ],
            'content': [
                'Custom messaging',
                'Localization options',
                'Help documentation',
                'Video tutorials',
                'Email templates'
            ],
            'technical': [
                'Custom domain setup',
                'SSL certificate',
                'Database separation',
                'API endpoints',
                'Webhook configuration'
            ]
        }

    def create_reseller_account(self, 
                              business_name: str,
                              contact_email: str, 
                              tier: str,
                              branding_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Create new white-label reseller account"""
        
        reseller_id = f"wl_{uuid.uuid4().hex[:8]}"
        
        account = {
            'reseller_id': reseller_id,
            'business_name': business_name,
            'contact_email': contact_email,
            'tier': tier,
            'tier_details': self.reseller_tiers[tier],
            'branding': branding_preferences,
            'status': 'active',
            'created_date': datetime.now().isoformat(),
            'custom_domain': f"{business_name.lower().replace(' ', '-')}.omni-powered.com",
            'api_key': f"wl_api_{uuid.uuid4().hex}",
            'monthly_revenue': 0,
            'total_clients': 0,
            'commission_earned': 0,
            'next_billing_date': (datetime.now() + timedelta(days=30)).isoformat()
        }
        
        # Generate custom branding package
        account['branding_package'] = self._generate_branding_package(
            reseller_id, branding_preferences, tier
        )
        
        # Setup initial dashboard configuration
        account['dashboard_config'] = self._setup_dashboard_config(tier)
        
        # Create training materials
        account['training_materials'] = self._generate_training_materials(tier)
        
        return account

    def _generate_branding_package(self, 
                                 reseller_id: str, 
                                 preferences: Dict[str, Any], 
                                 tier: str) -> Dict[str, Any]:
        """Generate complete branding package for reseller"""
        
        return {
            'package_id': f"brand_{reseller_id}",
            'primary_colors': {
                'primary': preferences.get('primary_color', '#7CFF00'),
                'secondary': preferences.get('secondary_color', '#0B1426'),
                'accent': preferences.get('accent_color', '#00FFDD')
            },
            'logo_variations': [
                f"logo_horizontal_{reseller_id}.svg",
                f"logo_vertical_{reseller_id}.svg", 
                f"logo_icon_{reseller_id}.svg",
                f"logo_white_{reseller_id}.svg"
            ],
            'css_framework': {
                'custom_variables': self._generate_css_variables(preferences),
                'component_overrides': self._generate_component_styles(preferences),
                'responsive_styles': self._generate_responsive_styles(preferences)
            },
            'email_templates': self._generate_email_templates(preferences),
            'marketing_materials': self._generate_marketing_materials(reseller_id, tier),
            'social_media_kit': self._generate_social_media_kit(preferences)
        }

    def _setup_dashboard_config(self, tier: str) -> Dict[str, Any]:
        """Setup dashboard configuration based on tier"""
        
        base_modules = [
            'client_management',
            'revenue_tracking', 
            'basic_automation',
            'support_center'
        ]
        
        professional_modules = base_modules + [
            'advanced_analytics',
            'white_label_settings',
            'custom_integrations',
            'training_center'
        ]
        
        enterprise_modules = professional_modules + [
            'api_management',
            'multi_tenant_control',
            'advanced_customization',
            'dedicated_support',
            'custom_development'
        ]
        
        module_mapping = {
            'starter': base_modules,
            'professional': professional_modules,
            'enterprise': enterprise_modules
        }
        
        return {
            'enabled_modules': module_mapping[tier],
            'dashboard_layout': self._get_dashboard_layout(tier),
            'navigation_structure': self._get_navigation_structure(tier),
            'permission_levels': self._get_permission_levels(tier)
        }

    def _generate_training_materials(self, tier: str) -> Dict[str, List[str]]:
        """Generate training materials based on tier"""
        
        base_training = [
            'OMNI System Overview',
            'Client Onboarding Process',
            'Basic Automation Setup',
            'Revenue Tracking Basics',
            'Support Best Practices'
        ]
        
        professional_training = base_training + [
            'Advanced Feature Configuration',
            'White-Label Customization',
            'Sales Process Optimization',
            'Client Retention Strategies',
            'Marketing Material Usage'
        ]
        
        enterprise_training = professional_training + [
            'API Integration Guide',
            'Multi-Tenant Management',
            'Custom Development Options',
            'Enterprise Sales Training',
            'Advanced Support Protocols'
        ]
        
        training_mapping = {
            'starter': base_training,
            'professional': professional_training, 
            'enterprise': enterprise_training
        }
        
        return {
            'video_tutorials': training_mapping[tier],
            'documentation': [f"{module}_guide.pdf" for module in training_mapping[tier]],
            'live_training_schedule': self._get_training_schedule(tier),
            'certification_program': tier in ['professional', 'enterprise']
        }

    def get_reseller_dashboard_data(self, reseller_id: str) -> Dict[str, Any]:
        """Get comprehensive dashboard data for reseller"""
        
        # Simulate real data - in production, this would query actual database
        return {
            'reseller_info': {
                'reseller_id': reseller_id,
                'business_name': 'Example Agency',
                'tier': 'professional',
                'status': 'active',
                'member_since': '2025-01-15'
            },
            'financial_metrics': {
                'monthly_revenue': f"${12750:,}",
                'commission_earned': f"${5100:,}",
                'commission_rate': '40%',
                'next_payout': f"${1275:,}",
                'total_earnings': f"${28900:,}"
            },
            'client_metrics': {
                'total_clients': 23,
                'active_clients': 21,
                'new_this_month': 4,
                'churn_rate': '8.7%',
                'average_client_value': f"${547:,}"
            },
            'performance_metrics': {
                'conversion_rate': '18.5%',
                'client_satisfaction': '94.2%',
                'support_tickets': 12,
                'response_time': '2.3 hours'
            },
            'recent_activity': [
                {
                    'date': '2025-08-08',
                    'action': 'New client onboarded',
                    'client': 'Tech Startup LLC',
                    'value': '$497'
                },
                {
                    'date': '2025-08-07', 
                    'action': 'Commission earned',
                    'client': 'Marketing Pro Inc',
                    'value': '$198'
                },
                {
                    'date': '2025-08-06',
                    'action': 'Client upgrade',
                    'client': 'Business Solutions Co',
                    'value': '$794'
                }
            ],
            'growth_projections': {
                'next_month_revenue': f"${15200:,}",
                'quarterly_projection': f"${42300:,}",
                'annual_projection': f"${168500:,}"
            }
        }

    def generate_client_proposal(self, 
                               reseller_id: str,
                               client_name: str, 
                               client_industry: str,
                               package_tier: str) -> Dict[str, Any]:
        """Generate client proposal with reseller branding"""
        
        package_pricing = {
            'basic': {'price': 297, 'features': 8, 'support': 'Email'},
            'professional': {'price': 597, 'features': 15, 'support': 'Priority'},
            'enterprise': {'price': 997, 'features': 25, 'support': 'Dedicated'}
        }
        
        selected_package = package_pricing[package_tier]
        
        return {
            'proposal_id': f"prop_{uuid.uuid4().hex[:8]}",
            'reseller_id': reseller_id,
            'client_info': {
                'name': client_name,
                'industry': client_industry,
                'package': package_tier
            },
            'pricing': {
                'monthly_cost': selected_package['price'],
                'setup_fee': 0,
                'first_year_savings': selected_package['price'] * 2,  # 2 months free
                'roi_projection': selected_package['price'] * 5  # 5x ROI projection
            },
            'features_included': self._get_package_features(package_tier),
            'implementation_timeline': {
                'setup': '24-48 hours',
                'training': '1 week',
                'full_deployment': '2 weeks',
                'first_results': '30 days'
            },
            'success_metrics': {
                'expected_revenue_increase': '300%',
                'time_savings': '25 hours/week',
                'automation_efficiency': '85%',
                'client_satisfaction': '95%+'
            },
            'next_steps': [
                'Review and approve proposal',
                'Complete onboarding forms',
                'Schedule implementation call',
                'Begin system setup',
                'Start training program'
            ],
            'proposal_expires': (datetime.now() + timedelta(days=7)).isoformat()
        }

    def _generate_css_variables(self, preferences: Dict) -> str:
        """Generate CSS variables for custom branding"""
        
        return f"""
        :root {{
            --primary-color: {preferences.get('primary_color', '#7CFF00')};
            --secondary-color: {preferences.get('secondary_color', '#0B1426')};
            --accent-color: {preferences.get('accent_color', '#00FFDD')};
            --font-family: {preferences.get('font_family', 'Segoe UI, sans-serif')};
            --border-radius: {preferences.get('border_radius', '12px')};
            --box-shadow: 0 4px 20px rgba(124, 255, 0, 0.15);
        }}
        """

    def _get_package_features(self, package_tier: str) -> List[str]:
        """Get features included in package tier"""
        
        features = {
            'basic': [
                'AI-Powered Revenue Optimization',
                'Automated Lead Generation', 
                'Email Marketing Automation',
                'Basic Analytics Dashboard',
                'Payment Processing Integration',
                'Customer Support Portal',
                'Mobile App Access',
                'Standard Training Materials'
            ],
            'professional': [
                'Everything in Basic, plus:',
                'Advanced AI Content Generation',
                'Multi-Platform Social Media Automation',
                'Advanced Analytics & Reporting',
                'Custom Funnel Builder',
                'A/B Testing Tools',
                'Priority Customer Support',
                'API Access',
                'Advanced Training Program'
            ],
            'enterprise': [
                'Everything in Professional, plus:',
                'Complete White-Label Solution',
                'Custom Integrations',
                'Dedicated Account Manager',
                'Advanced Security Features',
                'Custom Development Options',
                'Unlimited User Accounts',
                'Advanced Reporting Suite',
                'SLA Guarantees'
            ]
        }
        
        return features.get(package_tier, features['basic'])

    def _get_training_schedule(self, tier: str) -> List[Dict[str, str]]:
        """Get training schedule based on tier"""
        
        schedules = {
            'starter': [
                {'session': 'OMNI Basics', 'duration': '1 hour', 'frequency': 'One-time'},
                {'session': 'Client Management', 'duration': '30 min', 'frequency': 'Monthly'}
            ],
            'professional': [
                {'session': 'Advanced Features', 'duration': '2 hours', 'frequency': 'Weekly'},
                {'session': 'Sales Optimization', 'duration': '1 hour', 'frequency': 'Bi-weekly'},
                {'session': 'Q&A Sessions', 'duration': '45 min', 'frequency': 'Weekly'}
            ],
            'enterprise': [
                {'session': 'Custom Development', 'duration': '3 hours', 'frequency': 'Weekly'},
                {'session': 'Enterprise Features', 'duration': '2 hours', 'frequency': 'Bi-weekly'},
                {'session': 'Dedicated Support', 'duration': 'As needed', 'frequency': 'On-demand'}
            ]
        }
        
        return schedules.get(tier, schedules['starter'])

    def get_reseller_commission_report(self, reseller_id: str, month: str) -> Dict[str, Any]:
        """Generate detailed commission report"""
        
        return {
            'reseller_id': reseller_id,
            'report_period': month,
            'commission_summary': {
                'total_sales': f"${28750:,}",
                'commission_rate': '40%',
                'gross_commission': f"${11500:,}",
                'fees_deducted': f"${575:,}",
                'net_commission': f"${10925:,}",
                'payout_date': '2025-09-01'
            },
            'client_breakdown': [
                {
                    'client_name': 'Tech Solutions LLC',
                    'package': 'Enterprise',
                    'monthly_value': f"${997:,}",
                    'commission': f"${399:,}",
                    'status': 'Active'
                },
                {
                    'client_name': 'Marketing Pro Inc',
                    'package': 'Professional', 
                    'monthly_value': f"${597:,}",
                    'commission': f"${239:,}",
                    'status': 'Active'
                },
                {
                    'client_name': 'Small Biz Co',
                    'package': 'Basic',
                    'monthly_value': f"${297:,}",
                    'commission': f"${119:,}",
                    'status': 'Active'
                }
            ],
            'performance_bonuses': {
                'volume_bonus': f"${500:,}",
                'retention_bonus': f"${250:,}",
                'referral_bonus': f"${200:,}"
            },
            'next_tier_requirements': {
                'current_tier': 'Professional',
                'next_tier': 'Enterprise',
                'clients_needed': 7,
                'revenue_needed': f"${5250:,}"
            }
        }

# Global instance
white_label_system = WhiteLabelSystem()

def create_new_reseller(business_name: str, email: str, tier: str, branding: Dict) -> Dict[str, Any]:
    """Create new white-label reseller account"""
    return white_label_system.create_reseller_account(business_name, email, tier, branding)

def get_reseller_metrics(reseller_id: str) -> Dict[str, Any]:
    """Get reseller performance metrics"""
    return white_label_system.get_reseller_dashboard_data(reseller_id)

def generate_proposal(reseller_id: str, client_name: str, industry: str, package: str) -> Dict[str, Any]:
    """Generate client proposal for reseller"""
    return white_label_system.generate_client_proposal(reseller_id, client_name, industry, package)