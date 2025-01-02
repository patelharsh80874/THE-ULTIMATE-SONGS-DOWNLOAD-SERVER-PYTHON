# THE ULTIMATE SONGS DOWNLOAD SERVER PYTHON

A Flask-based server application that allows users to download songs with embedded metadata and album art. All input fields are mandatory to ensure proper metadata embedding and album cover functionality.

---

## Features
- Download audio files (`.m4a`) with metadata and album art.
- Metadata support: Title, Artist, Album, Year, and Cover Art.
- Supports `WEBP` album covers (auto-conversion to JPEG).
- Error handling for invalid or missing fields.
- Lightweight and fast, designed for seamless user experience.
- Temporary files are automatically cleaned up after download.

---

## Technologies Used
- **Flask**: Web server framework.
- **Flask-CORS**: Enable Cross-Origin Resource Sharing (CORS).
- **Requests**: Handle HTTP requests for downloading audio and image files.
- **Mutagen**: Add metadata to audio files.
- **Pillow**: Validate and process image files.
- **Python**: Backend logic implementation.

---

## API Endpoint

### **`GET /generate-audio`**

#### Query Parameters (All Required):
| Parameter   | Type   | Description                                                |
|-------------|--------|------------------------------------------------------------|
| `audioUrl`  | String | URL of the audio file to download.                         |
| `imageUrl`  | String | URL of the album cover image.                              |
| `songName`  | String | Name of the song.                                          |
| `artist`    | String | Artist of the song.                                        |
| `album`     | String | Album name of the song.                                    |
| `year`      | String | Release year of the song.                                  |

#### Response:
- **Success**: Returns the `.m4a` audio file with embedded metadata.
- **Failure**: Returns a JSON error message with appropriate HTTP status codes.

#### Example Request:
```bash
curl -X GET "http://127.0.0.1:5000/generate-audio?audioUrl=https://example.com/audio.m4a&imageUrl=https://example.com/image.webp&songName=Farzi&artist=Sachin-Jigar&album=Farzi&year=2023"
```

---

## Installation

### Clone the Repository:
```bash
git clone https://github.com/patelharsh80874/THE-ULTIMATE-SONGS-DOWNLOAD-SERVER-PYTHON
cd your-repo-name
```

### Create a Virtual Environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies:
```bash
pip install -r requirements.txt
```

### Run the Server:
```bash
python app.py
```

### Access the API:
The server runs on `http://127.0.0.1:5000` by default.

---

## File Structure

```
.
├── app.py                # Main Flask application
├── requirements.txt      # Project dependencies
├── README.md             # Project documentation
└── /tmp                  # Temporary directory for downloaded files
```

---

## Error Handling

1. **Missing or Invalid Parameters**:
   - Returns: `{"error": "All fields are required"}` with HTTP `400`.

2. **Invalid Audio URL**:
   - Returns: `{"error": "Invalid or inaccessible audio URL"}` with HTTP `400`.

3. **Invalid Image URL**:
   - Returns: `{"error": "Invalid or inaccessible image URL"}` with HTTP `400`.

4. **Server Error**:
   - Returns: `{"error": "Unexpected error occurred"}` with HTTP `500`.

---

## Requirements

Below is the content of `requirements.txt`:

```plaintext
blinker==1.9.0
certifi==2024.8.30
charset-normalizer==3.4.0
click==8.1.7
colorama==0.4.6
Flask==3.1.0
idna==3.10
itsdangerous==2.2.0
Jinja2==3.1.4
MarkupSafe==3.0.2
mutagen==1.47.0
requests==2.32.3
urllib3==2.2.3
Werkzeug==3.1.3
flask_cors==3.0.10
Pillow==11.0.0
```

To install all dependencies:
```bash
pip install -r requirements.txt
```

---
