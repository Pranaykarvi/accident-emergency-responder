class ResourceAllocator:
    def __init__(self):
        """
        Example resources with their “current” locations.
        In a real setup, these would update dynamically.
        """
        self.resources = [
            {"type": "ambulance", "id": "AMB1", "lat": 28.7000, "lon": 77.1000},
            {"type": "ambulance", "id": "AMB2", "lat": 28.7050, "lon": 77.1080},
            {"type": "police",    "id": "POL1", "lat": 28.7100, "lon": 77.1100},
            {"type": "fire",      "id": "FIR1", "lat": 28.6980, "lon": 77.0950}
        ]

    @staticmethod
    def _distance(lat1, lon1, lat2, lon2):
        """
        Simple Euclidean distance between two lat/lon points (for demo only).
        """
        return ((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) ** 0.5

    def allocate(self, incident_loc, needed_types=None):
        """
        incident_loc: {"lat": float, "lon": float}
        needed_types: list of resource types, e.g. ["ambulance", "police"].
                      If None, allocates one of each type.
        Returns a list of allocated resource dicts.
        """
        if needed_types is None:
            needed_types = ["ambulance", "police", "fire"]

        allocated = []
        for rtype in needed_types:
            candidates = [r for r in self.resources if r["type"] == rtype]
            if not candidates:
                continue
            # Choose the candidate with the smallest Euclidean distance
            closest = min(
                candidates,
                key=lambda r: self._distance(
                    r["lat"], r["lon"], incident_loc["lat"], incident_loc["lon"]
                )
            )
            allocated.append(closest)
        return allocated
