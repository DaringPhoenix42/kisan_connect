import google.generativeai as genai
import os
from datetime import datetime
import json

class KisanMitraAI:
    def __init__(self, api_key):
        """Initialize the AI system with Gemini API"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    def get_crop_recommendation(self, location, soil_type, irrigation, land_area, season, budget):
        """
        Get AI-powered crop recommendations using Gemini
        """
        
        # Create a comprehensive prompt for the AI
        prompt = f"""
        You are an expert agricultural AI assistant for Indian farmers. Based on the following parameters, 
        provide detailed crop recommendations for maximum profitability and sustainability.

        FARMER PARAMETERS:
        - Location: {location}, Maharashtra, India
        - Soil Type: {soil_type}
        - Irrigation: {irrigation}
        - Land Area: {land_area} acres
        - Season: {season}
        - Budget: ₹{budget:,}

        CURRENT CONTEXT:
        - Date: {datetime.now().strftime('%B %Y')}
        - Current Season: Kharif (Monsoon) - July to October
        - Market Conditions: High demand for pulses and oilseeds

        REQUIREMENTS:
        1. Recommend 3-4 best crops with confidence scores (0-100)
        2. For each crop, provide:
           - Scientific name and common name
           - MSP (Minimum Support Price) per quintal
           - Water requirement (Low/Moderate/High)
           - Time to harvest (days)
           - Risk level (Low/Moderate/High)
           - Expected profit per acre
           - Market demand analysis
           - Specific reason for recommendation

        3. Consider:
           - Soil suitability
           - Climate conditions
           - Market prices and demand
           - Water availability
           - Seasonal timing
           - Government support schemes
           - Pest and disease resistance

        4. Provide additional insights:
           - Best planting time
           - Required fertilizers
           - Pest management tips
           - Market timing for selling

        RESPONSE FORMAT:
        Return a JSON object with the following structure:
        {{
            "location": "location_name",
            "analysis_date": "current_date",
            "recommendations": [
                {{
                    "crop": "crop_key",
                    "confidence": confidence_score,
                    "reason": "detailed_reasoning",
                    "data": {{
                        "name": "Crop Name",
                        "scientific_name": "Scientific Name",
                        "msp": msp_price,
                        "water_need": "Low/Moderate/High",
                        "harvest_time": "X-Y days",
                        "risk": "Low/Moderate/High",
                        "expected_profit_per_acre": profit_amount,
                        "market_demand": "High/Moderate/Low",
                        "planting_time": "specific_time",
                        "fertilizer_requirement": "NPK ratio",
                        "pest_management": "key_tips"
                    }}
                }}
            ],
            "market_analysis": {{
                "trend": "market_trend",
                "price_forecast": "price_prediction",
                "demand_outlook": "demand_prediction"
            }},
            "additional_insights": [
                "insight1",
                "insight2",
                "insight3"
            ]
        }}

        Focus on practical, actionable advice that Indian farmers can implement immediately.
        """
        
        try:
            # Get AI response
            response = self.model.generate_content(prompt)
            
            # Parse the JSON response
            ai_recommendations = json.loads(response.text)
            
            return ai_recommendations
            
        except Exception as e:
            print(f"AI Error: {e}")
            # Fallback to mock data
            return self.get_fallback_recommendations(location, soil_type, irrigation)
    
    def analyze_plant_disease(self, image_path):
        """
        Analyze plant diseases using Gemini Vision API
        """
        try:
            # Use Gemini Vision for image analysis
            vision_model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Load and encode the image
            with open(image_path, 'rb') as img_file:
                image_data = img_file.read()
            
            prompt = """
            You are an expert plant pathologist. Analyze this plant image and provide:
            
            1. Disease identification (if any)
            2. Crop type identification
            3. Confidence level (0-100%)
            4. Severity assessment (Low/Moderate/High)
            5. Treatment recommendations:
               - Organic solutions
               - Chemical solutions (if necessary)
               - Preventive measures
            6. Additional care tips
            
            Format the response as JSON:
            {
                "disease": "disease_name",
                "crop": "crop_type",
                "confidence": confidence_percentage,
                "severity": "Low/Moderate/High",
                "solutions": {
                    "organic": "organic_treatment",
                    "chemical": "chemical_treatment",
                    "preventive": "preventive_measures"
                },
                "care_tips": "additional_care_instructions"
            }
            """
            
            response = vision_model.generate_content([prompt, image_data])
            return json.loads(response.text)
            
        except Exception as e:
            print(f"Vision AI Error: {e}")
            return self.get_fallback_disease_analysis()
    
    def get_irrigation_advice(self, crop, soil_type, weather, growth_stage):
        """
        Get AI-powered irrigation advice
        """
        prompt = f"""
        As an agricultural irrigation expert, provide detailed irrigation recommendations for:
        
        Crop: {crop}
        Soil Type: {soil_type}
        Weather: {weather}
        Growth Stage: {growth_stage}
        
        Provide recommendations for:
        1. Water requirement (liters per acre per day)
        2. Irrigation frequency
        3. Best time for irrigation
        4. Irrigation method recommendations
        5. Water conservation tips
        
        Return as JSON:
        {{
            "water_needed_liters": amount,
            "frequency": "frequency_description",
            "best_time": "optimal_time",
            "tips": "conservation_tips",
            "method": "recommended_method"
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except Exception as e:
            print(f"Irrigation AI Error: {e}")
            return self.get_fallback_irrigation_data()
    
    def get_fallback_recommendations(self, location, soil_type, irrigation):
        """Fallback recommendations when AI is unavailable"""
        return {
            "location": location,
            "analysis_date": datetime.now().strftime("%B %d, %Y"),
            "recommendations": [
                {
                    "crop": "soybean",
                    "confidence": 85,
                    "reason": "Suitable for current conditions based on historical data",
                    "data": {
                        "name": "Soybean",
                        "msp": 4800,
                        "water_need": "Moderate",
                        "harvest_time": "90-100 days",
                        "risk": "Moderate"
                    }
                }
            ]
        }
    
    def get_fallback_disease_analysis(self):
        """Fallback disease analysis when AI is unavailable"""
        return {
            "disease": "Unknown",
            "crop": "Unknown",
            "confidence": 0,
            "severity": "Unknown",
            "solutions": {
                "organic": "Consult local agricultural expert",
                "chemical": "Seek professional advice",
                "preventive": "Maintain field hygiene"
            }
        }
    
    def get_fallback_irrigation_data(self):
        """Fallback irrigation data when AI is unavailable"""
        return {
            "water_needed_liters": 25,
            "frequency": "Every 3-4 days",
            "best_time": "Early morning or evening",
            "tips": "Avoid watering during peak sunlight hours"
        }

# Example usage
if __name__ == "__main__":
    # Import config
    try:
        from config import get_api_key, is_ai_available
    except ImportError:
        print("❌ config.py not found. Please create it with your API key.")
        exit(1)
    
    # Check if AI is available
    if is_ai_available():
        api_key = get_api_key()
        ai = KisanMitraAI(api_key)
        
        print("🤖 Testing AI Integration...")
        
        # Test crop recommendation
        recommendation = ai.get_crop_recommendation(
            location="Nashik",
            soil_type="Black Soil",
            irrigation="Rain-fed",
            land_area=5,
            season="Kharif",
            budget=50000
        )
        
        print("✅ AI Crop Recommendation:")
        print(json.dumps(recommendation, indent=2))
    else:
        print("❌ AI not available. Please check your API key in config.py") 