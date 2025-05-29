import os
from src.detection.accident_detector import AccidentDetector
from agents.location_agent import LocationAgent
from agents.resource_allocator import ResourceAllocator
from agents.notifier_agent import NotifierAgent as EmailAgent
from agents.messenger_agent import MessengerAgent as WhatsAppAgent  # ✅ distinct alias

class AccidentAgent:
    def __init__(self):
        self.detector = AccidentDetector()
        self.loc_agent = LocationAgent()
        self.allocator = ResourceAllocator()
        self.email_notifier = EmailAgent()
        self.whatsapp_notifier = WhatsAppAgent()

        # Ensure outputs/ directory exists for annotated images/videos
        os.makedirs("outputs", exist_ok=True)

    def handle_image(self, image_path, camera_id=None, notify_email=None):
        """
        1. Run YOLO detection on image_path and save annotated image to outputs/.
        2. If any box is found, look up location, allocate resources, send WhatsApp.
        Returns a summary string AND a structured resources dict.
        """
        result = self.detector.detect_on_image(
            image_path=image_path,
            conf=0.25,
            save=True,
            save_dir="outputs"
        )
        num_boxes = len(result.boxes)
        if num_boxes == 0:
            return "No accidents detected.", {}

        # Location lookup
        loc = self.loc_agent.get_location(camera_id)
        lat, lon = loc["lat"], loc["lon"]
        address = loc.get("address", "Unknown Location")

        # Resource allocation
        allocated = self.allocator.allocate(incident_loc={"lat": lat, "lon": lon})

        # Compose message
        subj = f"Accident Alert at {address}"
        body = (
            f"Accident detected at {address} (lat: {lat}, lon: {lon}).\n"
            f"Number of incidents: {num_boxes}\n"
            f"Allocated: {', '.join([r['id'] for r in allocated])}"
        )

        # WhatsApp notification
        if notify_email:
            self.whatsapp_notifier.send_whatsapp(
                to_number=notify_email,
                message=f"{subj}\n\n{body}"
            )
        else:
            print("[Notification Skipped – no contact provided]")
            print("SUBJECT:", subj)
            print("BODY:", body)

        # Organize resources
        resources_dict = {}
        for r in allocated:
            resources_dict.setdefault(r["type"], []).append(r["id"])

        summary = (
            f"Detected {num_boxes} accident(s) at {address} (lat={lat}, lon={lon}).\n"
            f"Resources: {', '.join([f'{t}:{i}' for t, ids in resources_dict.items() for i in ids])}.\n"
            f"WhatsApp {'sent' if notify_email else 'not sent'}."
        )

        return summary, resources_dict

    def handle_webcam(self, camera_id=None, notify_email=None):
        """
        1. Captures up to max_frames from the webcam, writes annotated video to outputs/.
        2. If any accidents were detected, allocate resources and send WhatsApp.
        """
        output_video = self.detector.detect_on_webcam(
            camera_index=0,
            conf=0.25,
            save_dir="outputs",
            output_filename="webcam_output.mp4",
            max_frames=300
        )

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
            self.whatsapp_notifier.send_whatsapp(
                to_number=notify_email,
                message=f"{subj}\n\n{body}"
            )
        else:
            print("[Notification Skipped – no contact provided]")
            print("SUBJECT:", subj)
            print("BODY:", body)

        return f"Webcam detection complete. {body}"
