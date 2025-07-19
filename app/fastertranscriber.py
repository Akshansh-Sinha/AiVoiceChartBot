from faster_whisper import WhisperModel
import io
class FasterWhisperTranscriber:  
    def __init__(self, MODEL: str = "medium", AUDIO_FILE: str = None):
        self.model = WhisperModel(
            MODEL,
            device="cuda",
            compute_type="float16"
        )
        self.audio_file = AUDIO_FILE
        
    def transcribe(self) -> str:
        path = f"audio/recordings/{self.audio_file}"
        segments,_ = self.model.transcribe(path)
        full_text = " ".join([segment.text for segment in segments])
        print("Transcription Complete")
        return full_text
    
    def transcribe_audio_from_memory(self,audio_buffer: io.BytesIO) -> str:
        segments,_ = self.model.transcribe(audio_buffer)
        full_text = " ".join([segment.text for segment in segments])
        print("Transcription Complete")
        return full_text
    
    def get_transcript_name(self) -> str:
        return self.audio_file.rsplit(".",1)[0]
    def save_transcript(self,full_text: str):
        path = f"audio/transcripts/{self.get_transcript_name()}.txt"
        with open(path, "w", encoding="utf-8") as f:
            f.write(full_text)
        