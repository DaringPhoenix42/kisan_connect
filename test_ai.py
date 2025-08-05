#!/usr/bin/env python3
"""
Simple test script to verify AI integration
"""

import os
import sys

def test_python():
    """Test if Python is working"""
    print("🐍 Python version:", sys.version)
    return True

def test_ai_package():
    """Test if AI package can be imported"""
    try:
        import google.generativeai as genai
        print("✅ AI package imported successfully")
        return True
    except ImportError as e:
        print(f"❌ AI package import failed: {e}")
        print("💡 Try: python -m pip install google-generativeai==0.3.2")
        return False

def test_api_key():
    """Test if API key is set"""
    try:
        from config import get_api_key, is_ai_available
        if is_ai_available():
            api_key = get_api_key()
            print("✅ API key found in config.py")
            return True
        else:
            print("❌ API key not found in config.py")
            print("💡 Add your API key to config.py file")
            return False
    except ImportError:
        print("❌ config.py not found")
        print("💡 Create config.py file with your API key")
        return False

def test_ai_connection():
    """Test AI connection"""
    try:
        from config import get_api_key, is_ai_available
        import google.generativeai as genai
        
        if not is_ai_available():
            print("⚠️ Skipping AI connection test - no valid API key")
            return False
            
        api_key = get_api_key()
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Simple test prompt
        response = model.generate_content("Say 'Hello from Kisan Mitra AI!'")
        print("✅ AI connection successful!")
        print(f"🤖 AI Response: {response.text}")
        return True
        
    except Exception as e:
        print(f"❌ AI connection failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("🤖 Kisan Mitra AI Integration Test")
    print("=" * 50)
    print()
    
    tests = [
        ("Python Installation", test_python),
        ("AI Package", test_ai_package),
        ("API Key", test_api_key),
        ("AI Connection", test_ai_connection)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"Testing {test_name}...")
        result = test_func()
        results.append((test_name, result))
        print()
    
    # Summary
    print("=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! AI integration is ready!")
        print("🚀 You can now run: python app.py")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
        print("📖 See AI_SETUP.md for detailed instructions.")

if __name__ == "__main__":
    main() 