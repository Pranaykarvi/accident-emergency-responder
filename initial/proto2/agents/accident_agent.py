import os
from src.detection.accident_detector import AccidentDetector
from agents.location_agent import LocationAgent
from agents.resource_allocator import ResourceAllocator
from agents.notifier_agent import NotifierAgent
from agents.messenger_agent import NotifierAgent  # ✅ NEW

class AccidentAgent:
    def __init__(self):
        self.detector = AccidentDetector()
        self.loc_agent = LocationAgent()
        self.allocator = ResourceAllocator()
        self.notifier = NotifierAgent()

        # Ensure outputs/ directory exists for annotated images/videos
        os.makedirs("outputs", exist_ok=True)

    def handle_image(self, image_path, camera_id=None, notify_email=None):
        """
        1. Run YOLO detection on image_path and save annotated image to outputs/.
        2. If any box is found, look up location, allocate resources, send email.
        Returns a summary string AND a structured resources dict.
        """
        # 1. Detect accidents and save annotated image
        result = self.detector.detect_on_image(
            image_path=image_path,
            conf=0.25,
            save=True,
            save_dir="outputs"
        )
        num_boxes = len(result.boxes)
        if num_boxes == 0:
            return "No accidents detected.", {}

        # 2. Lookup location
        loc = self.loc_agent.get_location(camera_id)
        lat, lon = loc["lat"], loc["lon"]
        address = loc.get("address", "Unknown Location")

        # 3. Allocate resources
        allocated = self.allocator.allocate(incident_loc={"lat": lat, "lon": lon})

        # 4. Send WhatsApp Notification
        subj = f"Accident Alert at {address}"
        body = (
            f"Accident detected at {address} (lat: {lat}, lon: {lon}).\n"
            f"Number of incidents: {num_boxes}\n"
            f"Allocated: {', '.join([r['id'] for r in allocated])}"
        )
        annotated_img = os.path.join("outputs", os.path.basename(image_path))
        if notify_email:
            self.notifier.send_whatsapp(
                to_number=notify_email,
                message=f"{subj}\n\n{body}"
            )
        else:
            print("[Notification Skipped – no email provided]")
            print("SUBJECT:", subj)
            print("BODY:", body)

        # Structured resources dictionary by type
        resources_dict = {}
        for r in allocated:
            resources_dict.setdefault(r["type"], []).append(r["id"])

        summary = (
            f"Detected {num_boxes} accident(s) at {address} (lat={lat}, lon={lon}).\n"
            f"Resources: {', '.join([f'{t}:{i}' for t, ids in resources_dict.items() for i in ids])}.\n"
            f"Email {'sent' if notify_email else 'not sent'}."
        )

        return summary, resources_dict


    def handle_webcam(self, camera_id=None, notify_email=None):
        """
        1. Captures up to max_frames from the webcam, writes annotated video to outputs/.
        2. If any accidents were detected, allocate resources and send notification.
        """
        output_video = self.detector.detect_on_webcam(
            camera_index=0,
            conf=0.25,
            save_dir="outputs",
            output_filename="webcam_output.mp4",
            max_frames=300
        )

        # For simplicity, assume if detect_on_webcam returns normally, at least one box was detected.

        loc = self.loc_agent.get_location(camera_id)
        lat, lon = loc["lat"], loc["lon"]
        address = loc.get("address", "Unknown Location")

        allocated = self.allocator.allocate(incident_loc={"lat": lat, "lon": lon})

        subj = f"Accident Alert (Webcam) at {address}"
        body = (
            f"Accident(s) detected on live webcam at {address} "
            f"(lat: {lat}, lon: {lon}).\n"
            f"Resources: {', '.join([r['id'] for r in allocated])}.\n"
            f"Annotated video: {output_video}"
        )
        if notify_email:
          self.notifier.send_whatsapp(
        to_number=notify_email,
        message=f"{subj}\n\n{body}"
    )




        else:
            print("[Notification Skipped – no email provided]")
            print("SUBJECT:", subj)
            print("BODY:", body)

        return f"Webcam detection complete. {body}"
