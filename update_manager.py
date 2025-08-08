import os
import git
import shutil
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from models import UpdateHistory
from app import db
from config import config
from utils.backup import BackupManager

logger = logging.getLogger(__name__)

class UpdateManager:
    """Manage automatic system updates from GitHub"""
    
    def __init__(self):
        self.repo_url = config.github_repo_url
        self.current_version = self.get_current_version()
        self.backup_manager = BackupManager()
        self.repo_dir = Path("./repo_cache")
    
    def get_current_version(self):
        """Get current system version"""
        try:
            if Path(".git").exists():
                repo = git.Repo(".")
                return repo.head.commit.hexsha[:7]
            else:
                return "unknown"
        except:
            return "unknown"
    
    def check_for_updates(self):
        """Check if updates are available"""
        try:
            # Clean up previous repo cache
            if self.repo_dir.exists():
                shutil.rmtree(self.repo_dir)
            
            # Clone repository to check for updates
            repo = git.Repo.clone_from(self.repo_url, self.repo_dir)
            latest_commit = repo.head.commit.hexsha[:7]
            
            if latest_commit != self.current_version:
                return {
                    'available': True,
                    'version': latest_commit,
                    'message': repo.head.commit.message.strip()
                }
            else:
                return {'available': False}
                
        except Exception as e:
            logger.error(f"Error checking for updates: {e}")
            return {'error': str(e)}
    
    def perform_update(self):
        """Perform the actual update"""
        update_record = UpdateHistory(
            version_from=self.current_version,
            status='pending'
        )
        db.session.add(update_record)
        db.session.commit()
        
        try:
            # Create backup
            backup_path = self.backup_manager.create_backup()
            update_record.backup_path = backup_path
            
            # Check for updates
            update_info = self.check_for_updates()
            if not update_info.get('available'):
                update_record.status = 'no_update'
                db.session.commit()
                return {'status': 'no_update'}
            
            new_version = update_info['version']
            update_record.version_to = new_version
            
            # Apply updates
            self.apply_updates()
            
            # Update requirements if needed
            if Path("requirements.txt").exists():
                subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
            
            # Update database schema if needed
            self.update_database_schema()
            
            # Restart application components
            self.restart_components()
            
            update_record.status = 'success'
            update_record.completed_at = datetime.utcnow()
            db.session.commit()
            
            logger.info(f"Successfully updated to version {new_version}")
            return {
                'status': 'updated',
                'version': new_version,
                'backup_path': backup_path
            }
            
        except Exception as e:
            logger.error(f"Update failed: {e}")
            
            update_record.status = 'failed'
            update_record.error_message = str(e)
            update_record.completed_at = datetime.utcnow()
            db.session.commit()
            
            # Attempt rollback
            try:
                self.rollback_update(update_record.backup_path)
                update_record.status = 'rolled_back'
                db.session.commit()
            except Exception as rollback_error:
                logger.error(f"Rollback failed: {rollback_error}")
            
            return {'status': 'failed', 'error': str(e)}
    
    def apply_updates(self):
        """Apply updates from cached repository"""
        if not self.repo_dir.exists():
            raise Exception("No cached repository found")
        
        # Copy updated files (excluding certain directories)
        exclude_dirs = {'.git', '__pycache__', 'instance', 'logs', 'backups'}
        exclude_files = {'omnicore.db', 'config.ini'}
        
        for item in self.repo_dir.iterdir():
            if item.name in exclude_dirs or item.name in exclude_files:
                continue
                
            dest = Path(item.name)
            
            if item.is_file():
                shutil.copy2(item, dest)
                logger.debug(f"Updated file: {item.name}")
            elif item.is_dir():
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(item, dest)
                logger.debug(f"Updated directory: {item.name}")
    
    def update_database_schema(self):
        """Update database schema if needed"""
        try:
            with db.app.app_context():
                db.create_all()
                logger.info("Database schema updated")
        except Exception as e:
            logger.warning(f"Database schema update failed: {e}")
    
    def restart_components(self):
        """Restart necessary components after update"""
        try:
            # Reload plugins
            from plugin_manager import PluginManager
            plugin_manager = PluginManager()
            plugin_manager.load_all_plugins()
            logger.info("Plugins reloaded after update")
            
        except Exception as e:
            logger.warning(f"Component restart failed: {e}")
    
    def rollback_update(self, backup_path):
        """Rollback to previous version"""
        if not backup_path or not Path(backup_path).exists():
            raise Exception("No backup available for rollback")
        
        self.backup_manager.restore_backup(backup_path)
        logger.info(f"Rolled back to backup: {backup_path}")
    
    def check_and_update(self):
        """Check for updates and apply if available"""
        if not config.auto_update_enabled:
            return {'status': 'disabled'}
        
        update_info = self.check_for_updates()
        if update_info.get('error'):
            return {'status': 'error', 'error': update_info['error']}
        
        if not update_info.get('available'):
            return {'status': 'no_update'}
        
        return self.perform_update()
    
    def get_update_history(self, limit=10):
        """Get recent update history"""
        return UpdateHistory.query.order_by(UpdateHistory.started_at.desc()).limit(limit).all()
