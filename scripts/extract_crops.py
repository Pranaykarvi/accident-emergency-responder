# File: scripts/extract_crops.py

import os
import sys
import cv2

# ─────────────────────────────────────────────────────────────────────────────
# Add the project root to sys.path so that "import src.detection.accident_detector"
# works when running this script.
# ─────────────────────────────────────────────────────────────────────────────
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.detection.accident_detector import AccidentDetector

def extract_and_save_crops(
    image_dir="datasets/labeled/test/images",
    output_dir="severity_data/raw_crops",
    conf=0.25
):
    """
    Runs YOLO accident detection on every image in image_dir,
    crops each detected box, and saves crops under output_dir/<image_basename>_<i>.jpg
    """

    os.makedirs(output_dir, exist_ok=True)
    detector = AccidentDetector()

    # Loop through each image in the test set
    for img_name in os.listdir(image_dir):
        if not img_name.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        img_path = os.path.join(image_dir, img_name)
        # Run detection (do not save annotated image, just get boxes)
        result = detector.detect_on_image(image_path=img_path, conf=conf, save=False)

        # result.boxes.xyxy is an (N,4) array of [x1, y1, x2, y2]
        coords = result.boxes.xyxy.cpu().numpy()
        # result.boxes.conf is an (N,) array of confidences
        confidences = result.boxes.conf.cpu().numpy()
        # result.boxes.cls is an (N,) array of class IDs (we only have a single class "accident")
        classes = result.boxes.cls.cpu().numpy()

        # Load original image as a NumPy array (BGR)
        image = cv2.imread(img_path)
        if image is None:
            continue

        # For each detected box, crop and save
        for i in range(coords.shape[0]):
            x1, y1, x2, y2 = map(int, coords[i])
            crop = image[y1:y2, x1:x2]
            if crop.size == 0:
                continue

            base = os.path.splitext(img_name)[0]
            out_name = f"{base}_{i}.jpg"
            out_path = os.path.join(output_dir, out_name)
            cv2.imwrite(out_path, crop)

            print(f"Saved crop: {out_path}")

if __name__ == "__main__":
    extract_and_save_crops()
