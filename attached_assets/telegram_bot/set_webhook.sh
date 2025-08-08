
#!/bin/bash
curl -F "url=https://your-domain.com/$(cat .env | grep TELEGRAM_TOKEN | cut -d '=' -f2)" "https://api.telegram.org/bot$(cat .env | grep TELEGRAM_TOKEN | cut -d '=' -f2)/setWebhook"
