import os
from app import db
from models import BotConfig

class Config:
    """Configuration manager with database storage and environment fallback"""
    
    @staticmethod
    def get(key, default=None, from_env=True):
        """Get configuration value from database or environment"""
        try:
            config = BotConfig.query.filter_by(key=key).first()
            if config:
                return config.value
        except:
            pass
        
        if from_env:
            return os.getenv(key, default)
        return default
    
    @staticmethod
    def set(key, value, encrypted=False):
        """Set configuration value in database"""
        try:
            config = BotConfig.query.filter_by(key=key).first()
            if config:
                config.value = value
                config.encrypted = encrypted
            else:
                config = BotConfig(key=key, value=value, encrypted=encrypted)
                db.session.add(config)
            db.session.commit()
            return True
        except Exception as e:
            print(f"Failed to set config {key}: {e}")
            return False
    
    # Bot configuration properties
    @property
    def telegram_token(self):
        return self.get("TELEGRAM_TOKEN")
    
    @property
    def stripe_secret_key(self):
        return self.get("STRIPE_SECRET_KEY")
    
    @property
    def stripe_public_key(self):
        return self.get("STRIPE_PUBLIC_KEY")
    
    @property
    def openai_api_key(self):
        return self.get("OPENAI_API_KEY")
    
    @property
    def devto_key(self):
        return self.get("DEVTO_KEY", "JMbH7SctGzT4ZzZLyshTMFxS")
    
    @property
    def crypto_wallet(self):
        return self.get("CRYPTO_WALLET", "0xYourCryptoAddressHere")
    
    @property
    def github_repo_url(self):
        return self.get("GITHUB_REPO_URL", "https://github.com/your-username/omnicore-bot.git")
    
    @property
    def auto_update_enabled(self):
        return self.get("AUTO_UPDATE_ENABLED", "true").lower() == "true"

# Global config instance
config = Config()
