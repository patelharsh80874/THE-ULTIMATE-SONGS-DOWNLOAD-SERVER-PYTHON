from flask import Flask, request, jsonify, send_file
import requests
import logging
from mutagen.mp4 import MP4, MP4Cover
from pathlib import Path
from flask_cors import CORS
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/generate-audio', methods=['GET'])
def download_song():
    try:
        # Get the song details from the query parameters
        audio_url = request.args.get('audioUrl')
        image_url = request.args.get('imageUrl')
        song_name = request.args.get('songName', 'Unknown')
        artist = request.args.get('artist', 'Unknown')
        album = request.args.get('album', 'Unknown')
        year = request.args.get('year', 'Unknown')
        
        if not audio_url:
            return jsonify({"error": "Audio URL is required"}), 400
        
        logger.info(f"Downloading song: {song_name} by {artist}")

        # Validate and fetch the image
        image_content = None
        if image_url:
            try:
                image_response = requests.get(image_url, timeout=10)
                image_response.raise_for_status()

                # Check if the image can be opened
                image_bytes = io.BytesIO(image_response.content)
                with Image.open(image_bytes) as img:
                    if img.format == "WEBP":
                        img = img.convert("RGB")
                        converted_image = io.BytesIO()
                        img.save(converted_image, format="JPEG")
                        converted_image.seek(0)
                        image_content = converted_image.read()
                    else:
                        image_content = image_response.content
            except Exception as e:
                logger.error(f"Invalid image URL or failed to fetch image: {e}")
                return jsonify({"error": "Invalid or inaccessible image URL"}), 400

        # Create file path using pathlib for cross-platform compatibility
        tmp_dir = Path('/tmp')
        if not tmp_dir.exists():
            tmp_dir.mkdir(parents=True, exist_ok=True)
            
        song_id = song_name.replace(" ", "_")  # Use song name as ID for file naming
        file_path = tmp_dir / f"song_{song_id}.m4a"
        logger.info(f"Temporary file path: {file_path}")

        # Fetch and save the audio file
        audio_response = requests.get(audio_url, stream=True)
        audio_response.raise_for_status()

        # Write the file
        with open(file_path, 'wb') as f:
            for chunk in audio_response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Add metadata with cover art
        def add_metadata_with_cover(file_path, image_content):
            """Add metadata including cover art to the M4A file."""
            try:
                audio = MP4(file_path)

                # Add metadata
                audio.tags['\xa9nam'] = [song_name]
                audio.tags['\xa9ART'] = [artist]
                audio.tags['\xa9alb'] = [album]
                audio.tags['\xa9day'] = [year]

                # Add cover art
                if image_content:
                    cover_data = MP4Cover(image_content, MP4Cover.FORMAT_JPEG)
                    audio.tags['covr'] = [cover_data]

                audio.save()
                logger.info(f"Metadata added to {file_path}")
                return True

            except Exception as e:
                logger.error(f"Error adding metadata: {e}")
                return False

        if not add_metadata_with_cover(str(file_path), image_content):
            logger.warning("Failed to add metadata to the file")

        try:
            # Send the file as response
            return send_file(
                str(file_path),
                as_attachment=True,
                download_name=f"{song_name}.m4a",
                mimetype="audio/mp4"
            )
        finally:
            # Clean up the file after sending
            try:
                if file_path.exists():
                    file_path.unlink()
                    logger.info(f"Temporary file {file_path} deleted successfully.")
            except Exception as e:
                logger.error(f"Error removing temporary file: {e}")

    except requests.exceptions.RequestException as e:
        logger.error(f"API request error: {e}")
        return jsonify({"error": "Failed to fetch data from the provided URL"}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=['GET'])
def index():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>THE ULTIMATE MP3 Metadata Embedder</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link
    href="https://cdn.jsdelivr.net/npm/remixicon@4.5.0/fonts/remixicon.css"
    rel="stylesheet"
    />
    <style>
        /* Global Styles */
        body {
            background-color: #141414; /* Dark background */
            color: white;
            font-family: 'Inter', sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        /* Form Container */
        .form-container {
            border-radius: 12px;
            padding-left: 5%;
            width: 90%;
            height:100vh;
        }

        h1 {
            font-size: 15px;
            text-align: center;
            color: #ffcb00;
            margin-bottom: 20px;
        }

        label {
            font-size: 12px;
            color: #b3b3b3;
            font-weight: 500;
            margin-bottom: 5px;
            display: block;
        }

        input {
            width: 80%;
            padding: 12px;
            margin-bottom: 15px;
            border: 2px solid #333;
            background-color: #222;
            color: #fff;
            border-radius: 8px;
            font-size: 12px;
        }

        input:focus {
            outline: none;
            border-color: #ffcb00;
        }

        button {
            width: 25%;
            padding: 12px;
            background-color: #ffcb00;
            color: #141414;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        button:hover {
            background-color: #ffb400;
        }

        /* Success and Error Message */
        #message {
            margin-top: -20px;
            text-align: right;
            font-size: 12px;
            font-weight: 600;
        }

        .success {
            color: #28a745;
        }

        .error {
            color: #dc3545;
        }
        .info-div{
        display:flex;
        align-items: center;
        justify-content: center;
        gap:1vw;
        }

        @media only screen and (max-width: 600px) {
              #message {
            margin-top: 20px;
            text-align: center;
            font-size: 12px;
            font-weight: 600;
        }
        }
    </style>
</head>
<body>
    <div class="form-container">
    <div class="info-div">
    <h1>THE ULTIMATE MP3/M4A Metadata Embedder(python)<span style="font-size: 14px; color: #b3b3b3;"> (made by HARSH PATEL)</span></h1>
    <a href="https://github.com/patelharsh80874/THE-ULTIMATE-SONGS-DOWNLOAD-SERVER-PYTHON" target="_blank" title="GitHub Repository" style="text-decoration: none;">
    <i class="ri-github-fill" style="font-size: 36px; color: #b3b3b3;"></i>
    </a>
    <a href="https://instagram.com/patelharsh.in" target="_blank" title="instagram" style="text-decoration: none;">
    <i class="ri-instagram-fill" style="font-size: 36px; color: #b3b3b3;"></i>
    </a>
    </div>
        <form id="mp3Form">
            <label for="audioUrl">Audio URL:</label>
            <input type="url" id="audioUrl" name="audioUrl" required>

            <label for="imageUrl">Image URL:</label>
            <input type="url" id="imageUrl" name="imageUrl" required>

            <label for="songName">Song/Audio Name:</label>
            <input type="text" id="songName" name="songName" required>

            <label for="year">Year:</label>
            <input type="text" id="year" name="year" required>

            <label for="album">Album Name:</label>
            <input type="text" id="album" name="album" required>

            <label for="artist">Artist Name:</label>
            <input type="text" id="artist" name="artist" required>

            <button type="submit">Submit</button>
            <div id="message"></div>
        </form>
    </div>

    <script>
        document.getElementById('mp3Form').addEventListener('submit', function(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new URLSearchParams(new FormData(form));
    
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = "Submitting... your audio is being processed"; // Show loading message
    messageDiv.className = ""; // Clear previous classes
    
    // Extract the song name from the form data
    const songName = form.querySelector('input[name="songName"]').value || 'your_audio';  // Default to 'your_audio' if not provided

    // Make the request to generate the audio and handle the response
    fetch('/generate-audio?' + formData.toString(), {
        method: 'GET',
        headers: {
            'Accept': 'application/json', // Ensure server returns response in JSON
        }
    })
    .then(response => {
        if (response.ok) {
            // File is being processed and will be downloaded
            return response.blob();  // Return the audio file as blob for download
        } else {
            throw new Error('Error generating audio');
        }
    })
    .then(blob => {
        // Create a download link and simulate a click to start the download
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = songName + '.m4a'; // Use string concatenation instead of template literals
        link.click();
        

        // Success message after file is downloaded
        setTimeout(() => {
            form.reset();
            messageDiv.textContent = "Form submitted successfully! Your audio is ready for download.";
            messageDiv.className = "success";
        }, 500);
    })
    .catch(error => {
        // Handle errors (e.g., network issues, server issues)
        setTimeout(() => {
            messageDiv.textContent = "Error occurred. Please try again. Or Check Your Audio/Image URL Is Correct Or Not.";
            messageDiv.className = "error";
        }, 500);
    });
});
    </script>
</body>
</html>'''

# if __name__ == '__main__':
#     app.run(debug=True)