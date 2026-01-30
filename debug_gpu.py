
from utils.gpu_detector import GPUDetector
import sys
import os
from pathlib import Path

# Override ffmpeg path to test specifically
app_dir = Path(os.getcwd())
ffmpeg_path = str(app_dir / "ffmpeg" / "ffmpeg.exe")

print(f"Testing GPU Detector with FFmpeg: {ffmpeg_path}")

detector = GPUDetector(ffmpeg_path)

print("\n--- GPU Info ---")
gpu = detector.detect_gpu()
print(f"Detected: {gpu}")

print("\n--- Available Encoders ---")
encoders = detector.get_available_encoders()
print(f"Raw encoders: {encoders}")

print("\n--- Recommendation ---")
rec = detector.get_recommended_encoder()
print(f"Recommendation: {rec}")

print("\n--- AMF Check ---")
if 'h264_amf' in encoders:
    print("h264_amf IS available in the list.")
else:
    print("h264_amf IS NOT available in the list.")
