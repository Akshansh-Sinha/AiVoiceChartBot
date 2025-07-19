import pyaudio as pa
import wave as wv
from datetime import datetime
import io
import webrtcvad
import time
class AudioRecorder:      
    def __init__(self,chunk: int = 1024, rate: int = 16000, format: int = pa.paInt16, channel: int = 1):
        self.CHUNK = chunk
        self.RATE = rate
        self.FORMAT = format
        self.CHANNELS = channel
        self.FRAMES = []

    def record_audio(self, RECORD_SECONDS: int):    
        self.FRAMES = []
        audio = pa.PyAudio()
        
        stream = audio.open(
            channels=self.CHANNELS,
            input=True,
            rate=self.RATE,
            format=self.FORMAT,
            frames_per_buffer=self.CHUNK
            )

        print("Recording...")
 
        for _ in range(0,int(self.RATE/self.CHUNK * RECORD_SECONDS+1)):
            data = stream.read(self.CHUNK)
            self.FRAMES.append(data)
            
        print("Recorded")

        stream.stop_stream()
        stream.close()
        audio.terminate()

    def record_audio_to_memory(self, RECORD_SECONDS: int):    
        self.FRAMES = []
        audio = pa.PyAudio()
        
        stream = audio.open(
            channels=self.CHANNELS,
            input=True,
            rate=self.RATE,
            format=self.FORMAT,
            frames_per_buffer=self.CHUNK
            )

        print("Recording...")
 
        for _ in range(0,int(self.RATE/self.CHUNK * RECORD_SECONDS+1)):
            data = stream.read(self.CHUNK)
            self.FRAMES.append(data)
            
        print("Recorded")

        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        audio_data = b''.join(self.FRAMES)
        print("Done recording")
        return io.BytesIO(audio_data)

    def save_audio(self, OUTPUT_FILENAME: str = None) -> str:
        if OUTPUT_FILENAME:
            filename = f"{OUTPUT_FILENAME}.wav"
        else:
            timestamp = datetime.now().strftime("D_%d-%m-%Y_T_%H-%M-%S")
            filename = f"{timestamp}.wav"
        
        path = f"audio/recordings/{filename}"
                 
        wav = wv.open(path,"wb")
        wav.setnchannels(self.CHANNELS)
        audio = pa.PyAudio()
        sampwidth = audio.get_sample_size(self.FORMAT)
        audio.terminate()
        wav.setsampwidth(sampwidth)
        wav.setframerate(self.RATE)
        wav.writeframes(b''.join(self.FRAMES))
        wav.close()

        print(f"Saved to {filename}")
        
        return filename
    
class AutoAudioRecorder():
    def __init__(self,aggrissiveness: int, rate: int = 16000, format: int = pa.paInt16, channel: int = 1):
        self.CHUNK = int(rate * 30/1000)
        self.RATE = rate
        self.FORMAT = format
        self.CHANNELS = channel
        self.webrtcvad = webrtcvad.Vad(aggrissiveness)
        self.FRAMES = []
        
    def record_audio(self,max_silence_sec: int = 5):
        audio = pa.PyAudio()
        stream = audio.open(
            channels=self.CHANNELS,
            input=True,
            rate=self.RATE,
            format=self.FORMAT,
            frames_per_buffer=self.CHUNK
            )
        print("Recording...")
        self.FRAMES = []
        silence_start = None
        while True:
            frame = stream.read(self.CHUNK)
            is_speech = self.webrtcvad.is_speech(frame, self.RATE)
            self.FRAMES.append(frame)

            if not is_speech:
                if silence_start is None:
                    silence_start = time.time()
                elif time.time() - silence_start > max_silence_sec:
                    print("🛑 Detected silence. Stopping recording.")
                    break
            else:
                silence_start = None  # reset silence timer on speech

        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        audio_data = b''.join(self.FRAMES)
        print("Done recording")
        return self._get_wav_bytesio(audio_data)
    
    def _get_wav_bytesio(self, raw_audio_bytes: bytes) -> io.BytesIO:
        wav_buffer = io.BytesIO()
        with wv.open(wav_buffer, 'wb') as wav_file:
            wav_file.setnchannels(self.CHANNELS)
            wav_file.setsampwidth(pa.PyAudio().get_sample_size(self.FORMAT))
            wav_file.setframerate(self.RATE)
            wav_file.writeframes(raw_audio_bytes)
        wav_buffer.seek(0)
        return wav_buffer