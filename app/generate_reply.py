from api.schemas import RefinedQuery

final_reply = {
    "book_appointment": "Your appointment has been successfully booked. Please remember to show up at the hospital on time. We look forward to seeing you. Have a nice day! ",
    "cancel_appointment": "Your appointment has been successfully cancelled. We hope to see you again soon. Have a nice day! ",
    "inquire_availability": "We are sorry, but there are no available appointments for the specified date. Please choose a different date. Have a nice day! "
}
missing_slots_followup = {
    "book_appointment":{
        "patient_name": "What is your name?",
        "hospital": "Which hospital would you like to book an appointment at?",
        "doctor": "Which doctor would you like to book an appointment with?", 
        "appointment_date": "What date would you like to book an appointment on?", 
        "appointment_time": "What time would you like to book an appointment at?"
    },
    "cancel_appointment":{
        "booking_id": "What is your booking ID?",
        "patient_name": "What is your name?"
    },
    "reschedule_appointment":{
        "booking_id": "What is your booking ID?",
        "new_date": "What date would you like to reschedule your appointment to?",
        "new_time": "What time would you like to reschedule your appointment to?"
    }
}
def Generate_missing(missing: list, intent: str):

    if intent == "book_appointment":
            return missing_slots_followup[intent][missing[0]]
    elif intent == "cancel_appointment":
            return missing_slots_followup[intent][missing[0]]
    elif intent == "inquire_availability":
            return missing_slots_followup[intent][missing[0]]
           
def Generate_final_reply(intent: str):
    return final_reply[intent]   
    