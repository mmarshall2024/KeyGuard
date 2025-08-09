#!/usr/bin/env python3
"""
Test Stripe Integration for Immediate Revenue Generation
"""

import os
import stripe
import json
from datetime import datetime

def test_stripe_connection():
    """Test the Stripe API connection and create test products"""
    
    # Get the Stripe key
    stripe_key = os.environ.get('STRIPE_SECRET_KEY')
    if not stripe_key:
        print("❌ No STRIPE_SECRET_KEY found in environment")
        return False
    
    print(f"🔑 Testing Stripe key: {stripe_key[:8]}...")
    
    # Set the API key
    stripe.api_key = stripe_key
    
    try:
        # Test the connection by listing products
        print("📡 Testing Stripe connection...")
        products = stripe.Product.list(limit=3)
        print(f"✅ Connected to Stripe successfully")
        print(f"📦 Found {len(products.data)} existing products")
        
        # Test creating a simple product
        print("\n💡 Creating test product...")
        test_product = stripe.Product.create(
            name="OMNI Empire Test Product",
            description="Test product for immediate revenue generation",
            type="service"
        )
        
        print(f"✅ Test product created: {test_product.id}")
        
        # Create a price
        test_price = stripe.Price.create(
            unit_amount=2900,  # $29
            currency='usd',
            product=test_product.id
        )
        
        print(f"✅ Test price created: {test_price.id}")
        
        # Create payment link
        payment_link = stripe.PaymentLink.create(
            line_items=[{"price": test_price.id, "quantity": 1}]
        )
        
        print(f"✅ Payment link created: {payment_link.url}")
        
        # Save the working configuration
        working_config = {
            "stripe_connected": True,
            "test_product_id": test_product.id,
            "test_price_id": test_price.id,
            "payment_link": payment_link.url,
            "created_at": datetime.now().isoformat()
        }
        
        os.makedirs('data', exist_ok=True)
        with open('data/stripe_test_results.json', 'w') as f:
            json.dump(working_config, f, indent=2)
        
        print("\n🎉 STRIPE INTEGRATION WORKING!")
        print(f"💰 Ready to accept payments at: {payment_link.url}")
        
        return working_config
        
    except stripe.error.AuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        return False
    except stripe.error.APIError as e:
        print(f"❌ API Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def create_instant_revenue_products():
    """Create ready-to-sell products for immediate revenue"""
    
    stripe_key = os.environ.get('STRIPE_SECRET_KEY')
    stripe.api_key = stripe_key
    
    products_to_create = [
        {
            "name": "OMNI Empire Starter Pack",
            "description": "Complete business automation system with AI tools and templates",
            "price": 97,
            "features": ["AI Business Tools", "Marketing Templates", "Automation Setup"]
        },
        {
            "name": "Revenue Acceleration Blueprint",
            "description": "Step-by-step guide to building profitable online business",
            "price": 47,
            "features": ["Revenue Strategies", "Marketing Funnels", "Lead Generation"]
        },
        {
            "name": "Business Empire Toolkit",
            "description": "Professional toolkit for scaling your business operations",
            "price": 197,
            "features": ["Advanced Tools", "Premium Templates", "1-on-1 Support"]
        }
    ]
    
    created_products = []
    
    for product_data in products_to_create:
        try:
            # Create product
            product = stripe.Product.create(
                name=product_data["name"],
                description=product_data["description"],
                type="service"
            )
            
            # Create price
            price = stripe.Price.create(
                unit_amount=product_data["price"] * 100,  # Convert to cents
                currency='usd',
                product=product.id
            )
            
            # Create payment link
            payment_link = stripe.PaymentLink.create(
                line_items=[{"price": price.id, "quantity": 1}]
            )
            
            product_info = {
                "product_id": product.id,
                "price_id": price.id,
                "name": product_data["name"],
                "description": product_data["description"],
                "price": product_data["price"],
                "features": product_data["features"],
                "payment_link": payment_link.url,
                "created_at": datetime.now().isoformat()
            }
            
            created_products.append(product_info)
            print(f"✅ Created: {product_data['name']} - ${product_data['price']}")
            print(f"🔗 Payment link: {payment_link.url}")
            
        except Exception as e:
            print(f"❌ Failed to create {product_data['name']}: {e}")
    
    # Save products for the web app
    if created_products:
        with open('data/live_products.json', 'w') as f:
            json.dump({
                "products": created_products,
                "total_products": len(created_products),
                "total_revenue_potential": sum(p["price"] for p in created_products),
                "created_at": datetime.now().isoformat()
            }, f, indent=2)
        
        print(f"\n🎯 {len(created_products)} products ready for immediate sales!")
        print(f"💰 Total revenue potential per customer: ${sum(p['price'] for p in created_products)}")
    
    return created_products

if __name__ == "__main__":
    print("🚀 TESTING STRIPE INTEGRATION FOR IMMEDIATE REVENUE")
    print("=" * 60)
    
    # Test basic connection
    test_result = test_stripe_connection()
    
    if test_result:
        print("\n" + "=" * 60)
        print("💰 CREATING INSTANT REVENUE PRODUCTS")
        print("=" * 60)
        
        # Create revenue products
        products = create_instant_revenue_products()
        
        if products:
            print("\n🎉 READY TO MAKE MONEY!")
            print("📱 Share these payment links now:")
            for product in products:
                print(f"• {product['name']}: {product['payment_link']}")
    else:
        print("❌ Stripe integration failed. Check your API key.")