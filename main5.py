import pyautogui
import cv2
import numpy as np
from AppKit import NSScreen
import Quartz

def get_display_scaling_factor():
    main_screen = NSScreen.mainScreen()
    scaling_factor = main_screen.backingScaleFactor()
    return scaling_factor

def get_primary_display_bounds():
    displays = Quartz.CGDisplayCopyAllDisplayModes(Quartz.CGMainDisplayID(), None)
    main_display = displays[0]
    width = Quartz.CGDisplayModeGetWidth(main_display)
    height = Quartz.CGDisplayModeGetHeight(main_display)
    return (width, height)

def translate_coordinates(x, y):
    scaling_factor = get_display_scaling_factor()
    primary_bounds = get_primary_display_bounds()
    
    # Adjust coordinates based on scaling factor and primary display bounds
    translated_x = int(x / scaling_factor)
    translated_y = int(y / scaling_factor)
    
    # Ensure coordinates are within the primary display bounds
    translated_x = max(0, min(translated_x, primary_bounds[0] - 1))
    translated_y = max(0, min(translated_y, primary_bounds[1] - 1))
    
    return translated_x, translated_y

def debug_image_detection(image_path):
    print("Detected screen size:", pyautogui.size())
    print("Primary display bounds:", get_primary_display_bounds())
    print("Display scaling factor:", get_display_scaling_factor())
    
    # Perform image detection
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    template = cv2.imread(image_path, cv2.IMREAD_COLOR)
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    top_left = max_loc
    h, w = template.shape[:2]
    bottom_right = (top_left[0] + w, top_left[1] + h)
    center = (top_left[0] + w//2, top_left[1] + h//2)
    
    print(f"Image detected at: {center}")
    
    # Translate coordinates
    translated_x, translated_y = translate_coordinates(center[0], center[1])
    translated_center = (translated_x, translated_y)
    print(f"Translated coordinates: {translated_center}")
    
    # Move mouse to translated coordinates
    pyautogui.moveTo(translated_x, translated_y, duration=2)
    
    # Verify final position
    final_pos = pyautogui.position()
    print(f"Final mouse position: {final_pos}")

if __name__ == "__main__":
    image_path = "extension.png"
    print("Mac-Specific Coordinate Fix Script")
    print("-----------------------------------")
    debug_image_detection(image_path)
    print("Debug complete.")