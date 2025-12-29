# view_frames/Dockerfile

# Define a build argument that will be provided at build time
ARG BASE_VERSION=1.0

# Use the build argument variable in the FROM instruction
FROM base_image:${BASE_VERSION}

# Copy view_frames code
COPY . /app/
WORKDIR /app

# Run view_frames app with unbuffered output
CMD ["python3", "-u", "__main__.py"]
