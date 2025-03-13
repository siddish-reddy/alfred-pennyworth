"""
This script generates a custom icon for the Alfred Pennyworth app.
It creates a simple icon that can be used in the menu bar.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(output_path, size=(512, 512)):
    """Create a custom icon for Alfred Pennyworth"""
    # Create a new image with a transparent background
    img = Image.new('RGBA', size, color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a butler silhouette (simplified as a bow tie)
    # Background circle
    circle_radius = size[0] // 2 - 10
    circle_center = (size[0] // 2, size[1] // 2)
    draw.ellipse(
        (
            circle_center[0] - circle_radius,
            circle_center[1] - circle_radius,
            circle_center[0] + circle_radius,
            circle_center[1] + circle_radius
        ),
        fill=(40, 40, 40, 255)
    )
    
    # Draw bow tie
    bow_tie_width = size[0] // 3
    bow_tie_height = size[1] // 6
    bow_tie_center = (size[0] // 2, size[1] // 2)
    
    # Left triangle
    left_triangle = [
        (bow_tie_center[0] - bow_tie_width // 2, bow_tie_center[1]),
        (bow_tie_center[0], bow_tie_center[1] - bow_tie_height // 2),
        (bow_tie_center[0], bow_tie_center[1] + bow_tie_height // 2),
    ]
    draw.polygon(left_triangle, fill=(0, 0, 0, 255))
    
    # Right triangle
    right_triangle = [
        (bow_tie_center[0] + bow_tie_width // 2, bow_tie_center[1]),
        (bow_tie_center[0], bow_tie_center[1] - bow_tie_height // 2),
        (bow_tie_center[0], bow_tie_center[1] + bow_tie_height // 2),
    ]
    draw.polygon(right_triangle, fill=(0, 0, 0, 255))
    
    # Center rectangle
    center_rect = [
        (bow_tie_center[0] - 10, bow_tie_center[1] - 10),
        (bow_tie_center[0] + 10, bow_tie_center[1] + 10),
    ]
    draw.rectangle(center_rect, fill=(0, 0, 0, 255))
    
    # Add a white outline
    draw.ellipse(
        (
            circle_center[0] - circle_radius,
            circle_center[1] - circle_radius,
            circle_center[0] + circle_radius,
            circle_center[1] + circle_radius
        ),
        outline=(255, 255, 255, 255),
        width=3
    )
    
    # Save the image
    img.save(output_path)
    
    # Create a smaller version for menu bar (16x16)
    menu_bar_size = (16, 16)
    menu_bar_img = img.resize(menu_bar_size, Image.LANCZOS)
    menu_bar_path = os.path.splitext(output_path)[0] + "_menu.png"
    menu_bar_img.save(menu_bar_path)
    
    return output_path, menu_bar_path

if __name__ == "__main__":
    # Create the static directory if it doesn't exist
    os.makedirs("static", exist_ok=True)
    
    # Generate the icon
    icon_path, menu_icon_path = create_icon("static/alfred_icon.png")
    print(f"Icon created at: {icon_path}")
    print(f"Menu bar icon created at: {menu_icon_path}")