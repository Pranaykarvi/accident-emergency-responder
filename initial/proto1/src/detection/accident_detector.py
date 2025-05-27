from ultralytics import YOLO
import cv2
import os

class AccidentDetector:
    def __init__(self, model_path=None):
        """
        Initializes the detector with a YOLOv8 checkpoint.
        If no path is given, it defaults to your trained best.pt.
        """
        if model_path is None:
            # NOTE: Make sure this path matches where your best.pt actually lives.
            model_path = r"D:\target\AI-AGENTS\accident_detection_ai\experiments\experiments\runs\accident_yolov8n2\weights\best.pt"
        self.model = YOLO(model_path)

    def detect_on_image(self, image_path, conf=0.3, save=False, save_dir="outputs"):
        """
        Runs detection on a single image file and returns the Results[0] object.
        If save=True, writes annotated image (+ .txt) into save_dir.
        """
        results = self.model.predict(
            source=image_path,
            conf=conf,
            save=save,
            save_txt=save,
            save_dir=save_dir
        )
        return results[0]

    def detect_on_video(self, video_path, conf=0.3, show=True, save=False, save_dir="outputs"):
        """
        Runs detection on every frame of a video file.
        If show=True, Ultralytics opens its own display window.
        If save=True, an annotated video is written to save_dir (prefixed "pred_").
        """
        return self.model.predict(
            source=video_path,
            conf=conf,
            show=show,
            save=save,
            save_txt=save,
            save_dir=save_dir
        )

    def detect_on_webcam(
        self,
        camera_index=0,
        conf=0.3,
        save_dir="outputs",
        output_filename="webcam_output.mp4",
        max_frames=300
    ):
        """
        Captures frames from the webcam (camera_index), runs YOLO on each frame,
        draws boxes, and writes an annotated video file (output_filename) into save_dir.
        Processes up to max_frames frames, then stops and returns the output path.
        """
        # Ensure output directory exists
        os.makedirs(save_dir, exist_ok=True)

        # Open the webcam
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            raise RuntimeError(f"Cannot open webcam index {camera_index}")

        # Read one frame to get width/height
        ret, frame = cap.read()
        if not ret:
            cap.release()
            raise RuntimeError("Unable to read from webcam.")

        height, width = frame.shape[:2]

        # Prepare VideoWriter to save annotated frames
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        output_path = os.path.join(save_dir, output_filename)
        writer = cv2.VideoWriter(output_path, fourcc, 20.0, (width, height))

        frame_count = 0
        while frame_count < max_frames:
            ret, frame = cap.read()
            if not ret:
                break

            # Run YOLO on this frame (single‐frame inference)
            results = self.model.predict(source=frame, conf=conf, save=False)

            # Draw the boxes on the frame
            annotated = results[0].plot()

            # Write the annotated frame to the output video
            writer.write(annotated)

            frame_count += 1

        # Release resources
        cap.release()
        writer.release()
        return output_path
