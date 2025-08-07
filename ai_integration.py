import google.generativeai as genai
import json
import re
from PIL import Image

class KisanMitraAI:
    def __init__(self, api_key):
        """Initializes the AI system with the provided API key."""
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
            print("✅ Gemini AI Model Initialized Successfully.")
        except Exception as e:
            print(f"❌ Failed to configure Gemini AI: {e}")
            self.model = None

    def _get_ai_response(self, prompt, generation_config):
        """Helper function to get and parse response from the AI model."""
        if not self.model:
            raise ConnectionError("Gemini AI Model is not initialized.")

        try:
            response = self.model.generate_content(prompt, generation_config=generation_config)
            cleaned_text = re.sub(r'```json\s*|\s*```', '', response.text, flags=re.DOTALL)
            return json.loads(cleaned_text)
        
        except json.JSONDecodeError:
            print(f"⚠️ AI returned a non-JSON response. Raw text: {response.text}")
            raise ValueError("AI did not return a valid JSON format.")
        except Exception as e:
            print(f"❌ An unexpected error occurred during AI call: {e}")
            raise

    def get_crop_recommendation(self, location, soil_type, irrigation, land_area, season, budget, generation_config):
        """Generates a detailed crop recommendation using the Gemini API."""
        prompt = f"""
        As an expert agricultural advisor for Maharashtra, India, provide crop recommendations.
        Your response MUST be a valid JSON object. Do not include any text before or after the JSON.
        
        Farmer's Input:
        - Location: {location}, Maharashtra
        - Soil Type: {soil_type}
        - Irrigation: {irrigation}
        - Land Area: {land_area} acres
        - Season: {season}
        - Budget: INR {budget}

        Provide the top 2-3 crop recommendations in this exact JSON format:
        {{
            "location": "{location}",
            "recommendations": [
                {{"crop": "crop_name_1", "confidence": 92, "reason": "your_reasoning_here", "data": {{ "name": "Crop Name 1", "msp": 5000, "water_need": "Moderate", "harvest_time": "90-100 days", "risk": "Low" }}}},
                {{"crop": "crop_name_2", "confidence": 85, "reason": "your_reasoning_here", "data": {{ "name": "Crop Name 2", "msp": 7000, "water_need": "High", "harvest_time": "150-180 days", "risk": "Medium" }}}}
            ],
            "market_data": {{"crop_name_1": 5200, "crop_name_2": 7100}}, "ai_used": true
        }}
        """
        return self._get_ai_response(prompt, generation_config)

    def analyze_plant_disease(self, image_path, generation_config):
        """Analyzes a plant image for diseases using the Gemini Vision model."""
        if not self.model:
            raise ConnectionError("Gemini AI Model is not initialized.")
        try:
            image = Image.open(image_path)
            prompt = """
            As an expert plant pathologist, analyze the attached image of a plant leaf.
            Your response MUST be a valid JSON object. Do not include any text before or after the JSON.
            
            Provide the following in this exact JSON format:
            {
                "disease": "Disease Name", "crop": "Crop Name", "confidence": 95, "severity": "Moderate",
                "solutions": {
                    "organic": "A brief, clear organic solution.",
                    "chemical": "A brief, clear chemical solution.",
                    "preventive": "A brief, clear preventive measure."
                }, "ai_used": true
            }
            """
            response = self.model.generate_content([prompt, image], generation_config=generation_config)
            cleaned_text = re.sub(r'```json\s*|\s*```', '', response.text, flags=re.DOTALL)
            return json.loads(cleaned_text)
        except Exception as e:
            print(f"❌ An unexpected error occurred during AI image analysis: {e}")
            raise
            
    def get_irrigation_advice(self, crop, soil_type, land_area, weather, growth_stage, generation_config):
        """Generates irrigation advice using the Gemini API."""
        prompt = f"""
        As an agricultural irrigation expert for Maharashtra, India, provide a detailed irrigation plan.
        Your response MUST be a valid JSON object without any markdown formatting.
        
        Inputs:
        - Crop: {crop}
        - Soil Type: {soil_type}
        - Land Area: {land_area} acres
        - Current Weather: {weather}
        - Growth Stage: {growth_stage}

        Return recommendations in this exact JSON format:
        {{
          "water_needed_liters_per_acre": 15000,
          "frequency": "Every 2-3 days",
          "best_time": "Early morning (5 AM - 8 AM)",
          "method_feedback": "Drip irrigation is highly recommended for {crop} to ensure water efficiency.",
          "optimization_tips": "Use mulch to reduce soil moisture evaporation. Check soil moisture before watering.",
          "ai_used": true
        }}
        """
        return self._get_ai_response(prompt, generation_config)

    def get_fertilizer_advice(self, crop, soil_type, growth_stage, generation_config):
        """Generates fertilizer recommendations using the Gemini API."""
        prompt = f"""
        As an agronomist specializing in Indian agriculture, provide a fertilizer plan.
        Your response MUST be a valid JSON object without any markdown formatting.

        Inputs:
        - Crop: {crop}
        - Soil Type: {soil_type}
        - Growth Stage: {growth_stage}

        Return a plan in this exact JSON format:
        {{
            "quantity_per_acre": {{
                "nitrogen": "20 kg",
                "phosphorus": "40 kg",
                "potassium": "20 kg"
            }},
            "application_timing": "Apply as a basal dose during sowing.",
            "application_method": "Mix with the top 5-10 cm of soil before planting.",
            "organic_alternatives": "Well-decomposed farmyard manure (FYM) at 10 tons/acre.",
            "ai_used": true
        }}
        """
        return self._get_ai_response(prompt, generation_config)

    def get_soil_health_analysis(self, soil_type, ph, organic_matter, nitrogen, phosphorus, potassium, generation_config):
        """Generates a soil health analysis using the Gemini API."""
        prompt = f"""
        As a soil scientist, analyze soil health data from a farm in Maharashtra, India.
        Your response MUST be a valid JSON object without any markdown formatting.

        Inputs:
        - Soil Type: {soil_type}
        - pH Level: {ph}
        - Organic Matter (%): {organic_matter}
        - Nitrogen (N) (kg/ha): {nitrogen}
        - Phosphorus (P) (kg/ha): {phosphorus}
        - Potassium (K) (kg/ha): {potassium}

        Provide a comprehensive analysis in this exact JSON format:
        {{
            "soil_health_score": "8.2/10",
            "health_status": "Good",
            "ph_analysis": {{
                "current_status": "Near Neutral",
                "recommendation": "Maintain current pH. No immediate action required."
            }},
            "nutrient_analysis": {{
                "nitrogen_status": "Adequate",
                "phosphorus_status": "Slightly Deficient",
                "potassium_status": "Good"
            }},
            "suitable_crops": ["Sugarcane", "Cotton", "Soybean"],
            "soil_amendments": ["Add vermicompost to improve phosphorus levels.", "Continue crop rotation."],
            "long_term_plan": "Implement crop rotation with leguminous crops to naturally fix nitrogen.",
            "ai_used": true
        }}
        """
        return self._get_ai_response(prompt, generation_config)

    def get_agricultural_news(self, generation_config):
        """Generates the latest agricultural news using the Gemini API."""
        prompt = """
        As an agricultural journalist for India, provide the 3 latest and most relevant news headlines for farmers in Maharashtra.
        Your response MUST be a valid JSON object without any markdown formatting.

        Return the output in this exact JSON format:
        {
          "articles": [
            {
              "headline": "A recent and relevant news headline",
              "summary": "A brief one-sentence summary of the news.",
              "category": "Market",
              "source": "AI Generated",
              "date": "2025-08-07"
            }
          ]
        }
        """
        return self._get_ai_response(prompt, generation_config)

    def get_government_schemes(self, generation_config):
        """Gets details on relevant government schemes for farmers using the Gemini API."""
        prompt = """
        As a government policy expert for Indian agriculture, list 3 key central or Maharashtra state government schemes currently active for farmers.
        Your response MUST be a valid JSON object without any markdown formatting.

        For each scheme, provide a name, a brief objective, and the main benefit.
        Return the output in this exact JSON format:
        {
          "schemes": [
            {
              "name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
              "objective": "To provide insurance coverage and financial support to farmers in the event of failure of any of the notified crops as a result of natural calamities, pests & diseases.",
              "benefit": "Financial stability against crop loss."
            }
          ]
        }
        """
        return self._get_ai_response(prompt, generation_config)

    def get_weather_analysis(self, location, generation_config):
        """Gets a weather analysis for a given location using the Gemini API."""
        prompt = f"""
        As a meteorologist, provide a weather analysis for {location}, Maharashtra, India.
        Your response MUST be a valid JSON object without any markdown formatting.
        
        Provide the current weather and a 3-day forecast with an agricultural impact summary.
        Return the output in this exact JSON format:
        {{
          "location": "{location}",
          "current": {{
            "condition": "Partly Cloudy",
            "temperature_celsius": 28,
            "humidity_percent": 75,
            "wind_kph": 15
          }},
          "forecast": [
            {{"day": "Today", "condition": "Light rain possible", "max_temp_celsius": 30}},
            {{"day": "Tomorrow", "condition": "Cloudy with sunny spells", "max_temp_celsius": 31}},
            {{"day": "Day After", "condition": "Sunny", "max_temp_celsius": 32}}
          ],
          "agricultural_impact": "Favorable conditions for Kharif crops. Monitor for light showers, which may reduce the need for immediate irrigation."
        }}
        """
        return self._get_ai_response(prompt, generation_config)