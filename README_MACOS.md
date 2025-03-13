# Alfred Pennyworth - macOS App

This document provides instructions on how to build and run Alfred Pennyworth as a macOS application.

## Prerequisites

- macOS 15 or later
- Python 3.8 or later
- pip (Python package manager)

## Building the App

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Build the macOS app using py2app:

```bash
python setup.py py2app
```

This will create a standalone macOS application in the `dist` folder.

## Running the App

After building, you can run the app in one of the following ways:

1. Open Finder, navigate to the `dist` folder, and double-click on `Alfred Pennyworth.app`

2. Or run from the terminal:

```bash
open dist/Alfred\ Pennyworth.app
```

## Features

- Takes screenshots every 30 seconds
- Saves screenshots to `~/alfred_sentinel/current_session/`
- Creates timelapse videos from screenshots
- Uses Gemini API to detect when you're distracted
- Sends notifications to help you stay focused

## Configuration

The app stores its configuration in `~/alfred_sentinel/config/config.json`. You can configure:

- Gemini API key (required for distraction detection)
- Distraction check interval (default: 3 minutes)
- Distraction follow-up interval (default: 20 seconds)

## Troubleshooting

- If the app doesn't appear in the menu bar, check the system logs for errors
- Make sure you have a valid Gemini API key if you want to use the distraction detection feature
- Ensure ffmpeg is installed if you want to create timelapse videos

## Uninstalling

To uninstall the app, simply delete the application from your Applications folder and remove the configuration directory:

```bash
rm -rf ~/alfred_sentinel
```