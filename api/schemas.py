from fastapi import FastAPI
from datetime import date,time
from typing import Optional, Literal
from pydantic import BaseModel

class RawQuery(BaseModel):
    intent: Literal["book_appointment", "cancel_appointment", "inquire_availability"]
    hospital: Optional[str] = None
    department: Optional[str] = None
    doctor: Optional[str] = None
    day: Optional[str] = None
    appointment_date: Optional[str] = None
    appointment_time: Optional[str] = None
    patient_name: Optional[str] = None   
    self_diagnosis: Optional[str] = None
                                    
class RefinedQuery(BaseModel):
    intent: Literal["book_appointment", "cancel_appointment", "inquire_availability"]
    hospital: Optional[str] = None
    department: Optional[str] = None
    doctor: Optional[str] = None
    appointment_date: Optional[date] = None
    appointment_time: Optional[time] = None
    patient_name: Optional[str] = None   
    self_diagnosis: Optional[str] = None
    
class BotReply(BaseModel):
    reply: str
    status: Literal["success", "failure"]
    intent: Literal["book_appointment", "cancel_appointment", "inquire_availability"]
    missing_fields: Optional[dict] = None 