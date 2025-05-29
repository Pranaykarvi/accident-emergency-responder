# File: test_infer.py

from agents.accident_agent import AccidentAgent
from agents.emergency_responder import EmergencyResponder  # ✅ New
import time

if __name__ == "__main__":
    agent = AccidentAgent()
    dispatcher = EmergencyResponder()

    # Test image path with a known accident
    test_image = "datasets/labeled/test/images/Accidents-online-video-cutter_com-1-_mp4-113_jpg.rf.844efa2b5085d474ec7d125ba8fa8a42.jpg"

    print(f"Analyzing {test_image}...\n")
    summary = agent.handle_image(
        image_path=test_image,
        camera_id="cam_entrance",
        notify_email="whatsapp:+918655287793"
    )

    print("\n📋 Summary from AccidentAgent:")
    print(summary)

    # Extract location from summary for dispatch (basic method)
    location = "Entrance Gate"

    print("\n[🚨 Dispatch Initiated] Dispatching emergency units to", location)
    dispatch_log = dispatcher.dispatch(location)

    print("\n🚑 Dispatch Log:")
    for unit in dispatch_log["units"]:
        print(
            f" - {unit['type'].capitalize()} {unit['id']} | ETA: {unit['eta']} | Status: {unit['status']}"
        )

    print("\n⏳ Waiting for ETA simulation...\n")
    time.sleep(2)

    updated_units = dispatcher.check_status(location)
    print("📡 Updated Statuses:")
    for unit in updated_units["units"]:
        print(f" - {unit['type'].capitalize()} {unit['id']} | Status: {unit['status']}")
