from setuptools import setup

APP = ['app.py']
DATA_FILES = [
    'static/dark-knight-rises-silent-nod.png',
    'static/alfred_icon.png',
    'static/alfred_icon_menu.png'
]
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,  # This makes the app a menu bar app without a dock icon
        'CFBundleName': 'Alfred Pennyworth',
        'CFBundleDisplayName': 'Alfred Pennyworth',
        'CFBundleIdentifier': 'com.alfred.pennyworth',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': 'Copyright © 2023',
        'NSHighResolutionCapable': True,
    },
    'packages': ['rumps', 'PIL'],
    'iconfile': 'static/alfred_icon.png',
}

setup(
    name='Alfred Pennyworth',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)