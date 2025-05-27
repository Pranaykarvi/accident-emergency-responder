# File: test_webcam_save.py

from src.detection.accident_detector import AccidentDetector

if __name__ == "__main__":
    detector = AccidentDetector()

    print("Starting webcam capture and saving annotated video to 'outputs/webcam_output.mp4' ...")
    output_path = detector.detect_on_webcam(
        camera_index=0,
        conf=0.25,
        save_dir="outputs",
        output_filename="webcam_output.mp4",
        max_frames=300  # adjust as needed
    )
    print(f"Webcam inference saved to: {output_path}")
