# Text-to-Speech Flask API

A lightweight Flask API that converts text to speech and returns audio files. The application is optimized for minimal Docker image size and can be easily deployed.

## Features

- **RESTful API**: Simple HTTP endpoints for text-to-speech conversion
- **Audio Output**: Returns WAV audio files
- **Dockerized**: Optimized for minimal container size
- **Health Check**: Built-in health monitoring endpoint
- **Error Handling**: Comprehensive error handling and validation
- **Security**: Non-root user execution in Docker

## API Endpoints

### POST /tts
Convert text to speech and download audio file.

**Request:**
```json
{
    "text": "Hello, this is a test message."
}
```

**Response:** Audio file (MP3 format)

**Example using curl:**
```bash
curl -X POST http://localhost:5000/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, world!"}' \
  --output speech.mp3
```

### GET /health
Health check endpoint.

**Response:**
```json
{
    "status": "healthy",
    "service": "text-to-speech"
}
```

### GET /
API documentation and usage information.

## Quick Start

### Using Docker (Recommended)

1. **Build the Docker image:**
```bash
docker build -t text2speech-api .
```

2. **Run the container:**
```bash
docker run -p 5000:5000 text2speech-api
```

3. **Test the API:**
```bash
curl -X POST http://localhost:5000/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello from Docker!"}' \
  --output hello.mp3
```

### Local Development

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the application:**
```bash
python app.py
```

3. **Test the API:**
```bash
curl -X POST http://localhost:5000/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello from local development!"}' \
  --output hello.mp3
```

## Testing the API

### Quick Test Commands

**Test health endpoint:**
```bash
curl -s http://localhost:5000/health | python3 -m json.tool
```

**Test TTS endpoint:**
```bash
curl -X POST http://localhost:5000/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, this is a test message!"}' \
  --output test_audio.mp3
```

**Test API documentation:**
```bash
curl -s http://localhost:5000/ | python3 -m json.tool
```

**Test error handling:**
```bash
# Missing text field
curl -X POST http://localhost:5000/tts \
  -H "Content-Type: application/json" \
  -d '{"invalid": "data"}' | python3 -m json.tool

# Empty text
curl -X POST http://localhost:5000/tts \
  -H "Content-Type: application/json" \
  -d '{"text": ""}' | python3 -m json.tool
```

## Docker Optimization

The Docker image is optimized for minimal size:

- **Base Image**: `python:3.11-slim` (minimal Python image)
- **System Dependencies**: Only essential packages for TTS functionality
- **Multi-stage**: Efficient layer caching
- **Security**: Non-root user execution
- **Health Check**: Built-in container health monitoring

## Configuration

The TTS engine can be configured by modifying the gTTS parameters in `app.py`:

- **Language**: Default 'en' (English)
- **Speed**: Default slow=False (normal speed)
- **Voice**: Uses Google's default voice for the language

## Limitations

- **Text Length**: Maximum 1000 characters per request
- **Audio Format**: MP3 format only
- **Language**: English (can be modified in app.py)
- **Internet Required**: Uses Google Text-to-Speech service

## Production Deployment

For production deployment, consider:

1. **Reverse Proxy**: Use nginx or similar
2. **Process Manager**: Use gunicorn or uwsgi
3. **Environment Variables**: Configure via environment
4. **Logging**: Implement proper logging
5. **Monitoring**: Add metrics and monitoring

### Example with Gunicorn

```dockerfile
# Add to Dockerfile
RUN pip install gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

## Troubleshooting

### Common Issues

1. **Audio not generated**: Check if espeak is properly installed
2. **Permission errors**: Ensure proper file permissions
3. **Memory issues**: Monitor container memory usage

### Debug Mode

To run in debug mode locally:
```bash
export FLASK_DEBUG=1
python app.py
```

## License

This project is open source and available under the MIT License.
