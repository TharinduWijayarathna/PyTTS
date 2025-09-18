from flask import Flask, request, send_file, jsonify
from gtts import gTTS
import tempfile
import os
import uuid
import io

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "text-to-speech"})

@app.route('/tts', methods=['POST'])
def text_to_speech():
    """Convert text to speech and return audio file"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({"error": "Text is required"}), 400
        
        text = data['text'].strip()
        if not text:
            return jsonify({"error": "Text cannot be empty"}), 400
        
        # Limit text length to prevent abuse
        if len(text) > 1000:
            return jsonify({"error": "Text too long. Maximum 1000 characters allowed."}), 400
        
        # Create temporary file for audio output
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        temp_file.close()
        
        # Generate speech using gTTS
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(temp_file.name)
        
        # Check if file was created successfully
        if not os.path.exists(temp_file.name) or os.path.getsize(temp_file.name) == 0:
            return jsonify({"error": "Failed to generate audio"}), 500
        
        # Return the audio file
        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=f"speech_{uuid.uuid4().hex[:8]}.mp3",
            mimetype='audio/mpeg'
        )
        
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500
    
    finally:
        # Clean up temporary file
        if 'temp_file' in locals() and os.path.exists(temp_file.name):
            try:
                os.unlink(temp_file.name)
            except:
                pass

@app.route('/', methods=['GET'])
def index():
    """API documentation"""
    return jsonify({
        "service": "Text-to-Speech API",
        "version": "1.0.0",
        "endpoints": {
            "POST /tts": "Convert text to speech",
            "GET /health": "Health check",
            "GET /": "This documentation"
        },
        "usage": {
            "POST /tts": {
                "content-type": "application/json",
                "body": {"text": "Your text here"},
                "response": "Audio file (MP3 format)"
            }
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
