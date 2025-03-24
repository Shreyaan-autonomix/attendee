import logging
import os
import subprocess

logger = logging.getLogger(__name__)


class MediaRecorderReceiver:
    def __init__(self, file_location):
        self.file_location = file_location

    def cleanup(self):
        self.make_file_seekable()

    def on_encoded_mp4_chunk(self, chunk):
        # Check if file exists and open in appropriate mode
        mode = "ab" if os.path.exists(self.file_location) else "wb"

        # Write or append data to the file
        with open(self.file_location, mode) as f:
            f.write(chunk)

    def get_seekable_path(self, path):
        """
        Transform a file path to include '.seekable' before the extension.
        Example: /tmp/file.webm -> /tmp/file.seekable.webm
        """
        base, ext = os.path.splitext(path)
        return f"{base}.seekable{ext}"

    def make_file_seekable(self):
        input_path = self.file_location
        output_path = self.get_seekable_path(self.file_location)
        """Use ffmpeg to move the moov atom to the beginning of the file."""
        logger.info(f"Making file seekable: {input_path} -> {output_path}")
        # log how many bytes are in the file
        logger.info(f"File size: {os.path.getsize(input_path)} bytes")
        command = [
            "ffmpeg",
            "-i",
            str(input_path),
            "-c",
            "copy",  # Copy without re-encoding
            "-movflags",
            "+faststart",
            "-y",  # Overwrite output file without asking
            str(output_path),
        ]

        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg failed: {result.stderr}")

        # Replace the original file with the seekable version
        try:
            os.replace(str(output_path), str(input_path))
            logger.info(f"Replaced original file with seekable version: {input_path}")
        except Exception as e:
            logger.error(f"Failed to replace original file with seekable version: {e}")
            raise RuntimeError(f"Failed to replace original file: {e}")
