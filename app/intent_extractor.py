from dotenv import load_dotenv
from google import genai
from google.genai import types
from api.schemas import RawQuery
import json
import re
import os

class IntentExtractor:
    def __init__(self, text: str):
        # with open(f"audio/transcripts/{filename}.txt", "r", encoding="utf-8") as file:
        #     self.text = file.read()
        self.text = text
    @staticmethod   
    def extract_json_from_markdown(text: str) -> str:
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if match:
            return match.group(1)
        return text.strip()     
    def extract_intent(self)-> RawQuery:
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction='''
                                    You are an intent and entity extraction assistant designed to help a hospital appointment booking voice bot. 
                                    The bot receives transcribed user speech (in Hindi-English mix), and your job is to extract useful structured data.

                                    Use the transcription provided below to fill in the required fields. Return only a valid JSON object with keys exactly as shown, and `null` if data is missing.Return ONLY the JSON object. Do not explain, greet, or add any extra text before or after the JSON.

                                    ---

                                    🎯 Your goal: 
                                    From the given transcription, extract:

                                    {
                                    "intent": "book_appointment / cancel_appointment / inquire_availability / get_doctor_info / greet / other",
                                    "hospital": "Name of the hospital if mentioned, else null",
                                    "department": "Relevant department (e.g., cardiology, neurology), else null",
                                    "doctor": "Full name of doctor if mentioned, else null",
                                    "appointment_date": 'tomorrow','yesterday','today','kal(HINDI WORD) it means tomorrow if sentence is in future tense and yesterday if sentence is in past tense','parso in hindi meaning day before yesterday','tarso means 3 days ago from today', 'next Friday' or any specific date",
                                    "appointment_time": "Appointment time or time window if mentioned (e.g., 3 PM, morning, afternoon,evening,shaam,subah,dupahar), else null",
                                    "patient_name": "Name of the patient, if user says 'mera naam Ravi hai' Only Proper Noun is allowed, else null",
                                    "self_diagnosis": "What problem user is facing or what they mention they need help with (e.g., fever, chest pain), else null"
                                    }

                                    ---

                                    🧠 Instructions:
                                    - Keep values in **plain text** or `null` (not "none", not "missing", not empty string).
                                    - Do **not add extra keys** outside the ones listed above.
                                    - If the transcription contains unrelated chit-chat, still return the JSON, but with `"intent": "other"` and all other values as null.
                                    ---
                                    '''),
            contents=self.text
        )
        print("📤 Gemini raw output:\n", response.text)
        try:
            clean_json = IntentExtractor.extract_json_from_markdown(response.text)
            parsed_result = json.loads(clean_json)
            return RawQuery(**parsed_result)
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            print("⚠️ Gemini returned invalid JSON:", e)
            # Return fallback RawQuery with intent="other"
            return RawQuery(
                intent="Not_detected",
                hospital=None,
                department=None,
                doctor=None,
                appointment_date=None,
                appointment_time=None,
                patient_name=None,
                self_diagnosis=None
            )
        
