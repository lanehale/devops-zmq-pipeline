# edit_frames/Dockerfile

# Define a build argument that will be provided at build time
ARG BASE_VERSION=1.0

# Use the build argument variable in the FROM instruction
FROM base_image:${BASE_VERSION}

# Copy edit_frames code
COPY . /app/
WORKDIR /app

# Run edit_frames service
CMD ["python3", "-u", "__main__.py"]
