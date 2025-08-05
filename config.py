# Kisan Mitra Configuration File
# Store your API keys and configuration here

import os

# Try to import secrets, but don't fail if it doesn't exist
try:
    from secrets import GEMINI_API_KEY as SECRET_API_KEY
except ImportError:
    SECRET_API_KEY = None

# Use environment variable first, then secrets file, then fallback
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY') or SECRET_API_KEY or ""

# Flask Configuration
SECRET_KEY = 'kisan_mitra_secret_key_2025'
DEBUG = True

# Upload Configuration
UPLOAD_FOLDER = 'static/uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# AI Configuration
AI_ENABLED = True
AI_MODEL = 'gemini-1.5-flash'
AI_VISION_MODEL = 'gemini-1.5-flash'

def get_api_key():
    """Get API key from environment variable, secrets file, or config file"""
    # First try to get from environment variable
    env_key = os.getenv('GEMINI_API_KEY')
    if env_key and env_key.strip():
        return env_key
    
    # Try to get from secrets file
    try:
        from secrets import GEMINI_API_KEY as secret_key
        if secret_key and secret_key != "your_actual_gemini_api_key_here":
            return secret_key
    except ImportError:
        pass
    
    # Fallback to config file
    if GEMINI_API_KEY and GEMINI_API_KEY != "your_actual_gemini_api_key_here":
        return GEMINI_API_KEY
    
    return None

def is_ai_available():
    """Check if AI is available and configured"""
    try:
        import google.generativeai as genai
        api_key = get_api_key()
        return api_key is not None and api_key.strip() != ""
    except ImportError:
        return False

def print_api_key_status():
    """Print the status of API key configuration for debugging"""
    print("=== API Key Configuration Status ===")
    
    # Check environment variable
    env_key = os.getenv('GEMINI_API_KEY')
    if env_key:
        print("✅ Environment variable GEMINI_API_KEY is set")
    else:
        print("❌ Environment variable GEMINI_API_KEY is not set")
    
    # Check secrets file
    try:
        from secrets import GEMINI_API_KEY as secret_key
        if secret_key and secret_key != "your_actual_gemini_api_key_here":
            print("✅ Secrets file contains API key")
        else:
            print("❌ Secrets file has placeholder API key")
    except ImportError:
        print("❌ Secrets file not found")
    
    # Check config file
    if GEMINI_API_KEY and GEMINI_API_KEY != "your_actual_gemini_api_key_here":
        print("✅ Config file contains API key")
    else:
        print("❌ Config file has placeholder API key")
    
    # Final status
    if is_ai_available():
        print("✅ AI is available and configured")
    else:
        print("❌ AI is not available - no valid API key found")
    
    print("===================================") 