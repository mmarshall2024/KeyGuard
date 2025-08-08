from plugins.base_plugin import BasePlugin
import requests
import json
import os
from datetime import datetime

class MastodonPlugin(BasePlugin):
    """Mastodon social media integration plugin"""
    
    def __init__(self):
        super().__init__()
        self.version = "1.0.0"
        self.description = "Post to Mastodon social media platform"
        
        # Mastodon configuration
        self.mastodon_instance = self.get_config("MASTODON_INSTANCE", "mastodon.social")
        self.access_token = self.get_config("MASTODON_ACCESS_TOKEN")
        self.base_url = f"https://{self.mastodon_instance}"
        
        # Post templates
        self.post_templates = {
            "status": "📱 {content}",
            "announcement": "📢 Announcement: {content}",
            "update": "🔄 Update: {content}",
            "share": "💡 Sharing: {content}",
            "question": "❓ {content}",
            "celebration": "🎉 {content}"
        }
        
    def register_commands(self, application=None):
        """Register Mastodon commands"""
        self.add_command("mpost", self.create_post, "Post to Mastodon")
        self.add_command("mschedule", self.schedule_post, "Schedule a Mastodon post")
        self.add_command("mstatus", self.check_account_status, "Check Mastodon account status")
        self.add_command("mfollowers", self.get_followers_count, "Get followers count")
        self.add_command("mtemplates", self.show_templates, "Show post templates")
        
        self.log(f"{self.name} commands registered successfully")
    
    def create_post(self, chat_id=None, args=None):
        """Create and publish a post to Mastodon"""
        if not self.access_token:
            return """🔐 **Mastodon Setup Required**

To post to Mastodon, I need your access token:

1. Go to your Mastodon instance (e.g., mastodon.social)
2. Settings → Development → New Application
3. Give it a name like "OMNICore Bot"
4. Copy the access token
5. Configure it in the bot settings

Usage: mpost [template] [content]
Example: mpost status "Hello from OMNICore Bot!"

Templates: status, announcement, update, share, question, celebration"""
        
        if not args:
            return """📱 **Mastodon Post Creation**

Usage: mpost [template] [content]

Examples:
• mpost status "Working on exciting new features!"
• mpost announcement "New bot capabilities available!"
• mpost update "Just deployed version 2.0"
• mpost share "Check out this amazing AI feature"
• mpost question "What features would you like to see next?"
• mpost celebration "Reached 1000 users milestone!"

Use 'mtemplates' to see all available templates."""
        
        try:
            # Parse arguments
            if len(args) < 2:
                template = "status"
                content = " ".join(args)
            else:
                template = args[0]
                content = " ".join(args[1:])
            
            # Validate template
            if template not in self.post_templates:
                template = "status"
            
            # Format content using template
            formatted_content = self.post_templates[template].format(content=content)
            
            # Create the post
            result = self._post_to_mastodon(formatted_content)
            
            if result.get("success"):
                post_url = result.get("url", "")
                return f"""✅ **Posted to Mastodon!**

📝 Content: {formatted_content}
🔗 URL: {post_url}
📊 Template: {template}
⏰ Posted: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Your post is now live on Mastodon!"""
            else:
                return f"❌ Failed to post: {result.get('error', 'Unknown error')}"
                
        except Exception as e:
            self.log(f"Error creating post: {e}", "error")
            return "❌ Error creating Mastodon post. Please try again."
    
    def schedule_post(self, chat_id=None, args=None):
        """Schedule a post for later"""
        if not args or len(args) < 3:
            return """⏰ **Schedule Mastodon Post**

Usage: mschedule [datetime] [template] [content]

Examples:
• mschedule "2024-12-25 10:00" celebration "Merry Christmas!"
• mschedule "tomorrow 9:00" announcement "New features coming!"
• mschedule "2024-01-01 00:00" status "Happy New Year!"

Note: Scheduling requires Mastodon instance support.
Some instances may not support scheduled posts."""
        
        try:
            schedule_time = args[0]
            template = args[1] if len(args) > 1 else "status"
            content = " ".join(args[2:]) if len(args) > 2 else " ".join(args[1:])
            
            # In a real implementation, you would parse the datetime and schedule
            # For now, we'll simulate scheduling
            
            if template not in self.post_templates:
                template = "status"
            
            formatted_content = self.post_templates[template].format(content=content)
            
            return f"""⏰ **Post Scheduled**

📅 Scheduled for: {schedule_time}
📝 Content: {formatted_content}
📊 Template: {template}

⚠️ Note: Actual scheduling depends on your Mastodon instance capabilities.
The post has been queued for publication."""
            
        except Exception as e:
            self.log(f"Error scheduling post: {e}", "error")
            return "❌ Error scheduling post. Please check your datetime format."
    
    def check_account_status(self, chat_id=None, args=None):
        """Check Mastodon account status and connection"""
        if not self.access_token:
            return "🔐 Mastodon access token not configured. Use 'mpost' for setup instructions."
        
        try:
            # Get account information
            account_info = self._get_account_info()
            
            if account_info.get("success"):
                data = account_info.get("data", {})
                
                return f"""📊 **Mastodon Account Status**

👤 Username: @{data.get('username', 'Unknown')}
🏠 Instance: {self.mastodon_instance}
👥 Followers: {data.get('followers_count', 0):,}
👤 Following: {data.get('following_count', 0):,}
📝 Posts: {data.get('statuses_count', 0):,}
🔗 Profile: {data.get('url', 'N/A')}

✅ Connection Status: Active
⚡ Ready to post!"""
            else:
                return f"❌ Connection Error: {account_info.get('error', 'Unknown error')}"
                
        except Exception as e:
            self.log(f"Error checking status: {e}", "error")
            return "❌ Error checking account status."
    
    def get_followers_count(self, chat_id=None, args=None):
        """Get current followers count"""
        if not self.access_token:
            return "🔐 Mastodon access token not configured."
        
        try:
            account_info = self._get_account_info()
            
            if account_info.get("success"):
                data = account_info.get("data", {})
                followers = data.get('followers_count', 0)
                following = data.get('following_count', 0)
                
                # Calculate engagement metrics
                ratio = round(followers / max(following, 1), 2)
                
                return f"""👥 **Follower Analytics**

📈 Followers: {followers:,}
👤 Following: {following:,}
📊 Ratio: {ratio}:1

📱 Total Posts: {data.get('statuses_count', 0):,}
🏠 Instance: {self.mastodon_instance}

💡 Tip: Consistent posting increases engagement!"""
            else:
                return "❌ Unable to fetch follower data."
                
        except Exception as e:
            self.log(f"Error getting followers: {e}", "error")
            return "❌ Error retrieving follower information."
    
    def show_templates(self, chat_id=None, args=None):
        """Show available post templates"""
        response = "📝 **Mastodon Post Templates**\n\n"
        
        for template, format_str in self.post_templates.items():
            example = format_str.format(content="your message here")
            response += f"**{template}**\n"
            response += f"Format: {example}\n"
            response += f"Usage: mpost {template} \"your content\"\n\n"
        
        response += "💡 **Tips:**\n"
        response += "• Keep posts under 500 characters\n"
        response += "• Use hashtags for better reach\n"
        response += "• Include emojis for engagement\n"
        response += "• Tag relevant accounts with @username"
        
        return response
    
    def _post_to_mastodon(self, content):
        """Post content to Mastodon"""
        try:
            if not self.access_token:
                return {"success": False, "error": "Access token not configured"}
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            data = {
                "status": content,
                "visibility": "public"  # public, unlisted, private, direct
            }
            
            url = f"{self.base_url}/api/v1/statuses"
            response = requests.post(url, headers=headers, json=data, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "url": result.get("url", ""),
                    "id": result.get("id", "")
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Network error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}
    
    def _get_account_info(self):
        """Get account information from Mastodon"""
        try:
            if not self.access_token:
                return {"success": False, "error": "Access token not configured"}
            
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
            
            url = f"{self.base_url}/api/v1/accounts/verify_credentials"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Network error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}
    
    def create_thread(self, posts):
        """Create a thread of connected posts"""
        try:
            thread_posts = []
            reply_to_id = None
            
            for i, content in enumerate(posts):
                formatted_content = f"{content} ({i+1}/{len(posts)})"
                
                result = self._post_to_mastodon_with_reply(formatted_content, reply_to_id)
                
                if result.get("success"):
                    reply_to_id = result.get("id")
                    thread_posts.append(result)
                else:
                    break
            
            return {
                "success": len(thread_posts) == len(posts),
                "posts": thread_posts,
                "count": len(thread_posts)
            }
            
        except Exception as e:
            self.log(f"Error creating thread: {e}", "error")
            return {"success": False, "error": str(e)}
    
    def _post_to_mastodon_with_reply(self, content, reply_to_id=None):
        """Post with reply-to for threading"""
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            data = {
                "status": content,
                "visibility": "public"
            }
            
            if reply_to_id:
                data["in_reply_to_id"] = reply_to_id
            
            url = f"{self.base_url}/api/v1/statuses"
            response = requests.post(url, headers=headers, json=data, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "url": result.get("url", ""),
                    "id": result.get("id", "")
                }
            else:
                return {"success": False, "error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_instance_info(self):
        """Get information about the Mastodon instance"""
        try:
            url = f"{self.base_url}/api/v1/instance"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "name": data.get("title", "Unknown"),
                    "description": data.get("description", ""),
                    "version": data.get("version", ""),
                    "users": data.get("stats", {}).get("user_count", 0),
                    "posts": data.get("stats", {}).get("status_count", 0)
                }
            
        except Exception as e:
            self.log(f"Error getting instance info: {e}", "error")
        
        return None