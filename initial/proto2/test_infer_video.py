# File: test_video_infer.py
from src.detection.accident_detector import AccidentDetector

if __name__ == "__main__":
    detector = AccidentDetector()

    # Replace with the path to a video that contains an accident
    video_path = "datasets/labeled/test/videos/sample_accident.mp4"

    # Run detection on the entire video, show live frames, and save the annotated output
    detector.detect_on_video(
        video_path=video_path,
        conf=0.25,      # confidence threshold
        show=True,      # set True to pop up a window
        save=True,      # writes annotated video to "outputs/"
        save_dir="outputs"
    )
    print("Video inference complete. Check outputs/ for the annotated video.")
