import wave
import struct
import math
import random
import numpy as np

def generate_human_like_audio(duration=75, sample_rate=44100):
    """
    Generate a more natural-sounding audio waveform that simulates human speech patterns.
    Uses multiple frequencies and varying amplitudes.
    """
    num_samples = duration * sample_rate
    
    # Create audio data
    audio_data = []
    
    # Base frequencies common in human speech (in Hz)
    fundamental_freq = 150  # Average human fundamental frequency
    formant_freqs = [500, 1500, 2500]  # Common formant frequencies
    
    # Generate samples
    for i in range(num_samples):
        t = float(i) / sample_rate
        sample = 0
        
        # Add fundamental frequency with varying amplitude
        amplitude = 0.3 * (1 + 0.2 * math.sin(2 * math.pi * 2 * t))  # Amplitude modulation
        sample += amplitude * math.sin(2 * math.pi * fundamental_freq * t)
        
        # Add formants with different amplitudes
        for idx, freq in enumerate(formant_freqs):
            # Decrease amplitude for higher frequencies
            formant_amplitude = 0.2 / (idx + 1)
            # Add some random variation
            variation = 1 + 0.1 * random.random()
            sample += formant_amplitude * variation * math.sin(2 * math.pi * freq * t)
        
        # Add some noise for more natural sound
        sample += 0.05 * random.random()
        
        # Normalize to prevent clipping
        sample = max(min(sample, 1), -1)
        
        # Convert to 16-bit integer
        audio_data.append(int(sample * 32767))
    
    # Create WAV file
    with wave.open('sample-lecture.wav', 'w') as wav_file:
        # Set parameters
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        
        # Write audio data
        for sample in audio_data:
            wav_file.writeframes(struct.pack('h', sample))

if __name__ == '__main__':
    print("Generating audio file with human-like waveform patterns...")
    generate_human_like_audio()
    print("Audio file 'sample-lecture.wav' has been generated.")
