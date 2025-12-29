# DevOps ZeroMQ Pipeline

Docker Compose project demonstrating real-time video frame processing with ZeroMQ messaging, OpenCV filtering, and a Dash web dashboard. Includes multi-stage Docker image optimization (reduced from 1.66 GB to 808 MB).

## Features
- Distributed services communicating via ZeroMQ (publisher/subscriber pattern)
- Real-time frame processing with OpenCV
- Web dashboard for live viewing
- Health endpoint and graceful fallback
- Multi-stage Docker builds for minimal image size

## Quick Start

### Prerequisites
- Docker and Docker Compose installed

### Setup
1. Clone the repo
2. Place any short 30 FPS MP4 file in the `/data` folder as `sample_video_30fps.mp4`
3. Copy `.env.example` to `.env` (configure ports if needed)
4. (Optional) Create `safety-api-key.txt` with your API key for the audit tool

### Run
```bash
docker build --secret id=safety_api_key,src=safety-api-key.txt -t base_image:1.0 -f Dockerfile .
docker-compose up -d --build
```
Open http://localhost:7860 in your browser

### Health Check
```bash
curl -f http://localhost:7860/health
```

### Stop & Cleanup
```bash
docker-compose down
docker image rm base_image:1.0 split_frames:1.0 edit_frames:1.0 view_frames:1.0
```

## Image Optimization Notes
See commented history in .env.example — reduced final image from 1.66 GB to 808 MB using multi-stage builds and cleanup.

## Security & Best Practices
- Non-root users in containers
- Read-only filesystems where possible
- Limited capabilities and no privilege escalation
- Resource limits configured
- Docker secrets for sensitive data
- Vulnerability scanning in build (pip-audit, safety)

## Debugging Tips
- Monitor resource usage: `docker stats`
- Filter containers: `docker ps -f name=split_frames`

## 
Built as a personal learning project exploring distributed systems and container optimization.
