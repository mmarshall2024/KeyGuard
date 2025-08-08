import os
import shutil
import zipfile
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class BackupManager:
    """Manage system backups for safe updates"""
    
    def __init__(self, backup_dir="backups"):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
        self.max_backups = 10  # Keep only last 10 backups
    
    def create_backup(self):
        """Create a complete system backup"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"omnicore_backup_{timestamp}.zip"
        backup_path = self.backup_dir / backup_name
        
        try:
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Backup all Python files
                for py_file in Path(".").glob("**/*.py"):
                    if not any(exclude in str(py_file) for exclude in ['__pycache__', '.git', 'backups']):
                        zipf.write(py_file, py_file)
                
                # Backup templates
                for template in Path("templates").glob("**/*.html"):
                    zipf.write(template, template)
                
                # Backup static files
                if Path("static").exists():
                    for static_file in Path("static").glob("**/*"):
                        if static_file.is_file():
                            zipf.write(static_file, static_file)
                
                # Backup database (if SQLite)
                db_file = Path("omnicore.db")
                if db_file.exists():
                    zipf.write(db_file, db_file)
                
                # Backup configuration files
                config_files = ["config.ini", ".env"]
                for config_file in config_files:
                    if Path(config_file).exists():
                        zipf.write(config_file, config_file)
            
            logger.info(f"Backup created: {backup_path}")
            
            # Clean up old backups
            self._cleanup_old_backups()
            
            return str(backup_path)
            
        except Exception as e:
            logger.error(f"Backup creation failed: {e}")
            if backup_path.exists():
                backup_path.unlink()  # Remove incomplete backup
            raise
    
    def restore_backup(self, backup_path):
        """Restore system from backup"""
        backup_file = Path(backup_path)
        
        if not backup_file.exists():
            raise FileNotFoundError(f"Backup file not found: {backup_path}")
        
        try:
            # Create a temporary restore backup first
            temp_backup = self.create_backup()
            logger.info(f"Created temporary backup: {temp_backup}")
            
            with zipfile.ZipFile(backup_file, 'r') as zipf:
                # Extract all files
                zipf.extractall(".")
                
            logger.info(f"System restored from backup: {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"Backup restoration failed: {e}")
            # Try to restore from temporary backup
            try:
                if 'temp_backup' in locals():
                    with zipfile.ZipFile(temp_backup, 'r') as zipf:
                        zipf.extractall(".")
                    logger.info("Restored from temporary backup after failed restore")
            except:
                logger.error("Failed to restore from temporary backup")
            raise
    
    def list_backups(self):
        """List available backups"""
        backups = []
        
        for backup_file in self.backup_dir.glob("omnicore_backup_*.zip"):
            try:
                # Extract timestamp from filename
                timestamp_str = backup_file.stem.split('_')[-2] + '_' + backup_file.stem.split('_')[-1]
                timestamp = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                
                backups.append({
                    'path': str(backup_file),
                    'name': backup_file.name,
                    'timestamp': timestamp,
                    'size': backup_file.stat().st_size
                })
            except Exception as e:
                logger.warning(f"Could not parse backup file {backup_file}: {e}")
        
        # Sort by timestamp, newest first
        backups.sort(key=lambda x: x['timestamp'], reverse=True)
        return backups
    
    def delete_backup(self, backup_path):
        """Delete a specific backup"""
        backup_file = Path(backup_path)
        
        if backup_file.exists():
            backup_file.unlink()
            logger.info(f"Deleted backup: {backup_path}")
            return True
        else:
            logger.warning(f"Backup not found for deletion: {backup_path}")
            return False
    
    def get_backup_size(self):
        """Get total size of all backups"""
        total_size = 0
        
        for backup_file in self.backup_dir.glob("*.zip"):
            total_size += backup_file.stat().st_size
        
        return total_size
    
    def _cleanup_old_backups(self):
        """Remove old backups beyond the limit"""
        backups = self.list_backups()
        
        if len(backups) > self.max_backups:
            backups_to_delete = backups[self.max_backups:]
            
            for backup in backups_to_delete:
                self.delete_backup(backup['path'])
                logger.info(f"Cleaned up old backup: {backup['name']}")
    
    def verify_backup(self, backup_path):
        """Verify backup integrity"""
        backup_file = Path(backup_path)
        
        if not backup_file.exists():
            return False
        
        try:
            with zipfile.ZipFile(backup_file, 'r') as zipf:
                # Test the ZIP file
                bad_file = zipf.testzip()
                if bad_file:
                    logger.error(f"Backup corrupted, bad file: {bad_file}")
                    return False
                
                # Check for essential files
                essential_files = ['app.py', 'bot_core.py', 'models.py']
                file_list = zipf.namelist()
                
                for essential in essential_files:
                    if essential not in file_list:
                        logger.warning(f"Essential file missing from backup: {essential}")
                
                return True
                
        except Exception as e:
            logger.error(f"Backup verification failed: {e}")
            return False
