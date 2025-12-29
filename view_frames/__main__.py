# ----------------------------------------------------------------------------- #
#  Web dashboard for real-time frame display                                    #
#  Subscribes to processed frames via ZeroMQ and renders them in a Dash UI      #
#  Includes health endpoint and graceful fallback for no-data states            #
# ----------------------------------------------------------------------------- #

# Imports
...


EDIT_FRAMES_PORT = os.getenv("EDIT_FRAMES_PORT", default="7002")
EDIT_FRAMES_HOST = os.getenv("EDIT_FRAMES_HOST", default="localhost")


app = dash.Dash(__name__)


# Health check endpoint for proper container orchestration
@app.server.route("/health")
def health():
    return "Service is healthy", 200


app.layout = html.Div(
    style={...},
    children=[
        html.H1(...),
        html.Div(...),
        dcc.Interval(
            id="...",
            # Slowed this down for it to work in normal (non-incognito) tab using 'python view_frames/__main__.py' in cmd.exe
            interval=100,
            n_intervals=0,
        ),
    ],
)

context = zmq.Context()
subscriber = context.socket(zmq.SUB)
subscriber.connect(f"tcp://{EDIT_FRAMES_HOST}:{EDIT_FRAMES_PORT}")
subscriber.setsockopt_string(zmq.SUBSCRIBE, "")
print("connection complete")

image = None


# Define a distinct color, e.g., solid Red in BGR format (0, 0, 255)
PLACEHOLDER_COLOR = (0, 0, 255)


def generate_image():
    # Use a clear indicator that data is not yet flowing
    width, height = 400, 400
    # Create a solid red image placeholder
    image = np.full((height, width, 3), PLACEHOLDER_COLOR, dtype=np.uint8)

    # Add text to the image for clarity
    text = "NO DATA FLOWING"
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(
        image, text, (50, height // 2), font, 1, (255, 255, 255), 2, cv2.LINE_AA
    )

    return image


@app.callback(Output(...), Input(...))
def update_view(n_intervals):
    global image
    global subscriber

    # Check if frames are being sent (published)
    while subscriber.poll(0):
        data = subscriber.recv()
        ...

    # If no frames yet, use placeholder image
    if image is None:
        image = generate_image()

    # Decode frame image to base64
    ...

    # Display base64 as html jpg
    ...

    return image_html


if __name__ == "__main__":
    print("view_frames started.")
    app.run(host="0.0.0.0", debug=False)
