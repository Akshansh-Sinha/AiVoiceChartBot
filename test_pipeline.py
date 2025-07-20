from app.record import AudioRecorder, AutoAudioRecorder
from app.fastertranscriber import FasterWhisperTranscriber
from app.intent_extractor import IntentExtractor
from app.resolve_raw_query import ResolveRawQuery
from app.session_manager import reset_session, create_session, set_intent, get_intent, get_filled_slots, get_slot, set_slot
from app.slot_manager import get_missing_slots
import random 
import string
from app.generate_reply import Generate_missing,Generate_final_reply
from app.tts import speak
from pydantic import ValidationError
# if __name__ == "__main__":
#     recorder = AudioRecorder()

#     duration = int(input("Enter recording duration in seconds: "))
#     recorder.record_audio(duration)

#     name = input("Enter file name (or press Enter to auto-generate): ").strip()
#     if name == "":
#         filename = recorder.save_audio()
#     else:
#         filename = recorder.save_audio(name)
    
#     Transcriber = FasterWhisperTranscriber(AUDIO_FILE=filename)
#     result = Transcriber.transcribe()
#     rawquery = IntentExtractor(result).extract_intent()
#     refined_query = ResolveRawQuery(rawquery).resolve()
    
#     session_id = "test123"
#     reset_session(session_id)  
#     set_intent(session_id, refined_query.intent)
#     slot_data = refined_query.model_dump(exclude={"intent"}, exclude_none=True)
#     set_slot(session_id, slot_data)
    
#     print(f"Slots stored in session: {get_filled_slots(session_id)}")
#     missing = get_missing_slots(refined_query.intent,get_filled_slots(session_id))
#     print(f"🧩 Missing slots: {missing}")
   
session_id = ''.join(random.choice(string.ascii_letters) for _ in range(5))
print(session_id)
create_session(session_id)
start = "Hi, how can i assist you today?"
print("Hi, how can i assist you today?")
speak(start)
a = True
while(a):
    audio_file = AutoAudioRecorder(3).record_audio(max_silence_sec=5)
    transcription = FasterWhisperTranscriber().transcribe_audio_from_memory(audio_file)
    raw_json = IntentExtractor(transcription).extract_intent()
    
    try:
        refined_query = ResolveRawQuery(raw_json, session_id).resolve()
    except ValidationError as e:
        print("⚠️ Invalid intent or data:", raw_json)
        speak("Sorry, I did not understand that. Please try again.")
        continue
    set_intent(session_id, refined_query.intent)
    slot_data = refined_query.model_dump(exclude={"intent"}, exclude_none=True)
    set_slot(session_id, slot_data)
    print(f"Slots stored in session: {get_filled_slots(session_id)}")
    missing = get_missing_slots(refined_query.intent,get_filled_slots(session_id))
    print(f"🧩 Missing slots: {missing}")
    if missing:
        reply = Generate_missing(missing,refined_query.intent)
        print(reply)
    else:
        reply = Generate_final_reply(refined_query.intent)
        print(reply)
        a = False
       
reset_session(session_id)