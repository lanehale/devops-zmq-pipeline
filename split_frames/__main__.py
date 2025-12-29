# ----------------------------------------------------------------------------- #
#  Publishes video frames via ZeroMQ                                            #
#  Reads a video file, extracts frames at the original FPS, and publishes them  #
#  to a processing service for real-time handling                               #
# ----------------------------------------------------------------------------- #

# Imports
...


VIDEO_PATH = os.getenv("DATA_FILE")
SPLIT_FRAMES_PORT = os.getenv("SPLIT_FRAMES_PORT", default="7001")
SPLIT_FRAMES_HOST = os.getenv("SPLIT_FRAMES_HOST", default="*")  # bind - accept all


def main():
    # Verify the video path is found
    if not os.path.exists(VIDEO_PATH):
        print(f"Error: Video file not found at {VIDEO_PATH}")
        return

    # Open the video
    ...

    # Set frame parameters
    ...

    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind(f"tcp://{SPLIT_FRAMES_HOST}:{SPLIT_FRAMES_PORT}")

    count = 0
    while True:
        # Split video into frames
        ...

        if success:
            ...

            # Publish frames to edit_frames (subscriber)
            publisher.send(data)
            ...

        else:
            print(
                "Finished split_frames. Exiting loop."
            )  # Docker will restart the service automatically
            ...

    # Release resources
    ...


if __name__ == "__main__":
    print("split_frames started.")
    main()
