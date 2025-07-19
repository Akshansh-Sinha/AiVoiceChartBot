from api.schemas import RawQuery, RefinedQuery
from datetime import date,timedelta
import dateparser
from app.session_manager import set_intent,get_intent
class ResolveRawQuery:
    def __init__(self,raw_query: RawQuery, sessionId: str):
        self.raw_query = raw_query
        self.session_id = sessionId
        
    @staticmethod    
    def clean_time_expression(raw_time: str) -> str:
        if not raw_time:
            return None
        
        mapping = {
            "सुबह": "morning",
            "शाम": "evening",
            "दोपहर": "afternoon",
            "रात": "night",
            "बजे": "o'clock",
            "10 बजे": "10 o'clock",
        }
        for hin, eng in mapping.items():
            raw_time = raw_time.replace(hin, eng)
        return raw_time

    def resolve(self)-> RefinedQuery:
        #date resolution
        
        parsed_raw_date = None
        if self.raw_query.appointment_date:
            parsed_raw_date = dateparser.parse(self.raw_query.appointment_date)

        resolved_date = parsed_raw_date.date() if parsed_raw_date else None
        resolved_day = parsed_raw_date.strftime("%A") if parsed_raw_date else None
        
        #time resolution
        raw_time = self.raw_query.appointment_time
        cleaned_time = ResolveRawQuery.clean_time_expression(raw_time)
        parsed_raw_time = None
        if cleaned_time:
            parsed_raw_time = dateparser.parse(cleaned_time)

        resolved_time = parsed_raw_time.time() if parsed_raw_time else None
        
        # Step 3: Intent resolution logic
        detected_intent = self.raw_query.intent
        previous_intent = get_intent(self.session_id)

        # If Gemini returns 'other' or irrelevant intent, stick with previous
        if previous_intent in ["book_appointment", "cancel_appointment", "inquire_availability"]:
            if detected_intent not in ["book_appointment", "cancel_appointment", "inquire_availability"]:
                detected_intent = previous_intent
            else:
                set_intent(self.session_id, detected_intent)  # Update session if valid new intent
        else:
            # If no previous intent and current is valid, store it
            if detected_intent in ["book_appointment", "cancel_appointment", "inquire_availability"]:
               set_intent(self.session_id, detected_intent)
                
        return RefinedQuery(
            intent = detected_intent,
            hospital = self.raw_query.hospital,
            department = self.raw_query.department,
            doctor = self.raw_query.doctor,
            day = resolved_day,
            appointment_date = resolved_date,
            appointment_time = resolved_time,
            patient_name = self.raw_query.patient_name,
            self_diagnosis = self.raw_query.self_diagnosis
        )