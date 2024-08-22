import cv2
import pyautogui
import numpy as np
import time
import os

def save_debug_image(x, y, filename):
    """Save a debug image with a marker at the specified location."""
    screenshot = pyautogui.screenshot()
    img = np.array(screenshot)
    cv2.circle(img, (x, y), 20, (0, 0, 255), -1)
    cv2.imwrite(filename, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    print(f"Debug image saved as {filename}")

def locate_and_diagnose(image_path):
    print(f"Searching for image: {image_path}")
    
    # Step 1: Detect the image
    location = pyautogui.locateOnScreen(image_path)
    if location:
        center = pyautogui.center(location)
        print(f"Image found at: {center}")
        
        # Step 2: Save a debug image
        debug_filename = "debug_detected_location.png"
        save_debug_image(center.x, center.y, debug_filename)
        print(f"Please check {debug_filename} to verify the detected location.")
        
        # Step 3: Compare actual vs. reported mouse positions
        print("Moving mouse to detected location...")
        current_pos = pyautogui.position()
        print(f"Starting mouse position: {current_pos}")
        
        pyautogui.moveTo(center.x, center.y, duration=2)
        time.sleep(1)  # Wait a moment for any animations to settle
        
        new_pos = pyautogui.position()
        print(f"Ending mouse position: {new_pos}")
        print(f"Intended position: {center}")
        
        if new_pos != center:
            print(f"Discrepancy detected!")
            print(f"X offset: {new_pos.x - center.x}")
            print(f"Y offset: {new_pos.y - center.y}")
        
        # Save another debug image for the final mouse position
        final_debug_filename = "debug_final_mouse_position.png"
        save_debug_image(new_pos.x, new_pos.y, final_debug_filename)
        print(f"Please check {final_debug_filename} to verify the final mouse position.")
        
    else:
        print("Image not found on the screen.")

if __name__ == "__main__":
    image_path = "extension.png"
    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found. Please ensure the image file is in the same directory as this script.")
    else:
        locate_and_diagnose(image_path)
        print("Diagnosis complete. Please check the saved debug images.")