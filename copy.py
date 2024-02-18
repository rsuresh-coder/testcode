import sounddevice as sd
import soundfile as sf
import os 

def record_audio(duration, filename, samplerate=44100):
    # Record audio for the given duration in seconds
    print("Recording...")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1 )
    sd.wait()  # Wait until recording is finished
    print("Recording finished")

    # Save the recorded audio to a WAV file
    sf.write(filename, audio_data, samplerate)
    print(f"File saved as {filename}")

# Example usage: Record 5 seconds of audio and save it as "output.wav"

for i in range(5):
    print(i, sd.query_devices(i)['default_samplerate'])


os.remove('/Users/sureshreddy/Downloads/recordgpt.wav')
sd.default.device[0] = 5
record_audio(1, '/Users/sureshreddy/Downloads/recordgpt.wav')
