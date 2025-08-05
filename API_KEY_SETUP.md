# 🔐 API Key Setup Guide

This guide explains how to securely set up your Gemini API key for the Kisan Mitra project.

## 🛡️ Security Setup

Your API key is stored securely in a separate file that will **never** be committed to GitHub.

### Files Created:
- `secrets.py` - Contains your actual API key (NOT committed to GitHub)
- `.gitignore` - Ensures secrets.py is ignored by Git
- `config.py` - Updated to import from secrets.py securely
- `setup_api_key.py` - Helper script for easy setup

## 🚀 Quick Setup

### Option 1: Automated Setup (Recommended)
```bash
python setup_api_key.py
```
This script will:
1. Create the `secrets.py` file if it doesn't exist
2. Prompt you for your API key
3. Save it securely
4. Test the configuration

### Option 2: Manual Setup
1. **Get your API key** from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Edit `secrets.py`** and replace the placeholder:
   ```python
   GEMINI_API_KEY = "your_actual_gemini_api_key_here"
   ```
   with your real API key:
   ```python
   GEMINI_API_KEY = "AIzaSyC..."  # Your actual key
   ```

## 🔍 How It Works

The system checks for your API key in this order:
1. **Environment Variable** (`GEMINI_API_KEY`)
2. **Secrets File** (`secrets.py`)
3. **Config File** (`config.py`)

### Priority Order:
```python
# config.py - Line 10
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY') or SECRET_API_KEY or ""
```

## 🧪 Testing Your Setup

Run this to check if your API key is working:
```python
from config import print_api_key_status, is_ai_available

print_api_key_status()
print(f"AI Available: {is_ai_available()}")
```

## 🔒 Security Features

### ✅ What's Protected:
- `secrets.py` is in `.gitignore`
- API key is never hardcoded in committed files
- Graceful fallback to mock data if API key is missing
- Environment variable support for production

### 🚫 What's NOT Committed:
- Your actual API key
- `secrets.py` file
- Any sensitive credentials

### ✅ What IS Committed:
- `config.py` (with placeholder)
- `setup_api_key.py` (helper script)
- `.gitignore` (security rules)
- All other project files

## 🌍 Environment Variables (Production)

For production deployment, you can set environment variables:

### Windows:
```cmd
set GEMINI_API_KEY=your_actual_api_key_here
```

### Linux/Mac:
```bash
export GEMINI_API_KEY=your_actual_api_key_here
```

### Python:
```python
import os
os.environ['GEMINI_API_KEY'] = 'your_actual_api_key_here'
```

## 🔧 Troubleshooting

### Issue: "API key not found"
**Solution:**
1. Check if `secrets.py` exists
2. Verify your API key is correct
3. Run `python setup_api_key.py` to test

### Issue: "AI not available"
**Solution:**
1. Check your API key format
2. Verify internet connection
3. Test with `from config import is_ai_available`

### Issue: "ImportError: No module named 'secrets'"
**Solution:**
1. Run `python setup_api_key.py` to create the file
2. Or manually create `secrets.py` with your API key

## 📋 File Structure

```
your-project/
├── config.py              # Main config (imports from secrets)
├── secrets.py             # Your API key (NOT committed)
├── setup_api_key.py       # Setup helper
├── .gitignore             # Security rules
├── app.py                 # Main application
└── ... (other files)
```

## 🎯 Next Steps

1. **Set up your API key** using the setup script
2. **Test the application** with `python app.py`
3. **Commit your code** to GitHub (secrets.py will be ignored)
4. **Deploy securely** using environment variables

## 🔗 Get Your API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key
5. Use it in the setup process

---

**Remember:** Never commit your actual API key to version control! The setup is designed to keep your secrets secure while making development easy. 