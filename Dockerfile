# syntax=docker/dockerfile:1

# === Stage 1: The Builder Stage ===
# This stage installs all tools, dependencies, and runs audits.
FROM python:3.14-slim-bookworm AS builder

# Add work directory and upgrade pip
WORKDIR /app
RUN python -m pip install --upgrade pip

# Install system dependencies needed for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*


# Add and switch to non-root user (audits run better as non-root)
RUN adduser --disabled-password --comment '' --home /home/appuser --uid 1000 appuser
USER appuser

# Install Python requirements and audit tools as the appuser
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --user pip-audit safety --no-cache-dir

# Add user bin directory (~/.local/bin) to PATH environment variable
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Run checks and audits (must be in the builder stage)
RUN pip check
RUN pip-audit --strict
# Note: 'safety' audits must use secrets passed to the build command:
# docker build --secret id=safety_api_key,src=./safety_key .
RUN --mount=type=secret,id=safety_api_key,mode=0400,uid=1000 \
    export SAFETY_API_KEY=$(cat /run/secrets/safety_api_key) && \
    safety scan --full-report --strict


# === Stage 2: The Final Runtime Stage ===
# This stage copies only the necessary runtime files from Stage 1
FROM python:3.14-slim-bookworm AS runtime

# Copy the non-root user setup from the builder stage
RUN adduser --disabled-password --comment '' --home /home/appuser --uid 1000 appuser
USER appuser
WORKDIR /app

# Copy ONLY the installed Python packages and required libraries from the builder stage
COPY --from=builder /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages
COPY --from=builder /home/appuser/.local /home/appuser/.local
COPY --from=builder /app/requirements.txt /app/requirements.txt

# Copy all required system libraries for OpenGL/GLIB/atomic/etc. from the builder stage
COPY --from=builder /usr/lib/x86_64-linux-gnu/libGL* /usr/lib/x86_64-linux-gnu/
COPY --from=builder /usr/lib/x86_64-linux-gnu/libglib* /usr/lib/x86_64-linux-gnu/
COPY --from=builder /usr/lib/x86_64-linux-gnu/libgthread* /usr/lib/x86_64-linux-gnu/
COPY --from=builder /usr/lib/x86_64-linux-gnu/libatomic* /usr/lib/x86_64-linux-gnu/
COPY --from=builder /usr/lib/x86_64-linux-gnu/libX11* /usr/lib/x86_64-linux-gnu/
COPY --from=builder /usr/lib/x86_64-linux-gnu/libxcb* /usr/lib/x86_64-linux-gnu/
COPY --from=builder /usr/lib/x86_64-linux-gnu/libXau* /usr/lib/x86_64-linux-gnu/
COPY --from=builder /usr/lib/x86_64-linux-gnu/libXdmcp* /usr/lib/x86_64-linux-gnu/
COPY --from=builder /usr/lib/x86_64-linux-gnu/libbsd* /usr/lib/x86_64-linux-gnu/

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/home/appuser/.local/bin:${PATH}"
    # Re-add the user bin to PATH

# The image definition ends here. 
# Service-specific Dockerfiles will now use 'FROM my-base-image-name:tag'
