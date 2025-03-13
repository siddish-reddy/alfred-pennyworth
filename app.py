import rumps
import os
import time
import threading
import shutil
import base64
import json
import requests
from datetime import datetime
from PIL import ImageGrab
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get OpenRouter API key from environment variables
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Create a base directory to store screenshots
SCREENSHOTS_BASE_DIR = os.path.expanduser("~/alfred_sentinel/current_session/")
TIMELAPSES_BASE_DIR = os.path.expanduser("~/alfred_sentinel/timelapses_archive/")
os.makedirs(SCREENSHOTS_BASE_DIR, exist_ok=True)
os.makedirs(TIMELAPSES_BASE_DIR, exist_ok=True)

# Gemini API constants
DISTRACTION_CHECK_INTERVAL = 180  # 3 minutes in seconds
CONTINUED_DISTRACTION_CHECK_INTERVAL = 20  # 20 seconds

def encode_image_to_base64(image_path):
    """Convert an image to base64 encoding"""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error encoding image: {str(e)}")
        return None

def check_distraction_with_gemini(image_path):
    """
    Call Gemini API via OpenRouter to check if the user is distracted
    Returns True if distracted, False otherwise
    """
    if not OPENROUTER_API_KEY:
        rumps.notification("Alfred", "API Key Missing", "Please set OPENROUTER_API_KEY in your environment variables")
        return False
    
    try:
        # Encode the image to base64
        base64_image = encode_image_to_base64(image_path)
        if not base64_image:
            return False
        
        # Prepare the API request
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "alfred-pennyworth-app",
            "X-Title": "Alfred Pennyworth"
        }
        
        data = {
            "model": "google/gemini-2.0-flash-lite-preview-02-05:free",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze this screenshot of my computer screen. Am I distracted or not focused on productive work? Look for signs like social media, entertainment websites, games, or non-work related content. Only respond with 'DISTRACTED' or 'FOCUSED', nothing else."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
        }
        
        # Make the API request
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"].strip()
            return "DISTRACTED" in content.upper()
        else:
            print(f"API request failed with status code {response.status_code}: {response.text}")
            return False
    
    except Exception as e:
        print(f"Error checking distraction: {str(e)}")
        return False

class AwesomeStatusBarApp(rumps.App):
    def __init__(self, *args, **kwargs):
        super(AwesomeStatusBarApp, self).__init__(*args, **kwargs)
        self.screenshot_timer = None
        self.distraction_timer = None
        self.continued_distraction_timer = None
        self.is_capturing = False
        self.is_distracted = False
        self.menu = ["Capture", "Pause", "Create Video", "Check Distraction Now"]
    
    @rumps.clicked("Capture")
    def start_capturing(self, sender):
        if not self.is_capturing:
            self.is_capturing = True
            sender.state = self.is_capturing
            rumps.notification("Alfred", "Screenshot Capture", "Started capturing screenshots every 30 seconds")
            self.screenshot_timer = threading.Thread(target=self.capture_screenshots)
            self.screenshot_timer.daemon = True
            self.screenshot_timer.start()
            
            # Start the distraction check timer
            self.start_distraction_check()
    
    @rumps.clicked("Pause")
    def stop_capturing(self, sender):
        if self.is_capturing:
            self.is_capturing = False
            sender.state = self.is_capturing
            rumps.notification("Alfred", "Screenshot Capture", "Stopped capturing screenshots")
            
            # Stop the distraction check timers
            self.stop_distraction_check()
    
    @rumps.clicked("Check Distraction Now")
    def check_distraction_now(self, _):
        """Manually check for distraction using the latest screenshot"""
        if not self.is_capturing:
            rumps.notification("Alfred", "Not Capturing", "Start capturing first to check for distraction")
            return
        
        # Take a screenshot for immediate checking
        screenshot = ImageGrab.grab()
        current_date = datetime.now().strftime("%Y%m%d")
        screenshots_dir = os.path.join(SCREENSHOTS_BASE_DIR, current_date)
        os.makedirs(screenshots_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(screenshots_dir, f"screenshot_{timestamp}.png")
        screenshot.save(filename)
        
        # Check for distraction
        threading.Thread(target=self.check_distraction, args=(filename,)).start()
    
    def start_distraction_check(self):
        """Start the timer to check for distraction every 3 minutes"""
        self.distraction_timer = threading.Timer(DISTRACTION_CHECK_INTERVAL, self.distraction_check_callback)
        self.distraction_timer.daemon = True
        self.distraction_timer.start()
    
    def stop_distraction_check(self):
        """Stop all distraction check timers"""
        if self.distraction_timer:
            self.distraction_timer.cancel()
            self.distraction_timer = None
        
        if self.continued_distraction_timer:
            self.continued_distraction_timer.cancel()
            self.continued_distraction_timer = None
    
    def distraction_check_callback(self):
        """Callback for the distraction check timer"""
        if not self.is_capturing:
            return
        
        # Get the latest screenshot
        current_date = datetime.now().strftime("%Y%m%d")
        screenshots_dir = os.path.join(SCREENSHOTS_BASE_DIR, current_date)
        
        if not os.path.exists(screenshots_dir):
            # No screenshots yet, restart the timer
            self.distraction_timer = threading.Timer(DISTRACTION_CHECK_INTERVAL, self.distraction_check_callback)
            self.distraction_timer.daemon = True
            self.distraction_timer.start()
            return
        
        # Get the latest screenshot
        screenshots = [f for f in os.listdir(screenshots_dir) if f.endswith('.png')]
        if not screenshots:
            # No screenshots yet, restart the timer
            self.distraction_timer = threading.Timer(DISTRACTION_CHECK_INTERVAL, self.distraction_check_callback)
            self.distraction_timer.daemon = True
            self.distraction_timer.start()
            return
        
        screenshots.sort()
        latest_screenshot = os.path.join(screenshots_dir, screenshots[-1])
        
        # Check for distraction in a separate thread
        threading.Thread(target=self.check_distraction, args=(latest_screenshot,)).start()
        
        # Restart the timer
        self.distraction_timer = threading.Timer(DISTRACTION_CHECK_INTERVAL, self.distraction_check_callback)
        self.distraction_timer.daemon = True
        self.distraction_timer.start()
    
    def continued_distraction_check_callback(self):
        """Callback for the continued distraction check timer (every 20 seconds)"""
        if not self.is_capturing or not self.is_distracted:
            return
        
        # Get the latest screenshot
        current_date = datetime.now().strftime("%Y%m%d")
        screenshots_dir = os.path.join(SCREENSHOTS_BASE_DIR, current_date)
        
        if not os.path.exists(screenshots_dir):
            return
        
        # Get the latest screenshot
        screenshots = [f for f in os.listdir(screenshots_dir) if f.endswith('.png')]
        if not screenshots:
            return
        
        screenshots.sort()
        latest_screenshot = os.path.join(screenshots_dir, screenshots[-1])
        
        # Check for continued distraction in a separate thread
        threading.Thread(target=self.check_continued_distraction, args=(latest_screenshot,)).start()
    
    def check_distraction(self, screenshot_path):
        """Check if the user is distracted using the Gemini API"""
        is_distracted = check_distraction_with_gemini(screenshot_path)
        
        if is_distracted and not self.is_distracted:
            # User just became distracted
            self.is_distracted = True
            rumps.notification(
                "Alfred", 
                "Distraction Detected", 
                "You appear to be distracted. Let's get back to work!"
            )
            
            # Start the continued distraction check timer
            self.continued_distraction_timer = threading.Timer(
                CONTINUED_DISTRACTION_CHECK_INTERVAL, 
                self.continued_distraction_check_callback
            )
            self.continued_distraction_timer.daemon = True
            self.continued_distraction_timer.start()
    
    def check_continued_distraction(self, screenshot_path):
        """Check if the user is still distracted"""
        is_still_distracted = check_distraction_with_gemini(screenshot_path)
        
        if is_still_distracted:
            # User is still distracted
            rumps.notification(
                "Alfred", 
                "Still Distracted", 
                "You're still distracted. Let's refocus on our work!"
            )
            
            # Restart the continued distraction check timer
            self.continued_distraction_timer = threading.Timer(
                CONTINUED_DISTRACTION_CHECK_INTERVAL, 
                self.continued_distraction_check_callback
            )
            self.continued_distraction_timer.daemon = True
            self.continued_distraction_timer.start()
        else:
            # User is no longer distracted
            self.is_distracted = False
            rumps.notification(
                "Alfred", 
                "Back on Track", 
                "Great! You're focused again."
            )
    
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
    AwesomeStatusBarApp("👀").run()