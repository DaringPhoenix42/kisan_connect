@echo off
echo ========================================
echo    Kisan Mitra AI Setup Script
echo ========================================
echo.

echo Step 1: Installing AI package...
python -m pip install google-generativeai==0.3.2
echo.

echo Step 2: Setting up environment...
echo Please enter your Gemini API key (get it from https://makersuite.google.com/app/apikey):
set /p GEMINI_API_KEY="API Key: "
echo.

echo Step 3: Testing AI integration...
python -c "import google.generativeai as genai; print('✅ AI package installed successfully')"
echo.

echo Step 4: Starting the application...
echo Starting Kisan Mitra with AI integration...
python app.py

pause 