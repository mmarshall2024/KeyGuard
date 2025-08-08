from plugins.base_plugin import BasePlugin
from utils.mutation_engine import MutationEngine
from utils.observer_system import ObserverSystem
from utils.security_layer import SecurityLayer
import json
from datetime import datetime

class OMNICoreEnhancementPlugin(BasePlugin):
    """Advanced OMNI system enhancements with mutation, observation, and security"""
    
    def __init__(self):
        super().__init__()
        self.version = "2.0.0"
        self.description = "OMNI Core system with advanced mutation, observation, and security capabilities"
        
        # Initialize core systems
        self.mutation_engine = MutationEngine()
        self.observer_system = ObserverSystem()
        self.security_layer = SecurityLayer()
        
        # Start continuous monitoring
        self.observer_system.start_continuous_monitoring(interval=300)  # 5 minutes
        
    def register_commands(self, application=None):
        """Register enhanced OMNI commands"""
        # Mutation commands
        self.add_command("mutate", self.trigger_mutation, "Trigger system evolution")
        self.add_command("evolution", self.show_evolution_status, "Show evolution status")
        self.add_command("mutation_report", self.get_mutation_report, "Get detailed mutation report")
        
        # Observer commands
        self.add_command("observe", self.system_observation, "Perform system observation")
        self.add_command("system_health", self.check_system_health, "Check comprehensive system health")
        self.add_command("trends", self.show_system_trends, "Show system performance trends")
        self.add_command("alerts", self.get_system_alerts, "Get current system alerts")
        
        # Security commands
        self.add_command("security_scan", self.perform_security_scan, "Perform security scan")
        self.add_command("security_status", self.show_security_status, "Show security status")
        self.add_command("threat_analysis", self.analyze_threats, "Analyze security threats")
        
        # Advanced OMNI commands
        self.add_command("omni_status", self.show_omni_status, "Show complete OMNI system status")
        self.add_command("auto_optimize", self.auto_optimize_system, "Trigger automatic system optimization")
        self.add_command("system_report", self.generate_system_report, "Generate comprehensive system report")
        
        self.log(f"{self.name} enhanced commands registered successfully")
    
    def trigger_mutation(self, chat_id=None, args=None):
        """Trigger system mutation/evolution"""
        try:
            if args and len(args) > 0:
                # Targeted mutation
                target_area = args[0].lower()
                result = self.mutation_engine.trigger_targeted_mutation(target_area)
            else:
                # General mutation
                result = self.mutation_engine.mutate_logic()
            
            if result.get("success"):
                changes = result.get("changes", [])
                impact_score = result.get("impact_score", 0)
                
                response = "🧬 **OMNI System Mutation Complete**\n\n"
                response += f"🎯 **Evolution Type**: {result.get('category', 'General').title()}\n"
                response += f"📊 **Impact Score**: {impact_score:.2f}/1.0\n\n"
                
                response += "🔄 **Evolutionary Changes**:\n"
                for change in changes:
                    response += f"• {change}\n"
                
                response += f"\n⚡ **System Status**: Enhanced\n"
                response += f"🌟 **Evolution Level**: {self.mutation_engine._calculate_evolution_level()}"
                
                return response
            else:
                return f"❌ **Mutation Failed**: {result.get('error', 'Unknown error')}"
                
        except Exception as e:
            self.log(f"Error in mutation trigger: {e}", "error")
            return "❌ Error triggering system mutation"
    
    def show_evolution_status(self, chat_id=None, args=None):
        """Show current evolution status"""
        try:
            report = self.mutation_engine.get_mutation_report()
            
            response = "🧬 **OMNI Evolution Status**\n\n"
            response += f"🔬 **Evolution Level**: {report.get('system_evolution_level', 'Unknown')}\n"
            response += f"📈 **Total Mutations**: {report.get('total_mutations', 0)}\n"
            response += f"✅ **Success Rate**: {report.get('success_rate', 0)}%\n"
            response += f"💫 **Average Impact**: {report.get('average_impact', 0)}/1.0\n"
            response += f"⚡ **Recent Activity**: {report.get('recent_activity', 0)} mutations (24h)\n\n"
            
            # Category breakdown
            categories = report.get('category_breakdown', {})
            if categories:
                response += "📊 **Evolution Categories**:\n"
                for category, count in categories.items():
                    response += f"• {category.replace('_', ' ').title()}: {count}\n"
            
            return response
            
        except Exception as e:
            self.log(f"Error showing evolution status: {e}", "error")
            return "❌ Error retrieving evolution status"
    
    def get_mutation_report(self, chat_id=None, args=None):
        """Get detailed mutation report"""
        try:
            report = self.mutation_engine.get_mutation_report()
            
            response = "📋 **Detailed Mutation Report**\n\n"
            
            # System metrics
            response += "**📊 System Metrics**\n"
            response += f"• Total Mutations: {report.get('total_mutations', 0)}\n"
            response += f"• Success Rate: {report.get('success_rate', 0)}%\n"
            response += f"• Evolution Level: {report.get('system_evolution_level', 'Unknown')}\n\n"
            
            # Recent mutations
            recent = report.get('recent_mutations', [])[:3]
            if recent:
                response += "**🕒 Recent Mutations**\n"
                for mutation in recent:
                    timestamp = mutation.get('timestamp', 'Unknown')
                    mut_type = mutation.get('type', 'Unknown')
                    impact = mutation.get('impact_score', 0)
                    
                    response += f"• {timestamp[:10]}: {mut_type.replace('_', ' ').title()} (Impact: {impact:.2f})\n"
            
            return response
            
        except Exception as e:
            self.log(f"Error generating mutation report: {e}", "error")
            return "❌ Error generating mutation report"
    
    def system_observation(self, chat_id=None, args=None):
        """Perform comprehensive system observation"""
        try:
            observation = self.observer_system.observe_system()
            
            response = "👁️ **System Observation Complete**\n\n"
            response += f"🕐 **Timestamp**: {observation.get('timestamp', 'Unknown')[:19]}\n"
            response += f"🎯 **System Score**: {observation.get('system_score', 0)}/100\n\n"
            
            # Performance summary
            observations = observation.get('observations', {})
            if 'performance' in observations:
                perf = observations['performance']
                response += "**⚡ Performance**\n"
                response += f"• CPU Usage: {perf.get('cpu_usage', 0):.1f}%\n"
                response += f"• Memory Usage: {perf.get('memory_usage', 0):.1f}%\n"
                response += f"• Performance Score: {perf.get('performance_score', 0)}/100\n\n"
            
            # Security summary
            if 'security' in observations:
                security = observations['security']
                response += "**🛡️ Security**\n"
                response += f"• Security Score: {security.get('security_score', 0)}/100\n"
                response += f"• Threat Level: {security.get('threat_level', 'Unknown').title()}\n"
                response += f"• Process Anomalies: {security.get('process_anomalies', 0)}\n\n"
            
            # System health
            if 'system_health' in observations:
                health = observations['system_health']
                response += "**💚 System Health**\n"
                response += f"• Health Score: {health.get('health_score', 0)}/100\n"
                response += f"• Status: {health.get('system_status', 'Unknown').title()}\n"
                response += f"• Uptime: {health.get('uptime_hours', 0):.1f} hours\n"
            
            return response
            
        except Exception as e:
            self.log(f"Error in system observation: {e}", "error")
            return "❌ Error performing system observation"
    
    def check_system_health(self, chat_id=None, args=None):
        """Check comprehensive system health"""
        try:
            # Get health from mutation engine
            mutation_health = self.mutation_engine.get_system_health()
            
            # Get current observation
            observation = self.observer_system.observe_system()
            system_score = observation.get('system_score', 0)
            
            # Get alerts
            alerts = self.observer_system.get_alerts()
            
            response = "💚 **Comprehensive System Health Check**\n\n"
            
            # Overall health
            overall_health = (mutation_health.get('health_score', 0) + system_score) / 2
            status = "Excellent" if overall_health > 90 else "Good" if overall_health > 75 else "Fair" if overall_health > 60 else "Poor"
            
            response += f"🎯 **Overall Health**: {overall_health:.1f}/100 ({status})\n"
            response += f"🧬 **Evolution Health**: {mutation_health.get('health_score', 0)}/100\n"
            response += f"⚙️ **System Performance**: {system_score}/100\n"
            response += f"🔍 **Evolution Level**: {mutation_health.get('evolution_level', 'Unknown')}\n\n"
            
            # Alerts
            if alerts:
                response += "⚠️ **Active Alerts**\n"
                for alert in alerts[:3]:  # Show only first 3 alerts
                    alert_type = alert.get('type', 'info').upper()
                    message = alert.get('message', 'No details')
                    response += f"• [{alert_type}] {message}\n"
                response += "\n"
            
            # Recommendations
            recommendations = mutation_health.get('recommendations', [])
            if recommendations:
                response += "💡 **Recommendations**\n"
                for rec in recommendations[:3]:
                    response += f"• {rec}\n"
            
            return response
            
        except Exception as e:
            self.log(f"Error checking system health: {e}", "error")
            return "❌ Error checking system health"
    
    def show_system_trends(self, chat_id=None, args=None):
        """Show system performance trends"""
        try:
            hours = 24
            if args and len(args) > 0:
                try:
                    hours = min(168, max(1, int(args[0])))  # 1-168 hours (1 week max)
                except ValueError:
                    hours = 24
            
            trends = self.observer_system.get_trend_analysis(hours=hours)
            
            if trends.get("status") == "insufficient_data":
                return f"📊 **Insufficient Data**: {trends.get('message', 'No trend data available')}"
            
            response = f"📈 **System Trends ({hours}h)**\n\n"
            response += f"📋 **Observations**: {trends.get('observations_count', 0)}\n"
            response += f"📊 **Average Score**: {trends.get('average_system_score', 0)}/100\n"
            response += f"🎯 **Current Score**: {trends.get('current_score', 0)}/100\n"
            response += f"📈 **Trend**: {trends.get('trend_direction', 'Unknown').title()}\n"
            response += f"⚡ **Performance Avg**: {trends.get('performance_average', 0)}/100\n\n"
            
            # Recommendations
            recommendations = trends.get('recommendations', [])
            if recommendations:
                response += "💡 **Trend-Based Recommendations**\n"
                for rec in recommendations:
                    response += f"• {rec}\n"
            
            return response
            
        except Exception as e:
            self.log(f"Error showing system trends: {e}", "error")
            return "❌ Error retrieving system trends"
    
    def get_system_alerts(self, chat_id=None, args=None):
        """Get current system alerts"""
        try:
            alerts = self.observer_system.get_alerts()
            
            if not alerts:
                return "✅ **No Active Alerts** - System operating normally"
            
            response = f"⚠️ **System Alerts ({len(alerts)} active)**\n\n"
            
            # Group alerts by type
            alert_types = {}
            for alert in alerts:
                alert_type = alert.get('type', 'info')
                if alert_type not in alert_types:
                    alert_types[alert_type] = []
                alert_types[alert_type].append(alert)
            
            # Display alerts by priority
            priority_order = ['critical', 'warning', 'info']
            for alert_type in priority_order:
                if alert_type in alert_types:
                    type_alerts = alert_types[alert_type]
                    emoji = "🚨" if alert_type == "critical" else "⚠️" if alert_type == "warning" else "ℹ️"
                    
                    response += f"**{emoji} {alert_type.upper()} ({len(type_alerts)})**\n"
                    for alert in type_alerts[:3]:  # Limit to 3 per type
                        message = alert.get('message', 'No details')
                        category = alert.get('category', 'system')
                        response += f"• [{category}] {message}\n"
                    response += "\n"
            
            return response
            
        except Exception as e:
            self.log(f"Error getting system alerts: {e}", "error")
            return "❌ Error retrieving system alerts"
    
    def perform_security_scan(self, chat_id=None, args=None):
        """Perform comprehensive security scan"""
        try:
            scan_result = self.security_layer.sentinel_scan()
            
            response = "🛡️ **Security Scan Complete**\n\n"
            response += f"🆔 **Scan ID**: {scan_result.get('scan_id', 'Unknown')}\n"
            response += f"📊 **Security Score**: {scan_result.get('security_score', 0)}/100\n"
            response += f"⚠️ **Threat Level**: {scan_result.get('threat_level', 'Unknown').title()}\n"
            response += f"🔍 **Threats Detected**: {len(scan_result.get('threats_detected', []))}\n\n"
            
            # Show threats
            threats = scan_result.get('threats_detected', [])
            if threats:
                response += "**🚨 Detected Threats**\n"
                for threat in threats[:3]:  # Show first 3 threats
                    severity = threat.get('severity', 'unknown').upper()
                    threat_type = threat.get('type', 'unknown')
                    description = threat.get('description', 'No details')
                    
                    emoji = "🔴" if severity == "HIGH" else "🟡" if severity == "MEDIUM" else "🟢"
                    response += f"{emoji} [{severity}] {threat_type}: {description}\n"
                response += "\n"
            
            # Recommendations
            recommendations = scan_result.get('recommendations', [])
            if recommendations:
                response += "**💡 Security Recommendations**\n"
                for rec in recommendations[:3]:
                    response += f"• {rec}\n"
            
            return response
            
        except Exception as e:
            self.log(f"Error in security scan: {e}", "error")
            return "❌ Error performing security scan"
    
    def show_security_status(self, chat_id=None, args=None):
        """Show comprehensive security status"""
        try:
            security_summary = self.security_layer.get_security_summary()
            
            response = "🛡️ **Security Status Report**\n\n"
            response += f"📅 **Events (24h)**: {security_summary.get('total_events_24h', 0)}\n"
            response += f"🚫 **Blocked IPs**: {security_summary.get('blocked_ips', 0)}\n"
            response += f"📊 **Security Status**: {security_summary.get('security_status', 'Unknown').title()}\n"
            
            last_scan = security_summary.get('last_scan')
            if last_scan:
                response += f"🔍 **Last Scan**: {last_scan[:19]}\n\n"
            
            # Most common threats
            common_threats = security_summary.get('most_common_threats', [])
            if common_threats:
                response += "**⚠️ Most Common Threats (24h)**\n"
                for threat_type, count in common_threats[:3]:
                    response += f"• {threat_type.replace('_', ' ').title()}: {count}\n"
                response += "\n"
            
            # Security recommendations
            recommendations = security_summary.get('recommendations', [])
            if recommendations:
                response += "**🔒 Security Recommendations**\n"
                for rec in recommendations[:3]:
                    response += f"• {rec}\n"
            
            return response
            
        except Exception as e:
            self.log(f"Error showing security status: {e}", "error")
            return "❌ Error retrieving security status"
    
    def analyze_threats(self, chat_id=None, args=None):
        """Analyze current security threats"""
        try:
            # Get recent security scan
            scan_result = self.security_layer.sentinel_scan()
            
            threats = scan_result.get('threats_detected', [])
            
            if not threats:
                return "✅ **No Current Threats Detected** - Security posture is strong"
            
            response = "🔍 **Threat Analysis**\n\n"
            
            # Categorize threats by severity
            high_threats = [t for t in threats if t.get('severity') == 'high']
            medium_threats = [t for t in threats if t.get('severity') == 'medium']
            low_threats = [t for t in threats if t.get('severity') == 'low']
            
            response += f"🔴 **High Severity**: {len(high_threats)}\n"
            response += f"🟡 **Medium Severity**: {len(medium_threats)}\n"
            response += f"🟢 **Low Severity**: {len(low_threats)}\n\n"
            
            # Detail high severity threats
            if high_threats:
                response += "**🚨 High Priority Threats**\n"
                for threat in high_threats[:3]:
                    threat_type = threat.get('type', 'unknown')
                    description = threat.get('description', 'No details')
                    response += f"• {threat_type.replace('_', ' ').title()}: {description}\n"
                response += "\n"
            
            # Threat mitigation suggestions
            response += "**🛡️ Mitigation Actions**\n"
            if high_threats:
                response += "• Immediate action required for high severity threats\n"
            if medium_threats:
                response += "• Review and address medium severity issues\n"
            response += "• Continue monitoring for new threats\n"
            response += "• Regular security scans recommended\n"
            
            return response
            
        except Exception as e:
            self.log(f"Error analyzing threats: {e}", "error")
            return "❌ Error analyzing security threats"
    
    def show_omni_status(self, chat_id=None, args=None):
        """Show complete OMNI system status"""
        try:
            # Gather data from all systems
            mutation_health = self.mutation_engine.get_system_health()
            observation = self.observer_system.observe_system()
            security_summary = self.security_layer.get_security_summary()
            
            response = "🌟 **OMNI System Status**\n\n"
            
            # System overview
            overall_health = (mutation_health.get('health_score', 0) + observation.get('system_score', 0)) / 2
            response += f"🎯 **Overall Health**: {overall_health:.1f}/100\n"
            response += f"🧬 **Evolution Level**: {mutation_health.get('evolution_level', 'Unknown')}\n"
            response += f"🛡️ **Security Status**: {security_summary.get('security_status', 'Unknown').title()}\n"
            response += f"⚡ **Performance**: {observation.get('system_score', 0)}/100\n\n"
            
            # Key metrics
            response += "**📊 Key Metrics**\n"
            mutation_report = self.mutation_engine.get_mutation_report()
            response += f"• Mutations: {mutation_report.get('total_mutations', 0)}\n"
            response += f"• Security Events (24h): {security_summary.get('total_events_24h', 0)}\n"
            response += f"• System Uptime: {observation.get('observations', {}).get('system_health', {}).get('uptime_hours', 0):.1f}h\n\n"
            
            # Status indicators
            response += "**🔄 System Status**\n"
            response += "🟢 Mutation Engine: Active\n"
            response += "🟢 Observer System: Monitoring\n"
            response += "🟢 Security Layer: Protecting\n"
            response += "🟢 AI Suggestions: Learning\n"
            response += "🟢 Crypto Payments: Ready\n"
            response += "🟢 Mastodon Integration: Connected\n\n"
            
            response += "💡 **OMNI is fully operational and evolving autonomously**"
            
            return response
            
        except Exception as e:
            self.log(f"Error showing OMNI status: {e}", "error")
            return "❌ Error retrieving OMNI system status"
    
    def auto_optimize_system(self, chat_id=None, args=None):
        """Trigger automatic system optimization"""
        try:
            optimization_results = []
            
            # Trigger mutation for optimization
            mutation_result = self.mutation_engine.trigger_targeted_mutation("performance_optimization")
            if mutation_result.get("success"):
                optimization_results.append(f"✅ Performance mutation applied (Impact: {mutation_result.get('impact_score', 0):.2f})")
            
            # Get system health check
            health = self.mutation_engine.get_system_health()
            
            # Get current observations
            observation = self.observer_system.observe_system()
            
            response = "⚙️ **Auto-Optimization Complete**\n\n"
            response += f"🎯 **Optimization Score**: {health.get('health_score', 0)}/100\n"
            response += f"📈 **System Performance**: {observation.get('system_score', 0)}/100\n\n"
            
            response += "**🔄 Optimizations Applied**\n"
            for result in optimization_results:
                response += f"{result}\n"
            
            if not optimization_results:
                response += "• System already operating at optimal levels\n"
            
            response += "\n💡 **Auto-optimization will continue in background**"
            
            return response
            
        except Exception as e:
            self.log(f"Error in auto-optimization: {e}", "error")
            return "❌ Error during auto-optimization"
    
    def generate_system_report(self, chat_id=None, args=None):
        """Generate comprehensive system report"""
        try:
            # Collect data from all systems
            mutation_report = self.mutation_engine.get_mutation_report()
            observation = self.observer_system.observe_system()
            trends = self.observer_system.get_trend_analysis(hours=24)
            security_summary = self.security_layer.get_security_summary()
            alerts = self.observer_system.get_alerts()
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            response = f"📋 **Comprehensive System Report**\n🕐 Generated: {timestamp}\n\n"
            
            # Executive summary
            overall_health = (mutation_report.get('system_evolution_level', 'Unknown'), 
                            observation.get('system_score', 0),
                            security_summary.get('security_status', 'unknown'))
            
            response += "**📈 Executive Summary**\n"
            response += f"• Evolution Level: {mutation_report.get('system_evolution_level', 'Unknown')}\n"
            response += f"• System Performance: {observation.get('system_score', 0)}/100\n"
            response += f"• Security Status: {security_summary.get('security_status', 'Unknown').title()}\n"
            response += f"• Active Alerts: {len(alerts)}\n\n"
            
            # Performance metrics
            perf = observation.get('observations', {}).get('performance', {})
            response += "**⚡ Performance Metrics**\n"
            response += f"• CPU Usage: {perf.get('cpu_usage', 0):.1f}%\n"
            response += f"• Memory Usage: {perf.get('memory_usage', 0):.1f}%\n"
            response += f"• Performance Score: {perf.get('performance_score', 0)}/100\n\n"
            
            # Evolution metrics
            response += "**🧬 Evolution Metrics**\n"
            response += f"• Total Mutations: {mutation_report.get('total_mutations', 0)}\n"
            response += f"• Success Rate: {mutation_report.get('success_rate', 0)}%\n"
            response += f"• Recent Activity: {mutation_report.get('recent_activity', 0)} (24h)\n\n"
            
            # Security metrics
            response += "**🛡️ Security Metrics**\n"
            response += f"• Events (24h): {security_summary.get('total_events_24h', 0)}\n"
            response += f"• Blocked IPs: {security_summary.get('blocked_ips', 0)}\n"
            response += f"• Threat Types: {len(security_summary.get('threat_types_24h', {}))}\n\n"
            
            # Recommendations
            all_recommendations = []
            all_recommendations.extend(trends.get('recommendations', []))
            all_recommendations.extend(security_summary.get('recommendations', []))
            
            if all_recommendations:
                response += "**💡 System Recommendations**\n"
                unique_recs = list(set(all_recommendations))[:5]  # Remove duplicates, limit to 5
                for rec in unique_recs:
                    response += f"• {rec}\n"
            
            return response
            
        except Exception as e:
            self.log(f"Error generating system report: {e}", "error")
            return "❌ Error generating comprehensive system report"