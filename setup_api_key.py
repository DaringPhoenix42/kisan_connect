#!/usr/bin/env python3
"""
Kisan Mitra API Key Setup Script
This script helps you securely set up your Gemini API key
"""

import os
import sys

def setup_api_key():
    """Interactive setup for API key"""
    print("🔐 Kisan Mitra API Key Setup")
    print("=" * 40)
    
    # Check if secrets.py exists
    if os.path.exists('secrets.py'):
        print("✅ secrets.py file found")
    else:
        print("❌ secrets.py file not found")
        print("Creating secrets.py file...")
        create_secrets_file()
    
    # Get API key from user
    print("\n📝 Please enter your Gemini API key:")
    print("(You can get it from: https://makersuite.google.com/app/apikey)")
    print("(Press Enter to skip if you want to set it later)")
    
    api_key = input("API Key: ").strip()
    
    if not api_key:
        print("\n⚠️  No API key entered. You can set it later by editing secrets.py")
        print_api_key_instructions()
        return
    
    # Update secrets.py
    update_secrets_file(api_key)
    
    print("\n✅ API key has been saved to secrets.py")
    print("🔒 This file is in .gitignore and will NOT be committed to GitHub")
    
    # Test the configuration
    test_configuration()

def create_secrets_file():
    """Create the secrets.py file"""
    secrets_content = '''# Kisan Mitra Secrets File
# Store your actual API keys here
# IMPORTANT: This file should NEVER be committed to GitHub
# Add this file to your .gitignore

# Your actual Gemini API key goes here
GEMINI_API_KEY = "your_actual_gemini_api_key_here"

# Add other sensitive data here if needed
# DATABASE_PASSWORD = "your_db_password"
# JWT_SECRET = "your_jwt_secret"
'''
    
    with open('secrets.py', 'w') as f:
        f.write(secrets_content)
    
    print("✅ Created secrets.py file")

def update_secrets_file(api_key):
    """Update the API key in secrets.py"""
    try:
        with open('secrets.py', 'r') as f:
            content = f.read()
        
        # Replace the placeholder with actual API key
        content = content.replace('GEMINI_API_KEY = "your_actual_gemini_api_key_here"', 
                                f'GEMINI_API_KEY = "{api_key}"')
        
        with open('secrets.py', 'w') as f:
            f.write(content)
        
        print("✅ Updated secrets.py with your API key")
        
    except Exception as e:
        print(f"❌ Error updating secrets.py: {e}")
        print("Please manually edit secrets.py and replace the placeholder with your API key")

def test_configuration():
    """Test if the API key is working"""
    print("\n🧪 Testing API key configuration...")
    
    try:
        from config import print_api_key_status, is_ai_available
        print_api_key_status()
        
        if is_ai_available():
            print("\n🎉 API key is working correctly!")
        else:
            print("\n⚠️  API key is not working. Please check your key.")
            
    except Exception as e:
        print(f"❌ Error testing configuration: {e}")

def print_api_key_instructions():
    """Print instructions for manual setup"""
    print("\n📋 Manual Setup Instructions:")
    print("1. Open secrets.py in your text editor")
    print("2. Replace 'your_actual_gemini_api_key_here' with your actual API key")
    print("3. Save the file")
    print("4. Run this script again to test the configuration")
    print("\n🔗 Get your API key from: https://makersuite.google.com/app/apikey")

def check_gitignore():
    """Check if secrets.py is in .gitignore"""
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            content = f.read()
            if 'secrets.py' in content:
                print("✅ secrets.py is in .gitignore")
                return True
            else:
                print("⚠️  secrets.py is NOT in .gitignore")
                return False
    else:
        print("⚠️  .gitignore file not found")
        return False

if __name__ == "__main__":
    print("🔒 Checking security setup...")
    check_gitignore()
    print()
    
    setup_api_key()
    
    print("\n🎯 Next steps:")
    print("1. Run 'python app.py' to start your application")
    print("2. Test the AI features to make sure everything works")
    print("3. Commit your code to GitHub (secrets.py will be ignored)") 