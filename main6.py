import pyautogui
import cv2
import numpy as np
from AppKit import NSScreen
import Quartz
import os
import time
from datetime import datetime

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
    
    translated_x = int(x / scaling_factor)
    translated_y = int(y / scaling_factor)
    
    translated_x = max(0, min(translated_x, primary_bounds[0] - 1))
    translated_y = max(0, min(translated_y, primary_bounds[1] - 1))
    
    return translated_x, translated_y

def save_debug_image(image, filename, circles=None, rectangles=None):
    debug_image = image.copy()
    if circles:
        for circle in circles:
            cv2.circle(debug_image, circle[0], circle[1], circle[2], circle[3])
    if rectangles:
        for rect in rectangles:
            cv2.rectangle(debug_image, rect[0], rect[1], rect[2], rect[3])
    cv2.imwrite(filename, debug_image)
    print(f"Debug image saved: {filename}")

def detect_image(template_path, confidence=0.8, debug=True):
    start_time = time.time()
    
    print(f"Detecting image: {template_path}")
    print(f"Confidence threshold: {confidence}")
    print(f"Screen size: {pyautogui.size()}")
    print(f"Primary display bounds: {get_primary_display_bounds()}")
    print(f"Display scaling factor: {get_display_scaling_factor()}")
    
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    
    if template is None:
        raise FileNotFoundError(f"Template image not found: {template_path}")
    
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    if max_val < confidence:
        print(f"Image not found. Best match confidence: {max_val}")
        if debug:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_debug_image(screenshot, f"debug_not_found_{timestamp}.png")
        return None
    
    h, w = template.shape[:2]
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    center = (top_left[0] + w//2, top_left[1] + h//2)
    
    print(f"Image detected at: {center}")
    print(f"Match confidence: {max_val}")
    
    translated_x, translated_y = translate_coordinates(center[0], center[1])
    translated_center = (translated_x, translated_y)
    print(f"Translated coordinates: {translated_center}")
    
    if debug:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        circles = [(center, 5, (0, 0, 255), 2), (translated_center, 5, (255, 0, 0), 2)]
        rectangles = [(top_left, bottom_right, (0, 255, 0), 2)]
        save_debug_image(screenshot, f"debug_found_{timestamp}.png", circles, rectangles)
    
    end_time = time.time()
    print(f"Detection time: {end_time - start_time:.2f} seconds")
    
    return translated_center

def click_image(template_path, confidence=0.8, debug=True):
    result = detect_image(template_path, confidence, debug)
    if result:
        x, y = result
        print(f"Moving mouse to: ({x}, {y})")
        pyautogui.moveTo(x, y, duration=1)
        print("Clicking...")
        pyautogui.click()
        final_pos = pyautogui.position()
        print(f"Final mouse position: {final_pos}")
        return True
    else:
        print("Image not found. Click action not performed.")
        return False

if __name__ == "__main__":
    image_path = "extension.png"
    print("Generalized Mac Image Detection Script")
    print("--------------------------------------")
    success = click_image(image_path, confidence=0.7, debug=True)
    print(f"Operation {'successful' if success else 'failed'}.")