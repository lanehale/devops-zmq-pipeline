# ----------------------------------------------------------------------------- #
#  Processes video frames in real time, applying filters via OpenCV             #
#  Receives frames from source service via ZeroMQ, performs custom processing,  #
#  and forwards to dashboard for display                                        #
# ----------------------------------------------------------------------------- #

# Imports
...


BORDER_COLOR = (...)
FILL_VALUE = ...
BORDER_WIDTH = ...

SPLIT_FRAMES_PORT = os.getenv("SPLIT_FRAMES_PORT", default="7001")
SPLIT_FRAMES_HOST = os.getenv("SPLIT_FRAMES_HOST", default="localhost")
EDIT_FRAMES_PORT = os.getenv("EDIT_FRAMES_PORT", default="7002")
EDIT_FRAMES_HOST = os.getenv("EDIT_FRAMES_HOST", default="*")  # bind - access all


def add_border(...):
    # top
    ...
    # right
    ...
    # bottom
    ...
    # left
    ...

    return image


def edit_frames():
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect(f"tcp://{SPLIT_FRAMES_HOST}:{SPLIT_FRAMES_PORT}")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"")

    publisher = context.socket(zmq.PUB)
    publisher.bind(f"tcp://{EDIT_FRAMES_HOST}:{EDIT_FRAMES_PORT}")

    count = 0
    while True:
        # Check if frames are being sent (published)
        data = subscriber.recv()
        ...

        # Edit the frames
        image = add_border(...)
        ...

        # Send to view_frames
        publisher.send(data)
        ...


if __name__ == "__main__":
    print("edit_frames started.")
    edit_frames()
