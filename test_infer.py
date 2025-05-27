# File: test_infer.py

from agents.accident_agent import AccidentAgent

if __name__ == "__main__":
    agent = AccidentAgent()

    # Replace this with a known test image path containing an accident
    test_image = "datasets/labeled/test/images/Accidents-online-video-cutter_com-1-_mp4-113_jpg.rf.844efa2b5085d474ec7d125ba8fa8a42.jpg"

    print(f"Analyzing {test_image}...\n")
    summary = agent.handle_image(
    image_path=test_image,
    camera_id="cam_entrance",
    notify_email="whatsapp:+918655287793"
)

    print("\nSummary:\n" + summary)
