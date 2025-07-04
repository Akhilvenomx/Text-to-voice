# Import necessary libraries
from flask import Flask, request, send_file, jsonify
from gtts import gTTS
import os
from io import BytesIO
from flask_cors import CORS # Required for handling Cross-Origin Resource Sharing

# Initialize the Flask application
app = Flask(__name__)
# Enable CORS for all origins, allowing your HTML page to make requests
CORS(app)

@app.route('/')
def home():
    """
    A simple home route to confirm the server is running.
    """
    return "Text-to-Speech Backend is running!"

@app.route('/generate-mp3', methods=['POST'])
def generate_mp3():
    """
    API endpoint to generate an MP3 file from text using gTTS.
    Expects a JSON payload with 'text', 'lang', and 'tld'.
    Returns the generated MP3 file.
    """
    # Check if the request body is JSON
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    text = data.get('text')
    lang = data.get('lang', 'en') # Default to English if not provided
    tld = data.get('tld', 'us')   # Default to US TLD if not provided

    # Validate input
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # Create a gTTS object
        tts = gTTS(text=text, lang=lang, tld=tld, slow=False)

        # Save the audio to a BytesIO object (in-memory file)
        # This avoids writing to the disk, which is good for temporary files
        mp3_fp = BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0) # Rewind the stream to the beginning

        # Send the MP3 file back as a response
        return send_file(
            mp3_fp,
            mimetype='audio/mpeg',
            as_attachment=True,
            download_name='speech.mp3' # Suggested filename for download
        )

    except Exception as e:
        # Catch any errors during gTTS processing
        print(f"Error generating MP3: {e}")
        return jsonify({"error": f"Failed to generate MP3: {str(e)}. Check text or language parameters."}), 500

# Run the Flask app
if __name__ == '__main__':
    # Ensure gTTS can access its data (optional, but good for some environments)
    # os.environ['GTTS_LANG_DICT_PATH'] = '/path/to/your/gtts_lang_dict.json'
    app.run(debug=True, port=5000) # Run on port 5000, debug=True for development
