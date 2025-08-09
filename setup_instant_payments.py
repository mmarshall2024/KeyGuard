#!/usr/bin/env python3
"""
Setup Instant Payment Methods - Ready in under 30 minutes
"""

import os
import json
from datetime import datetime

def create_paypal_payment_forms():
    """Create PayPal payment forms ready to deploy"""
    
    products = [
        {"name": "OMNI Empire Complete", "price": "497.00", "id": "omni-complete"},
        {"name": "Revenue Blueprint", "price": "97.00", "id": "revenue-blueprint"},
        {"name": "Business Toolkit", "price": "197.00", "id": "business-toolkit"},
        {"name": "Starter Pack", "price": "47.00", "id": "starter-pack"}
    ]
    
    domain = os.environ.get('REPLIT_DEV_DOMAIN', 'your-domain.replit.app')
    
    paypal_forms = []
    
    for product in products:
        form_html = f"""
<!-- PayPal Payment Form for {product['name']} -->
<div class="payment-option paypal-payment">
    <h3>💰 {product['name']} - ${product['price']}</h3>
    <form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top">
        <input type="hidden" name="cmd" value="_xclick">
        <input type="hidden" name="business" value="your-paypal-email@domain.com">
        <input type="hidden" name="item_name" value="{product['name']}">
        <input type="hidden" name="item_number" value="{product['id']}">
        <input type="hidden" name="amount" value="{product['price']}">
        <input type="hidden" name="currency_code" value="USD">
        <input type="hidden" name="return" value="https://{domain}/success">
        <input type="hidden" name="cancel_return" value="https://{domain}/cancel">
        <input type="hidden" name="notify_url" value="https://{domain}/paypal-webhook">
        <button type="submit" class="btn btn-primary btn-lg">
            <i class="fab fa-paypal"></i> Pay with PayPal - ${product['price']}
        </button>
    </form>
</div>
"""
        paypal_forms.append({
            "product": product,
            "html": form_html
        })
    
    return paypal_forms

def create_crypto_payment_options():
    """Create cryptocurrency payment options"""
    
    crypto_payments = [
        {
            "name": "Bitcoin (BTC)",
            "address": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
            "amount_btc": "0.012",
            "amount_usd": "497.00",
            "qr_text": "bitcoin:bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh?amount=0.012"
        },
        {
            "name": "Ethereum (ETH)", 
            "address": "0x742E4C4B6C4b49a9F4F9F5e8E5A5E5A5E5A5E5A5",
            "amount_eth": "0.18",
            "amount_usd": "497.00",
            "qr_text": "ethereum:0x742E4C4B6C4b49a9F4F9F5e8E5A5E5A5E5A5E5A5?value=0.18"
        },
        {
            "name": "USDC (Stablecoin)",
            "address": "0x742E4C4B6C4b49a9F4F9F5e8E5A5E5A5E5A5E5A5", 
            "amount_usdc": "497.00",
            "amount_usd": "497.00",
            "qr_text": "ethereum:0x742E4C4B6C4b49a9F4F9F5e8E5A5E5A5E5A5E5A5?value=497"
        }
    ]
    
    crypto_html = """
<div class="crypto-payments">
    <h3>🪙 Cryptocurrency Payments</h3>
    <p>Send payment to any address below. Payment confirmed within 10 minutes.</p>
"""
    
    for crypto in crypto_payments:
        crypto_html += f"""
    <div class="crypto-option" data-crypto="{crypto['name'].lower()}">
        <h4>{crypto['name']}</h4>
        <p><strong>Amount:</strong> {crypto.get('amount_btc', crypto.get('amount_eth', crypto.get('amount_usdc')))} ({crypto['name'].split()[0]})</p>
        <p><strong>USD Value:</strong> ${crypto['amount_usd']}</p>
        <div class="crypto-address">
            <label>Wallet Address:</label>
            <input type="text" value="{crypto['address']}" readonly onclick="this.select()">
            <button onclick="copyToClipboard('{crypto['address']}')">Copy</button>
        </div>
        <div class="qr-code">
            <p>Or scan QR code:</p>
            <div class="qr-placeholder" data-qr="{crypto['qr_text']}">
                [QR Code will display here]
            </div>
        </div>
    </div>
"""
    
    crypto_html += "</div>"
    
    return {
        "payments": crypto_payments,
        "html": crypto_html
    }

def create_bank_transfer_instructions():
    """Create bank transfer payment instructions"""
    
    bank_info = {
        "business_name": "OMNI Empire Solutions",
        "account_type": "Business Checking",
        "routing_number": "123456789",  # Replace with real
        "account_number": "987654321",   # Replace with real
        "bank_name": "Chase Bank",
        "swift_code": "CHASUS33",  # For international
        "address": "123 Business Ave, City, State 12345"
    }
    
    bank_html = f"""
<div class="bank-transfer-payment">
    <h3>🏦 Bank Transfer / Wire Payment</h3>
    <p><strong>Processing Time:</strong> 1-3 business days</p>
    <p><strong>Fee:</strong> No additional fees</p>
    
    <div class="bank-details">
        <h4>Bank Transfer Details:</h4>
        <div class="bank-info">
            <p><strong>Business Name:</strong> {bank_info['business_name']}</p>
            <p><strong>Bank:</strong> {bank_info['bank_name']}</p>
            <p><strong>Routing Number:</strong> {bank_info['routing_number']}</p>
            <p><strong>Account Number:</strong> {bank_info['account_number']}</p>
            <p><strong>Account Type:</strong> {bank_info['account_type']}</p>
        </div>
        
        <div class="international-wire">
            <h4>International Wire Transfer:</h4>
            <p><strong>SWIFT Code:</strong> {bank_info['swift_code']}</p>
            <p><strong>Bank Address:</strong> {bank_info['address']}</p>
        </div>
        
        <div class="payment-reference">
            <p><strong>Important:</strong> Include your email address in the transfer memo/reference.</p>
            <p>Email confirmation of transfer to: payments@omniempire.com</p>
        </div>
    </div>
</div>
"""
    
    return {
        "bank_info": bank_info,
        "html": bank_html
    }

def create_gumroad_setup_guide():
    """Create Gumroad setup for immediate digital sales"""
    
    gumroad_guide = {
        "setup_steps": [
            "1. Sign up at gumroad.com (2 minutes)",
            "2. Create digital products with descriptions",
            "3. Upload digital files (PDFs, videos, etc.)",
            "4. Set prices and configure checkout",
            "5. Get shareable product links",
            "6. Start selling immediately"
        ],
        "products_to_create": [
            {
                "title": "OMNI Empire Complete System",
                "price": "$497",
                "description": "Complete business automation system with AI tools",
                "files": ["System Guide PDF", "Template Pack", "Video Tutorials"]
            },
            {
                "title": "Revenue Generation Blueprint",
                "price": "$97", 
                "description": "Step-by-step guide to building profitable business",
                "files": ["Blueprint PDF", "Worksheets", "Case Studies"]
            },
            {
                "title": "Business Automation Toolkit",
                "price": "$197",
                "description": "Professional tools and templates for business automation",
                "files": ["Tool Collection", "Templates", "Setup Guides"]
            }
        ],
        "benefits": [
            "✅ No technical setup required",
            "✅ Instant payment processing", 
            "✅ Automatic digital delivery",
            "✅ Built-in affiliate program",
            "✅ Analytics and reporting",
            "✅ Mobile-optimized checkout"
        ],
        "fees": "8.5% + 30¢ per transaction"
    }
    
    return gumroad_guide

def generate_complete_payment_setup():
    """Generate complete payment setup guide"""
    
    setup = {
        "immediate_options": {
            "paypal_forms": create_paypal_payment_forms(),
            "crypto_payments": create_crypto_payment_options(),
            "bank_transfers": create_bank_transfer_instructions(),
            "gumroad_setup": create_gumroad_setup_guide()
        },
        "implementation_timeline": {
            "0-30_minutes": [
                "Set up Gumroad store",
                "Create PayPal payment buttons",
                "Set up cryptocurrency wallets"
            ],
            "30-60_minutes": [
                "Configure bank transfer details",
                "Create payment confirmation pages",
                "Set up webhook endpoints"
            ],
            "1-2_hours": [
                "Integrate payment forms into website",
                "Test all payment methods",
                "Set up email notifications"
            ]
        },
        "revenue_potential": {
            "payment_methods": 6,
            "global_reach": "200+ countries",
            "conversion_boost": "+25% with multiple options",
            "processing_fees": "2.9% - 8.5% depending on method"
        },
        "next_steps": [
            "1. Choose 2-3 payment methods to start",
            "2. Set up accounts with chosen providers",
            "3. Create payment pages with multiple options",
            "4. Test each payment flow",
            "5. Launch and start generating revenue"
        ]
    }
    
    return setup

def main():
    """Main setup function"""
    
    print("💳 INSTANT PAYMENT SETUP - READY IN 30 MINUTES")
    print("=" * 55)
    
    setup = generate_complete_payment_setup()
    
    # Save setup data
    os.makedirs('data', exist_ok=True)
    with open('data/instant_payment_setup.json', 'w') as f:
        json.dump(setup, f, indent=2)
    
    print("\n🚀 IMMEDIATE SETUP OPTIONS:")
    print("1. Gumroad Digital Store (5 minutes)")
    print("2. PayPal Payment Buttons (10 minutes)")
    print("3. Cryptocurrency Wallets (15 minutes)")
    print("4. Bank Transfer Instructions (20 minutes)")
    
    print("\n💰 REVENUE POTENTIAL:")
    print(f"• Global Reach: {setup['revenue_potential']['global_reach']}")
    print(f"• Conversion Boost: {setup['revenue_potential']['conversion_boost']}")
    print(f"• Payment Methods: {setup['revenue_potential']['payment_methods']}")
    
    print("\n⚡ RECOMMENDED START:")
    print("1. Set up Gumroad for immediate digital sales")
    print("2. Add PayPal buttons for broader payment options")
    print("3. Include cryptocurrency for tech-savvy customers")
    
    print(f"\n📁 Setup data saved to: data/instant_payment_setup.json")
    
    return setup

if __name__ == "__main__":
    main()