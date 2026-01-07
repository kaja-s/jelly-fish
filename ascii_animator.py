#!/usr/bin/env python3
"""
ASCII Animation Generator and Player
Converts video frames to ASCII art and plays them as an animation
"""

import os
import sys
import time
from PIL import Image

# ASCII characters from darkest to lightest
ASCII_CHARS = "@%#*+=-:. "

def resize_image(image, new_width=100):
    """Resize image maintaining aspect ratio"""
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio * 0.55)  # 0.55 to account for character height
    return image.resize((new_width, new_height))

def grayscale(image):
    """Convert image to grayscale"""
    return image.convert("L")

def pixels_to_ascii(image):
    """Convert grayscale pixels to ASCII characters"""
    pixels = image.getdata()
    ascii_str = ""
    for pixel in pixels:
        ascii_str += ASCII_CHARS[pixel * len(ASCII_CHARS) // 256]
    return ascii_str

def image_to_ascii(image_path, width=100):
    """Convert an image file to ASCII art"""
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Error opening {image_path}: {e}")
        return None

    image = resize_image(image, width)
    image = grayscale(image)

    ascii_str = pixels_to_ascii(image)
    img_width = image.width

    # Split string into lines
    ascii_lines = [ascii_str[i:i + img_width] for i in range(0, len(ascii_str), img_width)]
    return "\n".join(ascii_lines)

def convert_frames_to_ascii(frames_dir, output_dir, width=100):
    """Convert all frames to ASCII and save them"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    frames = sorted([f for f in os.listdir(frames_dir) if f.endswith('.png')])

    print(f"Converting {len(frames)} frames to ASCII art...")
    for i, frame in enumerate(frames, 1):
        frame_path = os.path.join(frames_dir, frame)
        ascii_art = image_to_ascii(frame_path, width)

        if ascii_art:
            output_file = os.path.join(output_dir, frame.replace('.png', '.txt'))
            with open(output_file, 'w') as f:
                f.write(ascii_art)

        if i % 10 == 0:
            print(f"  Processed {i}/{len(frames)} frames")

    print(f"Done! ASCII frames saved to {output_dir}")

def play_animation(ascii_dir, fps=24, loop=True):
    """Play ASCII animation from saved frames"""
    frames = sorted([f for f in os.listdir(ascii_dir) if f.endswith('.txt')])

    if not frames:
        print(f"No ASCII frames found in {ascii_dir}")
        return

    frame_delay = 1.0 / fps

    print(f"Playing animation with {len(frames)} frames at {fps} FPS")
    print("Press Ctrl+C to stop\n")
    time.sleep(1)

    try:
        iteration = 0
        while True:
            for frame in frames:
                frame_path = os.path.join(ascii_dir, frame)
                with open(frame_path, 'r') as f:
                    ascii_art = f.read()

                # Clear screen and display frame
                os.system('clear' if os.name != 'nt' else 'cls')
                print(ascii_art)
                print(f"\nFrame: {frames.index(frame) + 1}/{len(frames)} | Loop: {iteration + 1}")

                time.sleep(frame_delay)

            iteration += 1
            if not loop:
                break

    except KeyboardInterrupt:
        print("\n\nAnimation stopped!")

def main():
    frames_dir = "/Users/kajaskerlj/Dev/jelly-fish/frames"
    ascii_dir = "/Users/kajaskerlj/Dev/jelly-fish/ascii_frames"

    # Check if ASCII frames already exist
    if not os.path.exists(ascii_dir) or not os.listdir(ascii_dir):
        print("Converting frames to ASCII art...")
        convert_frames_to_ascii(frames_dir, ascii_dir, width=80)
    else:
        print(f"ASCII frames already exist in {ascii_dir}")

    print("\nStarting animation...\n")
    time.sleep(1)
    play_animation(ascii_dir, fps=24, loop=True)

if __name__ == "__main__":
    main()
