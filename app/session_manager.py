session_data = {}

def create_session(session_id: str):
    if session_id not in session_data:
        session_data[session_id] = {
            "intent": None ,
            "slots": {}
        }

def get_intent(session_id: str):
    return session_data.get(session_id,{}).get("intent")

def set_intent(session_id: str, intent: str):
    create_session(session_id)  
    session_data[session_id]["intent"] = intent

def get_slot(session_id: str,key: str):
    return session_data.get(session_id,{}).get("slots",{}).get(key)

def set_slot(session_id: str, slots: dict):
    create_session(session_id)
    for key,value in slots.items():
        if value is not None:
            session_data[session_id]["slots"][key] = value

def get_filled_slots(session_id: str):
    if session_id not in session_data:
        raise ValueError(f"Session '{session_id}' not found.")
    return session_data[session_id].get("slots", {})

def reset_session(session_id: str):
    session_data.pop(session_id, None)

