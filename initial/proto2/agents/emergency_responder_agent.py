import random
from datetime import datetime, timedelta

class EmergencyResponderAgent:
    def __init__(self):
        self.active_dispatches = []

    def dispatch(self, resources, location):
        """
        Simulates dispatch of emergency services.
        Args:
            resources (dict): e.g., {"ambulance": ["AMB1"], "police": ["POL1"]}
            location (dict): { "latitude": float, "longitude": float, "address": str }

        Returns:
            dict: Dispatch summary with ETAs and status.
        """
        dispatch_time = datetime.now()
        summary = {
            "timestamp": dispatch_time.isoformat(),
            "location": location,
            "dispatched_units": [],
        }

        for r_type, r_ids in resources.items():
            for r_id in r_ids:
                eta = dispatch_time + timedelta(seconds=random.randint(5, 10))
                unit_record = {
                    "id": r_id,
                    "type": r_type,
                    "status": "dispatched",
                    "dispatched_at": dispatch_time.isoformat(),
                    "eta": eta.isoformat()
                }
                self.active_dispatches.append(unit_record)
                summary["dispatched_units"].append(unit_record)

        print(f"[🚨 Dispatch Initiated] {len(summary['dispatched_units'])} units dispatched to {location['address']}")
        return summary

    def track_status(self):
        """
        Returns only units whose status changed to 'arrived'.
        """
        current_time = datetime.now()
        newly_arrived = []

        for unit in self.active_dispatches:
            eta = datetime.fromisoformat(unit["eta"])
            if current_time >= eta and unit["status"] != "arrived":
                unit["status"] = "arrived"
                unit["arrived_at"] = current_time.isoformat()
                print(f"[✅ Unit Arrived] {unit['type'].upper()} {unit['id']} arrived at scene.")
                newly_arrived.append(unit)

        return newly_arrived

    def get_all_statuses(self):
        """Return status of all units (dispatched or arrived)."""
        return self.active_dispatches
