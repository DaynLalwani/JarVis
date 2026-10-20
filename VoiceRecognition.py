"""

FLOW 

START RECORDING ----> STOP RECORDING ----> Convert Audio to text (SpeechToText) ----> Set outut as command 


SPEECH Recognition platform ---> faster-whisper
"""

import faster_whisper
import sounddevice
import scipy.io.wavfile
from tkinter import messagebox

def recognise():
    #tiny --> base -->small --> medium --> Large-v3
    model_size = "medium"
    SAMPLE_RATE = 44100
    DURATION = 5
    filename = "Output.wav"
    messagebox.showinfo("STT INFO","Recording Started , Speak for the next 10 Seconds")
    recording = sounddevice.rec(int(DURATION*SAMPLE_RATE),samplerate=SAMPLE_RATE,channels=1)
    sounddevice.wait()
    messagebox.showinfo("STT INFO","Recording over , Starting Speech Recognition")
    scipy.io.wavfile.write(filename,SAMPLE_RATE,recording)

    model = faster_whisper.WhisperModel(model_size,device="cpu",compute_type="int8")
    segments,info = model.transcribe(filename,beam_size=5)
    output = ""
    for segment in segments:
        output += segment.text
    print(output)
    return output
    



