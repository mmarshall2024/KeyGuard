from plugins.base_plugin import BasePlugin
import json
import os
import hashlib
import base64
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

class EmbedManagerPlugin(BasePlugin):
    """Advanced embed management system for saving and retrieving rich content"""
    
    def __init__(self):
        super().__init__()
        self.version = "1.0.0"
        self.description = "Comprehensive embed management for rich content storage and retrieval"
        
        # Storage configuration
        self.embeds_file = "data/saved_embeds.json"
        self.embed_cache_dir = "data/embed_cache"
        self.max_embed_size = 10 * 1024 * 1024  # 10MB limit
        
        # Embed types supported
        self.supported_types = {
            "text": {"extensions": [".txt", ".md"], "max_size": "1MB"},
            "image": {"extensions": [".jpg", ".jpeg", ".png", ".gif", ".webp"], "max_size": "5MB"},
            "document": {"extensions": [".pdf", ".doc", ".docx"], "max_size": "10MB"},
            "data": {"extensions": [".json", ".csv", ".xml"], "max_size": "2MB"},
            "code": {"extensions": [".py", ".js", ".html", ".css", ".sql"], "max_size": "1MB"},
            "media": {"extensions": [".mp3", ".mp4", ".wav"], "max_size": "50MB"}
        }
        
        # Initialize storage
        self._ensure_storage_directories()
        self.saved_embeds = self._load_saved_embeds()
        
    def _ensure_storage_directories(self):
        """Ensure all storage directories exist"""
        os.makedirs("data", exist_ok=True)
        os.makedirs(self.embed_cache_dir, exist_ok=True)
        
    def register_commands(self, application=None):
        """Register embed management commands"""
        self.add_command("save_embed", self.save_embed, "Save content as embed")
        self.add_command("load_embed", self.load_embed, "Load saved embed")
        self.add_command("list_embeds", self.list_saved_embeds, "List all saved embeds")
        self.add_command("delete_embed", self.delete_embed, "Delete saved embed")
        self.add_command("embed_info", self.get_embed_info, "Get embed information")
        self.add_command("search_embeds", self.search_embeds, "Search through saved embeds")
        self.add_command("export_embeds", self.export_embeds, "Export embeds collection")
        self.add_command("import_embeds", self.import_embeds, "Import embeds collection")
        
        self.log(f"{self.name} commands registered successfully")
    
    def save_embed(self, chat_id=None, args=None):
        """Save content as an embed with metadata"""
        if not args or len(args) < 2:
            return """💾 **Save Embed**

Usage: save_embed [name] [type] [content/url]

Examples:
• save_embed "project_notes" text "My important project notes here"
• save_embed "logo" image "https://example.com/logo.png"
• save_embed "config" data "{'api_key': 'value', 'settings': {...}}"
• save_embed "script" code "function hello() { console.log('Hello'); }"

Supported types: text, image, document, data, code, media

Use list_embeds to see all saved embeds."""
        
        try:
            embed_name = args[0].strip('"\'')
            embed_type = args[1].lower()
            content = " ".join(args[2:]).strip('"\'') if len(args) > 2 else ""
            
            if embed_type not in self.supported_types:
                supported_list = ", ".join(self.supported_types.keys())
                return f"❌ Unsupported embed type: {embed_type}\nSupported types: {supported_list}"
            
            if not content:
                return "❌ Content cannot be empty. Please provide content to save."
            
            # Generate embed ID
            embed_id = self._generate_embed_id(embed_name, content)
            
            # Process content based on type
            processed_content = self._process_content(content, embed_type)
            if not processed_content.get("success"):
                return f"❌ Error processing content: {processed_content.get('error', 'Unknown error')}"
            
            # Create embed record
            embed_record = {
                "id": embed_id,
                "name": embed_name,
                "type": embed_type,
                "content": processed_content["content"],
                "metadata": {
                    "size": processed_content.get("size", 0),
                    "created_at": datetime.now().isoformat(),
                    "created_by": f"user_{chat_id}" if chat_id else "system",
                    "access_count": 0,
                    "last_accessed": None,
                    "tags": self._extract_tags(content, embed_type),
                    "checksum": processed_content.get("checksum", "")
                },
                "storage": {
                    "method": processed_content.get("storage_method", "inline"),
                    "path": processed_content.get("storage_path", ""),
                    "compressed": processed_content.get("compressed", False)
                }
            }
            
            # Save embed
            self.saved_embeds[embed_id] = embed_record
            self._save_embeds_to_file()
            
            return f"""✅ **Embed Saved Successfully**

📝 **Name**: {embed_name}
🆔 **ID**: {embed_id}
📊 **Type**: {embed_type}
💾 **Size**: {self._format_size(embed_record['metadata']['size'])}
🕐 **Created**: {embed_record['metadata']['created_at'][:19]}
🏷️ **Tags**: {', '.join(embed_record['metadata']['tags']) if embed_record['metadata']['tags'] else 'None'}

Use `load_embed {embed_name}` to retrieve this embed."""
            
        except Exception as e:
            self.log(f"Error saving embed: {e}", "error")
            return "❌ Error saving embed. Please try again."
    
    def load_embed(self, chat_id=None, args=None):
        """Load and display a saved embed"""
        if not args:
            return """📂 **Load Embed**

Usage: load_embed [name_or_id]

Examples:
• load_embed "project_notes"
• load_embed "abc123def"

Use list_embeds to see all available embeds."""
        
        try:
            identifier = args[0].strip('"\'')
            
            # Find embed by name or ID
            embed_record = self._find_embed(identifier)
            if not embed_record:
                return f"❌ Embed not found: {identifier}\nUse list_embeds to see available embeds."
            
            # Update access statistics
            embed_record["metadata"]["access_count"] += 1
            embed_record["metadata"]["last_accessed"] = datetime.now().isoformat()
            self._save_embeds_to_file()
            
            # Load content
            content = self._load_embed_content(embed_record)
            if not content.get("success"):
                return f"❌ Error loading embed: {content.get('error', 'Unknown error')}"
            
            # Format response based on type
            response = f"""📂 **Loaded Embed: {embed_record['name']}**

🆔 **ID**: {embed_record['id']}
📊 **Type**: {embed_record['type']}
💾 **Size**: {self._format_size(embed_record['metadata']['size'])}
👁️ **Accessed**: {embed_record['metadata']['access_count']} times
🕐 **Created**: {embed_record['metadata']['created_at'][:19]}

"""
            
            # Add content based on type
            if embed_record['type'] == 'text':
                response += f"📄 **Content**:\n```\n{content['content']}\n```"
            elif embed_record['type'] == 'code':
                response += f"💻 **Code**:\n```{self._detect_language(content['content'])}\n{content['content']}\n```"
            elif embed_record['type'] == 'data':
                response += f"📊 **Data**:\n```json\n{content['content']}\n```"
            elif embed_record['type'] in ['image', 'document', 'media']:
                response += f"🔗 **File**: {embed_record['storage']['path']}\n"
                response += f"📥 **Size**: {self._format_size(embed_record['metadata']['size'])}"
            
            if embed_record['metadata']['tags']:
                response += f"\n🏷️ **Tags**: {', '.join(embed_record['metadata']['tags'])}"
            
            return response
            
        except Exception as e:
            self.log(f"Error loading embed: {e}", "error")
            return "❌ Error loading embed."
    
    def list_saved_embeds(self, chat_id=None, args=None):
        """List all saved embeds with filtering options"""
        try:
            filter_type = args[0].lower() if args and args[0] in self.supported_types else None
            
            if not self.saved_embeds:
                return "📂 No saved embeds found. Use save_embed to create your first embed."
            
            # Filter embeds
            filtered_embeds = {}
            for embed_id, embed_data in self.saved_embeds.items():
                if not filter_type or embed_data['type'] == filter_type:
                    filtered_embeds[embed_id] = embed_data
            
            if not filtered_embeds:
                return f"📂 No embeds found for type: {filter_type}"
            
            response = f"📂 **Saved Embeds ({len(filtered_embeds)})**"
            if filter_type:
                response += f" - Type: {filter_type}"
            response += "\n\n"
            
            # Sort by creation date (newest first)
            sorted_embeds = sorted(
                filtered_embeds.items(),
                key=lambda x: x[1]['metadata']['created_at'],
                reverse=True
            )
            
            for embed_id, embed_data in sorted_embeds[:20]:  # Limit to 20 most recent
                name = embed_data['name']
                embed_type = embed_data['type']
                size = self._format_size(embed_data['metadata']['size'])
                created = embed_data['metadata']['created_at'][:10]  # Date only
                access_count = embed_data['metadata']['access_count']
                
                response += f"📝 **{name}** ({embed_type})\n"
                response += f"   🆔 ID: {embed_id[:8]}...\n"
                response += f"   💾 Size: {size} | 📅 {created} | 👁️ {access_count} views\n\n"
            
            if len(filtered_embeds) > 20:
                response += f"... and {len(filtered_embeds) - 20} more embeds\n"
            
            response += "💡 Use `load_embed [name]` to retrieve an embed"
            
            return response
            
        except Exception as e:
            self.log(f"Error listing embeds: {e}", "error")
            return "❌ Error listing saved embeds."
    
    def delete_embed(self, chat_id=None, args=None):
        """Delete a saved embed"""
        if not args:
            return """🗑️ **Delete Embed**

Usage: delete_embed [name_or_id]

⚠️ **Warning**: This action cannot be undone!

Examples:
• delete_embed "old_notes"
• delete_embed "abc123def" """
        
        try:
            identifier = args[0].strip('"\'')
            
            # Find embed
            embed_record = self._find_embed(identifier)
            if not embed_record:
                return f"❌ Embed not found: {identifier}"
            
            embed_name = embed_record['name']
            embed_id = embed_record['id']
            
            # Delete file if stored separately
            if embed_record['storage']['method'] == 'file' and embed_record['storage']['path']:
                try:
                    file_path = os.path.join(self.embed_cache_dir, embed_record['storage']['path'])
                    if os.path.exists(file_path):
                        os.remove(file_path)
                except Exception as e:
                    self.log(f"Error deleting embed file: {e}", "warning")
            
            # Remove from memory and save
            del self.saved_embeds[embed_id]
            self._save_embeds_to_file()
            
            return f"""✅ **Embed Deleted**

📝 **Name**: {embed_name}
🆔 **ID**: {embed_id}

The embed has been permanently removed."""
            
        except Exception as e:
            self.log(f"Error deleting embed: {e}", "error")
            return "❌ Error deleting embed."
    
    def get_embed_info(self, chat_id=None, args=None):
        """Get detailed information about an embed"""
        if not args:
            return "📊 Usage: embed_info [name_or_id]"
        
        try:
            identifier = args[0].strip('"\'')
            embed_record = self._find_embed(identifier)
            
            if not embed_record:
                return f"❌ Embed not found: {identifier}"
            
            metadata = embed_record['metadata']
            storage = embed_record['storage']
            
            response = f"""📊 **Embed Information**

📝 **Basic Info**
• Name: {embed_record['name']}
• ID: {embed_record['id']}
• Type: {embed_record['type']}
• Size: {self._format_size(metadata['size'])}

📅 **Timeline**
• Created: {metadata['created_at'][:19]}
• Last Accessed: {metadata['last_accessed'][:19] if metadata['last_accessed'] else 'Never'}
• Access Count: {metadata['access_count']}

💾 **Storage**
• Method: {storage['method']}
• Compressed: {'Yes' if storage['compressed'] else 'No'}
• Checksum: {metadata['checksum'][:16]}...

🏷️ **Tags**: {', '.join(metadata['tags']) if metadata['tags'] else 'None'}

👤 **Created By**: {metadata['created_by']}"""
            
            return response
            
        except Exception as e:
            self.log(f"Error getting embed info: {e}", "error")
            return "❌ Error retrieving embed information."
    
    def search_embeds(self, chat_id=None, args=None):
        """Search through saved embeds"""
        if not args:
            return """🔍 **Search Embeds**

Usage: search_embeds [query]

Examples:
• search_embeds "project"
• search_embeds "code python"
• search_embeds "image logo"

Searches through embed names, types, and tags."""
        
        try:
            query = " ".join(args).lower()
            matches = []
            
            for embed_id, embed_data in self.saved_embeds.items():
                # Search in name, type, and tags
                search_text = f"{embed_data['name']} {embed_data['type']} {' '.join(embed_data['metadata']['tags'])}".lower()
                
                if query in search_text:
                    matches.append((embed_id, embed_data))
            
            if not matches:
                return f"🔍 No embeds found matching: {query}"
            
            response = f"🔍 **Search Results ({len(matches)} found)**\nQuery: {query}\n\n"
            
            for embed_id, embed_data in matches[:10]:  # Limit to 10 results
                name = embed_data['name']
                embed_type = embed_data['type']
                size = self._format_size(embed_data['metadata']['size'])
                
                response += f"📝 **{name}** ({embed_type})\n"
                response += f"   🆔 {embed_id[:12]}... | 💾 {size}\n"
                if embed_data['metadata']['tags']:
                    response += f"   🏷️ {', '.join(embed_data['metadata']['tags'])}\n"
                response += "\n"
            
            if len(matches) > 10:
                response += f"... and {len(matches) - 10} more results"
            
            return response
            
        except Exception as e:
            self.log(f"Error searching embeds: {e}", "error")
            return "❌ Error searching embeds."
    
    def export_embeds(self, chat_id=None, args=None):
        """Export embeds collection for backup"""
        try:
            export_data = {
                "export_info": {
                    "timestamp": datetime.now().isoformat(),
                    "total_embeds": len(self.saved_embeds),
                    "exported_by": f"user_{chat_id}" if chat_id else "system",
                    "version": self.version
                },
                "embeds": self.saved_embeds
            }
            
            # Generate export filename
            export_filename = f"embeds_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            export_path = os.path.join("data", export_filename)
            
            # Save export file
            with open(export_path, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            return f"""📤 **Embeds Exported Successfully**

📁 **File**: {export_filename}
📊 **Embeds**: {len(self.saved_embeds)}
💾 **Size**: {self._format_size(os.path.getsize(export_path))}
🕐 **Exported**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

The export file contains all your saved embeds and can be used for backup or migration."""
            
        except Exception as e:
            self.log(f"Error exporting embeds: {e}", "error")
            return "❌ Error exporting embeds collection."
    
    def import_embeds(self, chat_id=None, args=None):
        """Import embeds collection from backup"""
        if not args:
            return """📥 **Import Embeds**

Usage: import_embeds [filename]

Example: import_embeds "embeds_export_20241201_143022.json"

⚠️ **Note**: This will merge with existing embeds. Duplicates will be skipped."""
        
        try:
            filename = args[0].strip('"\'')
            import_path = os.path.join("data", filename)
            
            if not os.path.exists(import_path):
                return f"❌ File not found: {filename}"
            
            # Load import file
            with open(import_path, 'r') as f:
                import_data = json.load(f)
            
            if 'embeds' not in import_data:
                return "❌ Invalid import file format."
            
            # Import embeds
            imported_count = 0
            skipped_count = 0
            
            for embed_id, embed_data in import_data['embeds'].items():
                if embed_id in self.saved_embeds:
                    skipped_count += 1
                else:
                    self.saved_embeds[embed_id] = embed_data
                    imported_count += 1
            
            # Save updated embeds
            self._save_embeds_to_file()
            
            export_info = import_data.get('export_info', {})
            
            return f"""📥 **Import Complete**

📁 **Source**: {filename}
✅ **Imported**: {imported_count} embeds
⏩ **Skipped**: {skipped_count} (already exist)
📊 **Total Embeds**: {len(self.saved_embeds)}

Original export from: {export_info.get('timestamp', 'Unknown')[:19]}"""
            
        except Exception as e:
            self.log(f"Error importing embeds: {e}", "error")
            return "❌ Error importing embeds collection."
    
    def _process_content(self, content: str, embed_type: str) -> Dict[str, Any]:
        """Process content based on embed type"""
        try:
            # Check content size
            content_size = len(content.encode('utf-8'))
            if content_size > self.max_embed_size:
                return {
                    "success": False,
                    "error": f"Content too large: {self._format_size(content_size)} (max: {self._format_size(self.max_embed_size)})"
                }
            
            # Generate checksum
            checksum = hashlib.sha256(content.encode('utf-8')).hexdigest()
            
            # For small content, store inline
            if content_size < 1024:  # 1KB
                return {
                    "success": True,
                    "content": content,
                    "size": content_size,
                    "checksum": checksum,
                    "storage_method": "inline"
                }
            
            # For larger content, consider compression and file storage
            compressed_content = self._compress_content(content)
            use_compression = len(compressed_content) < content_size * 0.8
            
            if use_compression:
                final_content = base64.b64encode(compressed_content).decode('utf-8')
                return {
                    "success": True,
                    "content": final_content,
                    "size": content_size,
                    "checksum": checksum,
                    "storage_method": "inline",
                    "compressed": True
                }
            else:
                return {
                    "success": True,
                    "content": content,
                    "size": content_size,
                    "checksum": checksum,
                    "storage_method": "inline",
                    "compressed": False
                }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _compress_content(self, content: str) -> bytes:
        """Compress content using gzip"""
        import gzip
        return gzip.compress(content.encode('utf-8'))
    
    def _decompress_content(self, compressed_data: str) -> str:
        """Decompress content from base64 gzip"""
        import gzip
        compressed_bytes = base64.b64decode(compressed_data.encode('utf-8'))
        return gzip.decompress(compressed_bytes).decode('utf-8')
    
    def _generate_embed_id(self, name: str, content: str) -> str:
        """Generate unique embed ID"""
        timestamp = str(int(datetime.now().timestamp() * 1000))
        hash_input = f"{name}_{content}_{timestamp}"
        return hashlib.md5(hash_input.encode('utf-8')).hexdigest()[:12]
    
    def _extract_tags(self, content: str, embed_type: str) -> List[str]:
        """Extract relevant tags from content"""
        tags = [embed_type]
        
        # Add language tags for code
        if embed_type == 'code':
            language = self._detect_language(content)
            if language:
                tags.append(language)
        
        # Add common keywords
        keywords = ['config', 'api', 'data', 'image', 'script', 'notes', 'backup']
        for keyword in keywords:
            if keyword.lower() in content.lower():
                tags.append(keyword)
        
        return list(set(tags))
    
    def _detect_language(self, content: str) -> str:
        """Detect programming language from content"""
        if 'function' in content and '{' in content:
            return 'javascript'
        elif 'def ' in content and ':' in content:
            return 'python'
        elif '<html' in content.lower():
            return 'html'
        elif 'SELECT' in content.upper() or 'FROM' in content.upper():
            return 'sql'
        return ''
    
    def _find_embed(self, identifier: str) -> Optional[Dict[str, Any]]:
        """Find embed by name or ID"""
        # Try exact ID match first
        if identifier in self.saved_embeds:
            return self.saved_embeds[identifier]
        
        # Try name match
        for embed_id, embed_data in self.saved_embeds.items():
            if embed_data['name'] == identifier:
                return embed_data
        
        # Try partial ID match
        for embed_id, embed_data in self.saved_embeds.items():
            if embed_id.startswith(identifier):
                return embed_data
        
        return None
    
    def _load_embed_content(self, embed_record: Dict[str, Any]) -> Dict[str, Any]:
        """Load content from embed record"""
        try:
            content = embed_record['content']
            
            # Handle compressed content
            if embed_record['storage'].get('compressed', False):
                content = self._decompress_content(content)
            
            return {"success": True, "content": content}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f}TB"
    
    def _load_saved_embeds(self) -> Dict[str, Any]:
        """Load saved embeds from file"""
        try:
            with open(self.embeds_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_embeds_to_file(self):
        """Save embeds to file"""
        try:
            with open(self.embeds_file, 'w') as f:
                json.dump(self.saved_embeds, f, indent=2)
        except Exception as e:
            self.log(f"Error saving embeds to file: {e}", "error")
    
    def get_embed_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about saved embeds"""
        if not self.saved_embeds:
            return {"total_embeds": 0}
        
        stats = {
            "total_embeds": len(self.saved_embeds),
            "total_size": 0,
            "type_breakdown": {},
            "access_stats": {"most_accessed": None, "least_accessed": None},
            "creation_timeline": {},
            "compression_savings": 0
        }
        
        access_counts = []
        
        for embed_data in self.saved_embeds.values():
            # Size statistics
            stats["total_size"] += embed_data['metadata']['size']
            
            # Type breakdown
            embed_type = embed_data['type']
            stats["type_breakdown"][embed_type] = stats["type_breakdown"].get(embed_type, 0) + 1
            
            # Access statistics
            access_count = embed_data['metadata']['access_count']
            access_counts.append((embed_data['name'], access_count))
            
            # Creation timeline
            creation_date = embed_data['metadata']['created_at'][:10]
            stats["creation_timeline"][creation_date] = stats["creation_timeline"].get(creation_date, 0) + 1
        
        # Most/least accessed
        if access_counts:
            access_counts.sort(key=lambda x: x[1])
            stats["access_stats"]["least_accessed"] = access_counts[0]
            stats["access_stats"]["most_accessed"] = access_counts[-1]
        
        return stats