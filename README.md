# Async Audio/Video Transcription Tool

This tool transcribes multiple audio and video files asynchronously, speeding up processing for long files by transcribing segments in parallel. It supports MP4 files (with audio extraction) and pre-extracted WAV audio files. Each file is processed separately, and the transcription is saved to a dedicated output file.

## Features
- Transcribes audio/video files using Google’s Speech Recognition API.
- Supports asynchronous processing for multiple segments within a single file.
- Saves each file's transcription to a separate text file.
- Supports multiple input files in a single run.


____
## Installation

### Prerequisites
- Python 3.6 or higher
- [FFmpeg](https://ffmpeg.org/download.html) (required for `moviepy` to extract audio from video files)

### Clone the Repository
```bash
git clone https://github.com/voidshaman/mp4toText.git
cd mp4toText
```

### Install Dependencies
The required libraries are listed in requirements.txt. Install them with:

```bash 
pip install -r requirements.txt
```

### Requirements Summary
moviepy: For extracting audio from video files.
pydub: For splitting audio files into segments.
speechrecognition: For transcribing audio with Google Speech Recognition.


_____
## Usage
The tool accepts multiple audio or video files as input. Each file’s transcription is saved to a separate file, named after the original file with _transcription.txt appended.

### Command-line Arguments
-f or --files: Paths to audio/video files to process (space-separated for multiple files).
-l or --language: Language code for transcription (default is English, en-US). For example, use tr-TR for Turkish.

### Example Commands
Transcribe a Single Video File

```python
python transcribe_audio.py -f your_video_file.mp4 -l en-US
```
Transcribe Multiple Audio/Video Files
```python
python transcribe_audio.py -f file1.mp4 file2.mp4 file3.wav -l en-US
```
Each file’s transcription will be saved to:

- file1_transcription.txt
- file2_transcription.txt
- file3_transcription.txt

### Supported File Formats
MP4: The tool extracts audio before transcription.
WAV: Directly transcribes without audio extraction.

### Notes
Ensure FFmpeg is installed on your system to support audio extraction from MP4 files.
Long files are automatically split into 60-second segments, which are transcribed in parallel for faster processing.

### Example Output
For your_video_file.mp4, the output file will be named your_video_file_transcription.txt and include the transcription for each segment.


[Transcription content here]
License
This project is licensed under the MIT License.

Contributing
Feel free to submit issues or pull requests for improvements or bug fixes. Contributions are always welcome!
