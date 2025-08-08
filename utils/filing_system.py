"""
OMNI Empire Master Filing System - Comprehensive organizational structure
"""
import os
import json
import shutil
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class OMNIFilingSystem:
    """Master filing system for OMNI Empire organization"""
    
    def __init__(self):
        self.base_path = "OMNI_EMPIRE"
        self.filing_structure = {
            "01_Core_System": {
                "description": "Core bot system files and configurations",
                "subdirs": ["bot_core", "plugins", "configs", "models", "utils"],
                "file_types": [".py", ".json", ".md", ".yml"]
            },
            "02_Businesses": {
                "description": "Business logic and enterprise modules",
                "subdirs": ["revenue_streams", "client_management", "partnerships", "market_analysis"],
                "file_types": [".py", ".json", ".csv", ".md"]
            },
            "03_Automations": {
                "description": "Automation workflows and scripts",
                "subdirs": ["workflows", "triggers", "actions", "schedules"],
                "file_types": [".py", ".json", ".yml", ".sh"]
            },
            "04_Payments_Licensing": {
                "description": "Payment processing and licensing systems",
                "subdirs": ["stripe_integration", "crypto_payments", "licenses", "subscriptions"],
                "file_types": [".py", ".json", ".txt", ".md"]
            },
            "05_Voice_AI": {
                "description": "Voice AI and speech processing",
                "subdirs": ["voice_models", "speech_recognition", "tts_engines", "voice_cloning"],
                "file_types": [".py", ".wav", ".mp3", ".json"]
            },
            "06_Merch_Music_Generators": {
                "description": "Content generation for merchandise and music",
                "subdirs": ["image_generators", "music_composers", "merch_designs", "brand_assets"],
                "file_types": [".py", ".png", ".jpg", ".mp3", ".svg"]
            },
            "07_Telegram_Bots": {
                "description": "Telegram bot implementations and variations",
                "subdirs": ["main_bot", "specialized_bots", "bot_templates", "webhook_handlers"],
                "file_types": [".py", ".json", ".md", ".txt"]
            },
            "08_Mobile_Apps": {
                "description": "Mobile application components and PWAs",
                "subdirs": ["pwa_components", "app_templates", "mobile_apis", "app_configs"],
                "file_types": [".html", ".js", ".css", ".json", ".manifest"]
            },
            "09_Desktop_Launchers": {
                "description": "Desktop application launchers and installers",
                "subdirs": ["electron_apps", "native_apps", "installers", "updaters"],
                "file_types": [".js", ".py", ".exe", ".dmg", ".deb"]
            },
            "10_Web_Deployments": {
                "description": "Web deployment configurations and assets",
                "subdirs": ["flask_apps", "static_sites", "apis", "cdn_assets"],
                "file_types": [".py", ".html", ".js", ".css", ".json"]
            },
            "11_Vault_Logic": {
                "description": "Security vault and access control systems",
                "subdirs": ["encryption", "access_control", "key_management", "secure_storage"],
                "file_types": [".py", ".key", ".pem", ".json"]
            },
            "12_NFT_Token_Gates": {
                "description": "NFT and token-gated access systems",
                "subdirs": ["smart_contracts", "token_verification", "nft_metadata", "blockchain_apis"],
                "file_types": [".sol", ".py", ".json", ".md"]
            },
            "13_Debug_Backup_Security": {
                "description": "System debugging, backup, and security tools",
                "subdirs": ["debug_tools", "backup_systems", "security_scanners", "recovery_tools"],
                "file_types": [".py", ".log", ".backup", ".json"]
            },
            "14_Mutation_Logs": {
                "description": "System evolution and mutation tracking",
                "subdirs": ["evolution_history", "mutation_patterns", "adaptation_logs", "performance_metrics"],
                "file_types": [".json", ".log", ".csv", ".md"]
            },
            "15_AI_Clones": {
                "description": "AI personality clones and training data",
                "subdirs": ["personality_models", "training_datasets", "clone_configs", "behavioral_patterns"],
                "file_types": [".json", ".txt", ".py", ".pkl"]
            },
            "16_User_Data": {
                "description": "User data management and privacy controls",
                "subdirs": ["user_profiles", "preferences", "interaction_history", "privacy_controls"],
                "file_types": [".json", ".csv", ".enc", ".md"]
            },
            "17_Logs_Analytics": {
                "description": "System logs and analytics processing",
                "subdirs": ["system_logs", "analytics_data", "metrics", "reports"],
                "file_types": [".log", ".json", ".csv", ".html"]
            },
            "18_Branding_Assets": {
                "description": "Brand assets and marketing materials",
                "subdirs": ["logos", "templates", "color_schemes", "marketing_copy"],
                "file_types": [".png", ".svg", ".jpg", ".pdf", ".txt"]
            },
            "19_Legal_IP_Documents": {
                "description": "Legal documents and intellectual property",
                "subdirs": ["licenses", "terms_of_service", "privacy_policies", "ip_registrations"],
                "file_types": [".pdf", ".txt", ".md", ".doc"]
            },
            "20_Master_Control": {
                "description": "Master control panel and system orchestration",
                "subdirs": ["control_panel", "system_orchestration", "global_configs", "emergency_controls"],
                "file_types": [".py", ".json", ".yml", ".sh"]
            }
        }
        
        self.metadata_file = os.path.join(self.base_path, "filing_system_metadata.json")
        self._ensure_structure()
        self.metadata = self._load_metadata()
    
    def _ensure_structure(self):
        """Create the complete filing system structure"""
        try:
            # Create base directory
            os.makedirs(self.base_path, exist_ok=True)
            
            # Create all main directories and subdirectories
            for main_dir, config in self.filing_structure.items():
                main_path = os.path.join(self.base_path, main_dir)
                os.makedirs(main_path, exist_ok=True)
                
                # Create subdirectories
                for subdir in config["subdirs"]:
                    subdir_path = os.path.join(main_path, subdir)
                    os.makedirs(subdir_path, exist_ok=True)
                
                # Create README for each main directory
                readme_path = os.path.join(main_path, "README.md")
                if not os.path.exists(readme_path):
                    self._create_directory_readme(readme_path, main_dir, config)
            
            logger.info("OMNI Empire filing structure ensured")
            
        except Exception as e:
            logger.error(f"Error ensuring filing structure: {e}")
    
    def _create_directory_readme(self, readme_path: str, directory_name: str, config: Dict[str, Any]):
        """Create README file for directory"""
        content = f"""# {directory_name.replace('_', ' ').title()}

## Description
{config['description']}

## Structure
"""
        for subdir in config["subdirs"]:
            content += f"- `{subdir}/` - {subdir.replace('_', ' ').title()}\n"
        
        content += f"""
## Supported File Types
{', '.join(config['file_types'])}

## Last Updated
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        try:
            with open(readme_path, 'w') as f:
                f.write(content)
        except Exception as e:
            logger.error(f"Error creating README: {e}")
    
    def organize_file(self, file_path: str, category: str, subcategory: str = None) -> Dict[str, Any]:
        """Organize a file into the appropriate directory"""
        try:
            if category not in self.filing_structure:
                return {"success": False, "error": f"Invalid category: {category}"}
            
            if not os.path.exists(file_path):
                return {"success": False, "error": f"File not found: {file_path}"}
            
            # Determine destination
            if subcategory:
                dest_dir = os.path.join(self.base_path, category, subcategory)
            else:
                dest_dir = os.path.join(self.base_path, category)
            
            os.makedirs(dest_dir, exist_ok=True)
            
            # Get filename and create destination path
            filename = os.path.basename(file_path)
            dest_path = os.path.join(dest_dir, filename)
            
            # Handle duplicates by adding timestamp
            if os.path.exists(dest_path):
                name, ext = os.path.splitext(filename)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{name}_{timestamp}{ext}"
                dest_path = os.path.join(dest_dir, filename)
            
            # Move or copy file
            shutil.copy2(file_path, dest_path)
            
            # Update metadata
            self._update_file_metadata(dest_path, category, subcategory)
            
            return {
                "success": True,
                "original_path": file_path,
                "new_path": dest_path,
                "category": category,
                "subcategory": subcategory
            }
            
        except Exception as e:
            logger.error(f"Error organizing file: {e}")
            return {"success": False, "error": str(e)}
    
    def auto_organize_current_project(self) -> Dict[str, Any]:
        """Automatically organize current project files into appropriate categories"""
        organization_results = []
        
        try:
            # Define file mapping rules
            file_mappings = {
                "01_Core_System": {
                    "patterns": ["bot_core.py", "main.py", "app.py", "config.py", "models.py"],
                    "subdirs": {"*.py": "bot_core", "*.json": "configs", "*.md": "configs"}
                },
                "07_Telegram_Bots": {
                    "patterns": ["plugins/", "routes/"],
                    "subdirs": {"plugins/*": "main_bot", "routes/*": "webhook_handlers"}
                },
                "11_Vault_Logic": {
                    "patterns": ["utils/security_layer.py", "utils/mutation_engine.py"],
                    "subdirs": {"security_layer.py": "access_control", "mutation_engine.py": "secure_storage"}
                },
                "13_Debug_Backup_Security": {
                    "patterns": ["utils/observer_system.py"],
                    "subdirs": {"observer_system.py": "debug_tools"}
                },
                "14_Mutation_Logs": {
                    "patterns": ["data/mutation_history.json", "data/system_observations.json"],
                    "subdirs": {"mutation_history.json": "evolution_history", "system_observations.json": "mutation_patterns"}
                },
                "16_User_Data": {
                    "patterns": ["data/user_interactions.json"],
                    "subdirs": {"user_interactions.json": "interaction_history"}
                },
                "17_Logs_Analytics": {
                    "patterns": ["*.log"],
                    "subdirs": {"*.log": "system_logs"}
                }
            }
            
            # Scan project files
            for root, dirs, files in os.walk("."):
                for file in files:
                    file_path = os.path.join(root, file)
                    
                    # Skip already organized files
                    if self.base_path in file_path:
                        continue
                    
                    # Find appropriate category
                    category, subcategory = self._classify_file(file_path, file_mappings)
                    
                    if category:
                        result = self.organize_file(file_path, category, subcategory)
                        organization_results.append(result)
            
            # Update metadata
            self._save_metadata()
            
            return {
                "success": True,
                "organized_files": len([r for r in organization_results if r.get("success")]),
                "failed_files": len([r for r in organization_results if not r.get("success")]),
                "results": organization_results
            }
            
        except Exception as e:
            logger.error(f"Error auto-organizing project: {e}")
            return {"success": False, "error": str(e)}
    
    def _classify_file(self, file_path: str, mappings: Dict[str, Any]) -> tuple:
        """Classify a file into appropriate category and subcategory"""
        filename = os.path.basename(file_path)
        file_ext = os.path.splitext(filename)[1]
        
        for category, config in mappings.items():
            patterns = config.get("patterns", [])
            
            # Check if file matches any pattern
            for pattern in patterns:
                if pattern in file_path or pattern == filename:
                    # Find appropriate subdirectory
                    subdirs = config.get("subdirs", {})
                    for pattern_key, subdir in subdirs.items():
                        if pattern_key == filename or pattern_key == f"*{file_ext}":
                            return category, subdir
                    
                    # Return category with default subdirectory
                    return category, config.get("subdirs", {}).get("default", None)
        
        return None, None
    
    def get_filing_report(self) -> Dict[str, Any]:
        """Generate comprehensive filing system report"""
        try:
            report = {
                "timestamp": datetime.now().isoformat(),
                "total_categories": len(self.filing_structure),
                "categories": {},
                "file_statistics": {},
                "recent_activity": []
            }
            
            total_files = 0
            total_size = 0
            
            for category, config in self.filing_structure.items():
                category_path = os.path.join(self.base_path, category)
                
                if not os.path.exists(category_path):
                    continue
                
                category_stats = {
                    "description": config["description"],
                    "subdirectories": len(config["subdirs"]),
                    "files": 0,
                    "size": 0,
                    "last_modified": None
                }
                
                # Scan category directory
                for root, dirs, files in os.walk(category_path):
                    for file in files:
                        if file.endswith('.md'):  # Skip README files
                            continue
                        
                        file_path = os.path.join(root, file)
                        try:
                            stat = os.stat(file_path)
                            category_stats["files"] += 1
                            category_stats["size"] += stat.st_size
                            
                            file_mtime = datetime.fromtimestamp(stat.st_mtime)
                            if not category_stats["last_modified"] or file_mtime > category_stats["last_modified"]:
                                category_stats["last_modified"] = file_mtime.isoformat()
                        except OSError:
                            continue
                
                report["categories"][category] = category_stats
                total_files += category_stats["files"]
                total_size += category_stats["size"]
            
            report["file_statistics"] = {
                "total_files": total_files,
                "total_size": self._format_size(total_size),
                "average_file_size": self._format_size(total_size / max(total_files, 1))
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating filing report: {e}")
            return {"error": str(e)}
    
    def search_files(self, query: str, category: str = None) -> List[Dict[str, Any]]:
        """Search for files across the filing system"""
        try:
            results = []
            search_path = os.path.join(self.base_path, category) if category else self.base_path
            
            if not os.path.exists(search_path):
                return results
            
            query_lower = query.lower()
            
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    if query_lower in file.lower():
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, self.base_path)
                        
                        try:
                            stat = os.stat(file_path)
                            results.append({
                                "filename": file,
                                "path": rel_path,
                                "full_path": file_path,
                                "size": stat.st_size,
                                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                                "category": rel_path.split(os.sep)[0] if os.sep in rel_path else "root"
                            })
                        except OSError:
                            continue
            
            # Sort by relevance (exact matches first, then by modification time)
            results.sort(key=lambda x: (
                query_lower != x["filename"].lower(),  # Exact matches first
                -os.path.getmtime(x["full_path"])  # Then by newest first
            ))
            
            return results[:20]  # Limit to 20 results
            
        except Exception as e:
            logger.error(f"Error searching files: {e}")
            return []
    
    def create_backup(self) -> Dict[str, Any]:
        """Create complete backup of the filing system"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"omni_empire_backup_{timestamp}"
            backup_path = f"{backup_name}.zip"
            
            # Create zip archive
            shutil.make_archive(backup_name, 'zip', self.base_path)
            
            # Get backup stats
            backup_size = os.path.getsize(backup_path)
            
            return {
                "success": True,
                "backup_file": backup_path,
                "backup_size": self._format_size(backup_size),
                "timestamp": timestamp,
                "contents": self.get_filing_report()
            }
            
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return {"success": False, "error": str(e)}
    
    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f}TB"
    
    def _update_file_metadata(self, file_path: str, category: str, subcategory: str = None):
        """Update metadata for organized file"""
        try:
            rel_path = os.path.relpath(file_path, self.base_path)
            
            if "organized_files" not in self.metadata:
                self.metadata["organized_files"] = []
            
            file_info = {
                "path": rel_path,
                "category": category,
                "subcategory": subcategory,
                "organized_at": datetime.now().isoformat(),
                "size": os.path.getsize(file_path)
            }
            
            self.metadata["organized_files"].append(file_info)
            
        except Exception as e:
            logger.error(f"Error updating file metadata: {e}")
    
    def _load_metadata(self) -> Dict[str, Any]:
        """Load filing system metadata"""
        try:
            if os.path.exists(self.metadata_file):
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        
        return {
            "created_at": datetime.now().isoformat(),
            "version": "1.0.0",
            "organized_files": [],
            "system_stats": {}
        }
    
    def _save_metadata(self):
        """Save filing system metadata"""
        try:
            self.metadata["last_updated"] = datetime.now().isoformat()
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving metadata: {e}")
    
    def get_directory_structure(self, category: str = None) -> str:
        """Get formatted directory structure"""
        try:
            if category and category not in self.filing_structure:
                return f"Category '{category}' not found"
            
            structure = ""
            categories = {category: self.filing_structure[category]} if category else self.filing_structure
            
            for cat_name, config in categories.items():
                structure += f"\n📁 {cat_name.replace('_', ' ').title()}\n"
                structure += f"   {config['description']}\n"
                
                for subdir in config["subdirs"]:
                    subdir_path = os.path.join(self.base_path, cat_name, subdir)
                    file_count = 0
                    
                    if os.path.exists(subdir_path):
                        file_count = len([f for f in os.listdir(subdir_path) 
                                        if os.path.isfile(os.path.join(subdir_path, f)) and not f.endswith('.md')])
                    
                    structure += f"   ├── {subdir}/ ({file_count} files)\n"
                
                structure += f"   └── Supported: {', '.join(config['file_types'])}\n"
            
            return structure
            
        except Exception as e:
            logger.error(f"Error getting directory structure: {e}")
            return f"Error: {e}"