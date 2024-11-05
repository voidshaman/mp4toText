import argparse
import os
from pydub import AudioSegment
import speech_recognition as sr
from moviepy.editor import AudioFileClip

def extract_audio_from_video(video_path, output_audio_path):
    """Extract audio from a video file and save it as a WAV file."""
    try:
        audio_clip = AudioFileClip(video_path)
        audio_clip.write_audiofile(output_audio_path, codec="pcm_s16le", fps=16000)
        audio_clip.close()
        print(f"Audio extraction completed successfully from {video_path}.")
    except Exception as e:
        print(f"Error extracting audio from {video_path}: {e}")
        return False
    return True

def split_audio(audio_path, segment_length_ms=60000):
    """Split audio into segments of specified length (default is 60 seconds)."""
    audio = AudioSegment.from_wav(audio_path)
    segments = []
    for i in range(0, len(audio), segment_length_ms):
        segment = audio[i:i + segment_length_ms]
        segment_path = f"segment_{i // segment_length_ms}.wav"
        segment.export(segment_path, format="wav")
        segments.append(segment_path)
    return segments

def transcribe_audio_segment(segment_path, language):
    """Transcribe a single audio segment."""
    recognizer = sr.Recognizer()
    audio_data = sr.AudioFile(segment_path)
    
    with audio_data as source:
        recognizer.adjust_for_ambient_noise(source)
        audio_content = recognizer.record(source)
    
    try:
        transcription = recognizer.recognize_google(audio_content, language=language)
        return transcription
    except Exception as e:
        print(f"Error during transcription of {segment_path}: {e}")
        return ""

if __name__ == "__main__":
    # Argument parser for specifying the video or audio files and language
    parser = argparse.ArgumentParser(description="Transcribe multiple audio or video files and save each transcription to a separate file.")
    parser.add_argument("-f", "--files", nargs='+', required=True, help="Paths to video or audio files to be processed")
    parser.add_argument("-l", "--language", default="en-US", help="Language code for transcription (e.g., 'tr-TR' for Turkish)")

    args = parser.parse_args()
    files = args.files
    language = args.language
    audio_output_path = "temp_extracted_audio.wav"  # Temporary file for audio extraction
    
    # Process each file in the queue
    for file_path in files:
        print(f"\nProcessing file: {file_path}")
        
        # Generate an output filename based on the input file name
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_file_path = f"{base_name}_transcription.txt"

        # Check if it's an MP4 file or a pre-extracted WAV file
        if file_path.lower().endswith(".mp4"):
            print("Extracting audio from video file...")
            if not extract_audio_from_video(file_path, audio_output_path):
                print(f"Skipping {file_path} due to extraction error.")
                continue
            audio_path = audio_output_path
        else:
            audio_path = file_path  # Use provided audio file directly

        # Ensure the audio file exists
        if not os.path.isfile(audio_path):
            print(f"Error: The audio file '{audio_path}' was not found. Skipping.")
            continue

        # Split audio into 60-second segments
        print("Splitting audio into 60-second segments...")
        segments = split_audio(audio_path)

        # Transcribe each segment and write to the output file
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(f"--- Transcription for {file_path} ---\n")
            for segment in segments:
                print(f"Transcribing {segment}...")
                transcription = transcribe_audio_segment(segment, language)
                f.write(transcription + " ")
                
                # Optional: remove the segment file after transcription to save space
                os.remove(segment)
        
        print(f"Finished processing {file_path}. Transcription saved to {output_file_path}.")

        # Cleanup the temporary audio file if it was created
        if file_path.lower().endswith(".mp4") and os.path.exists(audio_output_path):
            try:
                os.remove(audio_output_path)
                print("Temporary audio file removed.")
            except Exception as e:
                print(f"Error removing temporary audio file: {e}")

    print("\nAll files processed. Transcriptions saved individually.")
