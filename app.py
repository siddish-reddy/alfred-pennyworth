import rumps
import os
import time
import threading
import shutil
from datetime import datetime
from PIL import ImageGrab
import subprocess

# Create a base directory to store screenshots
SCREENSHOTS_BASE_DIR = os.path.expanduser("~/alfred_sentinel/current_session/")
TIMELAPSES_BASE_DIR = os.path.expanduser("~/alfred_sentinel/timelapses_archive/")
os.makedirs(SCREENSHOTS_BASE_DIR, exist_ok=True)
os.makedirs(TIMELAPSES_BASE_DIR, exist_ok=True)

class AwesomeStatusBarApp(rumps.App):
    def __init__(self, *args, **kwargs):
        super(AwesomeStatusBarApp, self).__init__(*args, **kwargs)
        self.screenshot_timer = None
        self.is_capturing = False
        self.menu = ["Capture", "Pause", "Create Video"]
    
    @rumps.clicked("Capture")
    def start_capturing(self, sender):
        if not self.is_capturing:
            self.is_capturing = True
            sender.state = self.is_capturing
            rumps.notification("Alfred", "Screenshot Capture", "Started capturing screenshots every 30 seconds")
            self.screenshot_timer = threading.Thread(target=self.capture_screenshots)
            self.screenshot_timer.daemon = True
            self.screenshot_timer.start()
    
    @rumps.clicked("Pause")
    def stop_capturing(self, sender):
        if self.is_capturing:
            self.is_capturing = False
            sender.state = self.is_capturing
            rumps.notification("Alfred", "Screenshot Capture", "Stopped capturing screenshots")
    
    def capture_screenshots(self):
        while self.is_capturing:
            try:
                # Take a screenshot
                screenshot = ImageGrab.grab()
                
                # Get current date for folder organization
                current_date = datetime.now().strftime("%Y%m%d")
                screenshots_dir = os.path.join(SCREENSHOTS_BASE_DIR, current_date)
                
                # Create date folder if it doesn't exist
                os.makedirs(screenshots_dir, exist_ok=True)
                
                # Generate a filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(screenshots_dir, f"screenshot_{timestamp}.png")
                
                # Save the screenshot
                screenshot.save(filename)
                
                # Wait for 30 seconds
                for _ in range(20):
                    if not self.is_capturing:
                        break
                    time.sleep(1)
            except Exception as e:
                rumps.notification("Alfred", "Error", f"Failed to capture screenshot: {str(e)}")
                self.is_capturing = False
    
    @rumps.clicked("Create Video")
    def create_video(self, _):
        try:
            # Get list of date folders
            date_folders = [f for f in os.listdir(SCREENSHOTS_BASE_DIR) 
                           if os.path.isdir(os.path.join(SCREENSHOTS_BASE_DIR, f))]
            
            if not date_folders:
                rumps.alert("No screenshots", "No screenshots found to create a video.")
                return
            
            # Process each date folder
            for date_folder in date_folders:
                folder_path = os.path.join(SCREENSHOTS_BASE_DIR, date_folder)
                screenshots = [f for f in os.listdir(folder_path) if f.endswith('.png')]
                
                if not screenshots:
                    continue
                
                # Sort screenshots by name (which includes timestamp)
                screenshots.sort()
                
                # Extract first and last screenshot times for the filename
                first_time = screenshots[0].replace("screenshot_", "").replace(".png", "")
                last_time = screenshots[-1].replace("screenshot_", "").replace(".png", "")
                
                # Create output video filename with time range
                output_video = os.path.join(
                    TIMELAPSES_BASE_DIR, 
                    f"timelapse_{date_folder}_{first_time}_to_{last_time}.mp4"
                )
                
                # Use ffmpeg to create a video
                cmd = [
                    "ffmpeg",
                    "-framerate", "1",
                    "-pattern_type", "glob",
                    "-i", f"{folder_path}/screenshot_*.png",
                    "-c:v", "libx264",
                    "-pix_fmt", "yuv420p",
                    output_video
                ]
                
                # Run the command in a separate thread to avoid blocking the UI
                threading.Thread(
                    target=self._run_ffmpeg, 
                    args=(cmd, output_video, folder_path)
                ).start()
                
                rumps.notification(
                    "Alfred", 
                    "Video Creation", 
                    f"Started creating video from screenshots for {date_folder}"
                )
        except Exception as e:
            rumps.alert("Error", f"Failed to create video: {str(e)}")
    
    def _run_ffmpeg(self, cmd, output_path, screenshots_folder):
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            
            # Verify the video file exists and has size > 0
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                # Delete the screenshots after successful video creation
                shutil.rmtree(screenshots_folder)
                
                rumps.notification(
                    "Alfred", 
                    "Video Creation", 
                    f"Video created successfully at {output_path}\nScreenshots have been deleted."
                )
            else:
                rumps.notification(
                    "Alfred", 
                    "Warning", 
                    f"Video may not have been created properly. Screenshots were not deleted."
                )
        except subprocess.CalledProcessError as e:
            rumps.notification(
                "Alfred", 
                "Error", 
                f"Failed to create video: {e.stderr.decode()}"
            )

if __name__ == "__main__":
    app = AwesomeStatusBarApp("🎩", "Alfred Pennyworth")
    # Set custom icon
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/alfred_icon_menu.png")
    if os.path.exists(icon_path):
        app.icon = icon_path
    app.run()