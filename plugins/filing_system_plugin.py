from plugins.base_plugin import BasePlugin
from utils.filing_system import OMNIFilingSystem
import json
from datetime import datetime

class FilingSystemPlugin(BasePlugin):
    """OMNI Empire Master Filing System Management"""
    
    def __init__(self):
        super().__init__()
        self.version = "1.0.0"
        self.description = "Master filing system for OMNI Empire organization and management"
        
        # Initialize the filing system
        self.filing_system = OMNIFilingSystem()
        
    def register_commands(self, application=None):
        """Register filing system management commands"""
        self.add_command("file_organize", self.organize_file, "Organize a file into the filing system")
        self.add_command("auto_organize", self.auto_organize_project, "Automatically organize project files")
        self.add_command("filing_report", self.get_filing_report, "Get comprehensive filing system report")
        self.add_command("file_search", self.search_files, "Search for files in the filing system")
        self.add_command("filing_structure", self.show_directory_structure, "Show filing system structure")
        self.add_command("filing_backup", self.create_system_backup, "Create complete filing system backup")
        self.add_command("filing_status", self.show_filing_status, "Show current filing system status")
        
        self.log(f"{self.name} commands registered successfully")
    
    def organize_file(self, chat_id=None, args=None):
        """Organize a specific file into the filing system"""
        if not args or len(args) < 2:
            return """📁 **File Organization**

Usage: file_organize [file_path] [category] [subcategory]

**Available Categories:**
• 01_Core_System - Core bot system files
• 02_Businesses - Business logic and enterprise
• 03_Automations - Automation workflows
• 04_Payments_Licensing - Payment and licensing
• 05_Voice_AI - Voice AI and speech processing
• 07_Telegram_Bots - Telegram bot implementations
• 11_Vault_Logic - Security and access control
• 13_Debug_Backup_Security - Debug and security tools
• 14_Mutation_Logs - System evolution tracking
• 16_User_Data - User data management
• 17_Logs_Analytics - Logs and analytics
• 18_Branding_Assets - Brand assets and marketing

Example: file_organize "config.py" "01_Core_System" "configs" """
        
        try:
            file_path = args[0].strip('"\'')
            category = args[1]
            subcategory = args[2] if len(args) > 2 else None
            
            result = self.filing_system.organize_file(file_path, category, subcategory)
            
            if result.get("success"):
                return f"""✅ **File Organized Successfully**

📁 **Original**: {result['original_path']}
📂 **New Location**: {result['new_path']}
🗂️ **Category**: {result['category'].replace('_', ' ').title()}
📋 **Subcategory**: {result.get('subcategory', 'Main directory')}

File has been organized into the OMNI Empire filing system."""
            else:
                return f"❌ **Organization Failed**: {result.get('error', 'Unknown error')}"
                
        except Exception as e:
            self.log(f"Error organizing file: {e}", "error")
            return "❌ Error organizing file."
    
    def auto_organize_project(self, chat_id=None, args=None):
        """Automatically organize all project files"""
        try:
            result = self.filing_system.auto_organize_current_project()
            
            if result.get("success"):
                organized = result.get("organized_files", 0)
                failed = result.get("failed_files", 0)
                
                response = f"""🤖 **Auto-Organization Complete**

✅ **Successfully Organized**: {organized} files
❌ **Failed**: {failed} files
📊 **Total Processed**: {organized + failed} files

🗂️ **OMNI Empire Filing System Active**

"""
                # Show some examples of organized files
                successful_results = [r for r in result.get("results", []) if r.get("success")]
                if successful_results:
                    response += "**Recent Organizations:**\n"
                    for i, res in enumerate(successful_results[:5]):
                        filename = res.get("new_path", "").split('/')[-1]
                        category = res.get("category", "").replace('_', ' ').title()
                        response += f"• {filename} → {category}\n"
                    
                    if len(successful_results) > 5:
                        response += f"... and {len(successful_results) - 5} more files\n"
                
                response += "\nUse `filing_report` to see complete organization status."
                return response
            else:
                return f"❌ **Auto-Organization Failed**: {result.get('error', 'Unknown error')}"
                
        except Exception as e:
            self.log(f"Error in auto-organization: {e}", "error")
            return "❌ Error during automatic organization."
    
    def get_filing_report(self, chat_id=None, args=None):
        """Generate comprehensive filing system report"""
        try:
            report = self.filing_system.get_filing_report()
            
            if "error" in report:
                return f"❌ **Report Error**: {report['error']}"
            
            stats = report.get("file_statistics", {})
            categories = report.get("categories", {})
            
            response = f"""📊 **OMNI Empire Filing System Report**

🗂️ **System Statistics**
• Total Categories: {report.get('total_categories', 0)}
• Total Files: {stats.get('total_files', 0)}
• Total Size: {stats.get('total_size', '0B')}
• Average File Size: {stats.get('average_file_size', '0B')}

**📁 Category Breakdown**
"""
            
            # Show top categories by file count
            sorted_categories = sorted(
                categories.items(),
                key=lambda x: x[1].get("files", 0),
                reverse=True
            )
            
            for category, data in sorted_categories[:8]:  # Show top 8 categories
                name = category.replace('_', ' ').title()
                files = data.get("files", 0)
                size = self.filing_system._format_size(data.get("size", 0))
                
                if files > 0:
                    response += f"• {name}: {files} files ({size})\n"
            
            response += f"\n🕐 **Generated**: {report.get('timestamp', '')[:19]}"
            response += "\n💡 Use `filing_structure` to see detailed directory layout"
            
            return response
            
        except Exception as e:
            self.log(f"Error generating filing report: {e}", "error")
            return "❌ Error generating filing system report."
    
    def search_files(self, chat_id=None, args=None):
        """Search for files in the filing system"""
        if not args:
            return """🔍 **File Search**

Usage: file_search [query] [category]

Examples:
• file_search "config"
• file_search "plugin" "01_Core_System"
• file_search ".py"

Search through filenames in the OMNI Empire filing system."""
        
        try:
            query = args[0].strip('"\'')
            category = args[1] if len(args) > 1 else None
            
            results = self.filing_system.search_files(query, category)
            
            if not results:
                search_scope = f" in category '{category}'" if category else ""
                return f"🔍 No files found matching '{query}'{search_scope}"
            
            response = f"🔍 **Search Results ({len(results)} found)**\n"
            response += f"Query: '{query}'"
            if category:
                response += f" in {category.replace('_', ' ').title()}"
            response += "\n\n"
            
            for result in results[:10]:  # Limit to 10 results
                filename = result["filename"]
                path = result["path"]
                size = self.filing_system._format_size(result["size"])
                modified = result["modified"][:10]  # Date only
                
                response += f"📄 **{filename}**\n"
                response += f"   📂 {path}\n"
                response += f"   💾 {size} | 📅 {modified}\n\n"
            
            if len(results) > 10:
                response += f"... and {len(results) - 10} more results\n"
            
            return response
            
        except Exception as e:
            self.log(f"Error searching files: {e}", "error")
            return "❌ Error searching filing system."
    
    def show_directory_structure(self, chat_id=None, args=None):
        """Show filing system directory structure"""
        try:
            category = args[0] if args else None
            
            if category and category not in self.filing_system.filing_structure:
                available = ", ".join(list(self.filing_system.filing_structure.keys())[:5])
                return f"❌ Invalid category: {category}\nAvailable: {available}..."
            
            structure = self.filing_system.get_directory_structure(category)
            
            title = f"📁 **OMNI Empire Filing Structure**"
            if category:
                title += f" - {category.replace('_', ' ').title()}"
            
            response = title + "\n" + structure
            
            if not category:
                response += "\n💡 Use `filing_structure [category]` to see specific category details"
            
            return response
            
        except Exception as e:
            self.log(f"Error showing directory structure: {e}", "error")
            return "❌ Error retrieving directory structure."
    
    def create_system_backup(self, chat_id=None, args=None):
        """Create complete filing system backup"""
        try:
            result = self.filing_system.create_backup()
            
            if result.get("success"):
                return f"""💾 **Filing System Backup Created**

📁 **Backup File**: {result['backup_file']}
💾 **Size**: {result['backup_size']}
🕐 **Timestamp**: {result['timestamp']}

**System Contents:**
• Total Categories: {result['contents'].get('total_categories', 0)}
• Total Files: {result['contents'].get('file_statistics', {}).get('total_files', 0)}
• Total Size: {result['contents'].get('file_statistics', {}).get('total_size', '0B')}

Backup includes complete OMNI Empire filing system with all organized files and metadata."""
            else:
                return f"❌ **Backup Failed**: {result.get('error', 'Unknown error')}"
                
        except Exception as e:
            self.log(f"Error creating backup: {e}", "error")
            return "❌ Error creating filing system backup."
    
    def show_filing_status(self, chat_id=None, args=None):
        """Show current filing system status and health"""
        try:
            report = self.filing_system.get_filing_report()
            
            if "error" in report:
                return f"❌ **Status Check Failed**: {report['error']}"
            
            stats = report.get("file_statistics", {})
            categories = report.get("categories", {})
            
            # Calculate health metrics
            active_categories = len([c for c in categories.values() if c.get("files", 0) > 0])
            total_categories = report.get("total_categories", 0)
            utilization = (active_categories / total_categories * 100) if total_categories > 0 else 0
            
            # Determine system status
            if utilization > 80:
                status = "🟢 Excellent"
            elif utilization > 60:
                status = "🟡 Good"
            elif utilization > 40:
                status = "🟠 Fair"
            else:
                status = "🔴 Poor"
            
            response = f"""📊 **OMNI Empire Filing Status**

🎯 **System Health**: {status} ({utilization:.1f}% utilized)
📁 **Active Categories**: {active_categories}/{total_categories}
📄 **Total Files**: {stats.get('total_files', 0)}
💾 **Total Storage**: {stats.get('total_size', '0B')}

**🔥 Most Active Categories:**
"""
            
            # Show most active categories
            active_cats = [(k, v) for k, v in categories.items() if v.get("files", 0) > 0]
            active_cats.sort(key=lambda x: x[1].get("files", 0), reverse=True)
            
            for category, data in active_cats[:5]:
                name = category.replace('_', ' ').title()
                files = data.get("files", 0)
                response += f"• {name}: {files} files\n"
            
            if not active_cats:
                response += "• No files organized yet - use `auto_organize` to start\n"
            
            response += "\n💡 **Recommendations:**\n"
            if utilization < 50:
                response += "• Run `auto_organize` to organize project files\n"
            if stats.get("total_files", 0) > 100:
                response += "• Consider creating a backup with `filing_backup`\n"
            response += "• Use `file_search` to quickly locate organized files"
            
            return response
            
        except Exception as e:
            self.log(f"Error checking filing status: {e}", "error")
            return "❌ Error checking filing system status."