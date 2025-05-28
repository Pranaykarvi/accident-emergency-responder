import json
import os

class LocationAgent:
    def __init__(self, config_path="agents/camera_locations.json"):
        """
        Loads a JSON file mapping camera IDs to locations.
        If file not found, uses an empty default dictionary.
        """
        if os.path.isfile(config_path):
            with open(config_path, "r") as f:
                self.locations = json.load(f)
        else:
            self.locations = {}

    def get_location(self, camera_id=None):
        """
        Returns a dict {"lat": float, "lon": float, "address": str}.
        If camera_id not found or None, returns a default location.
        """
        if camera_id and camera_id in self.locations:
            return self.locations[camera_id]
        # Default fallback location (example: New Delhi)
        return {"lat": 28.7041, "lon": 77.1025, "address": "New Delhi, India"}
