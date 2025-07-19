# slot_config.py

required_slots = {
    "book_appointment": ["hospital", "doctor", "appointment_date", "appointment_time", "patient_name"],
    "cancel_appointment": ["booking_id", "patient_name"],
    "reschedule_appointment": ["booking_id", "new_date", "new_time"],
    # Add more intents as needed
}

def get_required_slots(intent: str):
    return required_slots.get(intent, [])
