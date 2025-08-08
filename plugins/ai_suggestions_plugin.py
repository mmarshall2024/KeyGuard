from plugins.base_plugin import BasePlugin
import json
import datetime
from collections import defaultdict, Counter
import requests
import os

class AISuggestionsPlugin(BasePlugin):
    """AI-driven feature suggestions based on usage patterns"""
    
    def __init__(self):
        super().__init__()
        self.version = "1.0.0"
        self.description = "Analyze usage patterns and suggest new features"
        
        # Usage tracking storage
        self.usage_file = "data/usage_patterns.json"
        self.suggestions_file = "data/ai_suggestions.json"
        
        # Initialize data storage
        self._ensure_data_directory()
        self.usage_data = self._load_usage_data()
        
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        import os
        os.makedirs("data", exist_ok=True)
        
    def register_commands(self, application=None):
        """Register AI suggestion commands"""
        self.add_command("suggest", self.get_suggestions, "Get AI-driven feature suggestions")
        self.add_command("usage_stats", self.show_usage_stats, "Show usage statistics")
        self.add_command("analyze_patterns", self.analyze_patterns, "Analyze user behavior patterns")
        
        self.log(f"{self.name} commands registered successfully")
    
    def track_usage(self, user_id, action, context=None):
        """Track user interaction for pattern analysis"""
        try:
            timestamp = datetime.datetime.now().isoformat()
            
            usage_entry = {
                "user_id": str(user_id),
                "action": action,
                "context": context or {},
                "timestamp": timestamp,
                "hour": datetime.datetime.now().hour,
                "day_of_week": datetime.datetime.now().weekday()
            }
            
            # Load current usage data
            if "interactions" not in self.usage_data:
                self.usage_data["interactions"] = []
            
            self.usage_data["interactions"].append(usage_entry)
            
            # Keep only last 1000 interactions to prevent file bloat
            if len(self.usage_data["interactions"]) > 1000:
                self.usage_data["interactions"] = self.usage_data["interactions"][-1000:]
            
            # Save updated data
            self._save_usage_data()
            
        except Exception as e:
            self.log(f"Error tracking usage: {e}", "error")
    
    def _load_usage_data(self):
        """Load usage data from file"""
        try:
            with open(self.usage_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "interactions": [],
                "feature_requests": [],
                "pain_points": []
            }
    
    def _save_usage_data(self):
        """Save usage data to file"""
        try:
            with open(self.usage_file, 'w') as f:
                json.dump(self.usage_data, f, indent=2)
        except Exception as e:
            self.log(f"Error saving usage data: {e}", "error")
    
    def get_suggestions(self, chat_id=None, args=None):
        """Generate AI-driven feature suggestions"""
        try:
            # Analyze current usage patterns
            patterns = self._analyze_usage_patterns()
            
            # Generate suggestions based on patterns
            suggestions = self._generate_suggestions(patterns)
            
            if not suggestions:
                return """🤖 **AI Feature Suggestions**

I'm still learning your usage patterns. Keep using the bot and I'll suggest personalized features based on:
• Most used commands
• Time-based usage patterns  
• Frequently requested features
• Pain points and gaps

Try using various features, and I'll analyze patterns to suggest improvements!"""
            
            response = "🤖 **AI-Driven Feature Suggestions**\n\n"
            
            for i, suggestion in enumerate(suggestions[:5], 1):
                response += f"**{i}. {suggestion['title']}**\n"
                response += f"📊 Confidence: {suggestion['confidence']}%\n"
                response += f"💡 Reason: {suggestion['reason']}\n"
                response += f"🎯 Impact: {suggestion['impact']}\n\n"
            
            response += "These suggestions are based on your usage patterns and current trends!"
            
            return response
            
        except Exception as e:
            self.log(f"Error generating suggestions: {e}", "error")
            return "❌ Error generating suggestions. Please try again."
    
    def _analyze_usage_patterns(self):
        """Analyze usage patterns from collected data"""
        interactions = self.usage_data.get("interactions", [])
        
        if not interactions:
            return {}
        
        # Analyze patterns
        patterns = {
            "most_used_commands": Counter(),
            "peak_hours": Counter(),
            "common_contexts": Counter(),
            "user_behavior": defaultdict(list),
            "temporal_patterns": {},
            "interaction_frequency": 0
        }
        
        for interaction in interactions:
            action = interaction.get("action", "")
            user_id = interaction.get("user_id", "")
            hour = interaction.get("hour", 0)
            context = interaction.get("context", {})
            
            patterns["most_used_commands"][action] += 1
            patterns["peak_hours"][hour] += 1
            patterns["user_behavior"][user_id].append(action)
            
            # Analyze context patterns
            if context:
                for key, value in context.items():
                    patterns["common_contexts"][f"{key}:{value}"] += 1
        
        patterns["interaction_frequency"] = len(interactions)
        
        return patterns
    
    def _generate_suggestions(self, patterns):
        """Generate feature suggestions based on patterns"""
        suggestions = []
        
        if not patterns or patterns.get("interaction_frequency", 0) < 5:
            return suggestions
        
        most_used = patterns.get("most_used_commands", Counter())
        peak_hours = patterns.get("peak_hours", Counter())
        
        # Suggestion 1: Enhanced popular features
        if most_used:
            top_command = most_used.most_common(1)[0]
            suggestions.append({
                "title": f"Enhanced {top_command[0].title()} Features",
                "reason": f"You use '{top_command[0]}' frequently ({top_command[1]} times)",
                "confidence": min(95, 60 + (top_command[1] * 5)),
                "impact": "High - Improves your most-used feature"
            })
        
        # Suggestion 2: Time-based automation
        if peak_hours:
            peak_hour = peak_hours.most_common(1)[0][0]
            suggestions.append({
                "title": "Smart Scheduling & Automation",
                "reason": f"Most active at {peak_hour}:00 - automation could help",
                "confidence": 75,
                "impact": "Medium - Reduces manual work during peak hours"
            })
        
        # Suggestion 3: Integration suggestions
        if "weather" in [cmd for cmd, count in most_used.most_common(3)]:
            suggestions.append({
                "title": "Location-Based Smart Notifications",
                "reason": "Weather requests suggest location awareness needs",
                "confidence": 80,
                "impact": "High - Proactive weather alerts and location features"
            })
        
        # Suggestion 4: Conversation enhancement
        if patterns.get("interaction_frequency", 0) > 20:
            suggestions.append({
                "title": "Advanced Conversation Memory",
                "reason": "High interaction frequency suggests need for context retention",
                "confidence": 85,
                "impact": "High - More natural, context-aware conversations"
            })
        
        # Suggestion 5: Productivity features
        if any("help" in cmd for cmd, count in most_used.most_common(5)):
            suggestions.append({
                "title": "Personalized Quick Actions",
                "reason": "Frequent help requests suggest need for easier access",
                "confidence": 70,
                "impact": "Medium - Faster access to common actions"
            })
        
        return suggestions
    
    def show_usage_stats(self, chat_id=None, args=None):
        """Show detailed usage statistics"""
        try:
            patterns = self._analyze_usage_patterns()
            
            if not patterns or patterns.get("interaction_frequency", 0) == 0:
                return "📊 No usage data available yet. Start using the bot to see statistics!"
            
            most_used = patterns.get("most_used_commands", Counter())
            peak_hours = patterns.get("peak_hours", Counter())
            
            response = "📊 **Usage Statistics**\n\n"
            response += f"🔄 Total Interactions: {patterns['interaction_frequency']}\n\n"
            
            # Top commands
            if most_used:
                response += "**🏆 Most Used Commands:**\n"
                for cmd, count in most_used.most_common(5):
                    percentage = (count / patterns['interaction_frequency']) * 100
                    response += f"• {cmd}: {count} times ({percentage:.1f}%)\n"
                response += "\n"
            
            # Peak hours
            if peak_hours:
                response += "**⏰ Peak Usage Hours:**\n"
                for hour, count in peak_hours.most_common(3):
                    response += f"• {hour:02d}:00 - {count} interactions\n"
                response += "\n"
            
            response += "Use /suggest to get AI-driven feature recommendations!"
            
            return response
            
        except Exception as e:
            self.log(f"Error showing stats: {e}", "error")
            return "❌ Error retrieving usage statistics."
    
    def analyze_patterns(self, chat_id=None, args=None):
        """Detailed pattern analysis"""
        try:
            patterns = self._analyze_usage_patterns()
            
            if not patterns or patterns.get("interaction_frequency", 0) < 3:
                return "🔍 Need more usage data for pattern analysis. Keep using the bot!"
            
            analysis = self._perform_deep_analysis(patterns)
            
            response = "🔍 **Deep Pattern Analysis**\n\n"
            
            if analysis.get("user_type"):
                response += f"👤 **User Profile**: {analysis['user_type']}\n"
                response += f"📈 **Engagement Level**: {analysis['engagement_level']}\n\n"
            
            if analysis.get("trends"):
                response += "📈 **Detected Trends:**\n"
                for trend in analysis["trends"]:
                    response += f"• {trend}\n"
                response += "\n"
            
            if analysis.get("recommendations"):
                response += "💡 **Optimization Recommendations:**\n"
                for rec in analysis["recommendations"]:
                    response += f"• {rec}\n"
            
            return response
            
        except Exception as e:
            self.log(f"Error in pattern analysis: {e}", "error")
            return "❌ Error performing pattern analysis."
    
    def _perform_deep_analysis(self, patterns):
        """Perform deep analysis of usage patterns"""
        analysis = {
            "user_type": "Standard User",
            "engagement_level": "Medium",
            "trends": [],
            "recommendations": []
        }
        
        frequency = patterns.get("interaction_frequency", 0)
        most_used = patterns.get("most_used_commands", Counter())
        
        # Determine user type
        if frequency > 50:
            analysis["user_type"] = "Power User"
            analysis["engagement_level"] = "High"
        elif frequency > 20:
            analysis["user_type"] = "Regular User"
            analysis["engagement_level"] = "Medium"
        else:
            analysis["user_type"] = "Casual User"
            analysis["engagement_level"] = "Low"
        
        # Detect trends
        if "weather" in [cmd for cmd, count in most_used.most_common(3)]:
            analysis["trends"].append("Location & Weather Focused Usage")
        
        if "joke" in [cmd for cmd, count in most_used.most_common(3)]:
            analysis["trends"].append("Entertainment & Social Features Popular")
        
        if frequency > 30:
            analysis["trends"].append("High Engagement - Daily Active User")
        
        # Generate recommendations
        if analysis["user_type"] == "Power User":
            analysis["recommendations"].extend([
                "Consider advanced automation features",
                "API integrations for productivity",
                "Custom command creation"
            ])
        else:
            analysis["recommendations"].extend([
                "Explore more bot features with /help",
                "Try natural conversation instead of commands",
                "Set up notifications for regular updates"
            ])
        
        return analysis
    
    def request_feature(self, user_id, feature_description):
        """Allow users to request specific features"""
        try:
            request = {
                "user_id": str(user_id),
                "description": feature_description,
                "timestamp": datetime.datetime.now().isoformat(),
                "status": "pending"
            }
            
            if "feature_requests" not in self.usage_data:
                self.usage_data["feature_requests"] = []
            
            self.usage_data["feature_requests"].append(request)
            self._save_usage_data()
            
            return "✅ Feature request submitted! The AI will consider this for future suggestions."
            
        except Exception as e:
            self.log(f"Error submitting feature request: {e}", "error")
            return "❌ Error submitting feature request."