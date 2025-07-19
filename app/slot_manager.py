# slot_manager.py

from .slotconfig import get_required_slots

def get_missing_slots(intent: str, filled_slots: dict) -> list:
    required = get_required_slots(intent)
    return [slot for slot in required if not filled_slots.get(slot)]
