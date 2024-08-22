import pyautogui
import cv2
import numpy as np
from AppKit import NSScreen, NSWorkspace
import Quartz
import os
import time
from datetime import datetime
import argparse

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

def get_active_window_info():
    workspace = NSWorkspace.sharedWorkspace()
    active_app = workspace.activeApplication()
    app_name = active_app['NSApplicationName']
    return app_name

def get_window_bounds(app_name):
    workspace = NSWorkspace.sharedWorkspace()
    running_apps = workspace.runningApplications()
    for app in running_apps:
        if app.localizedName() == app_name:
            pid = app.processIdentifier()
            options = Quartz.kCGWindowListOptionOnScreenOnly | Quartz.kCGWindowListExcludeDesktopElements
            window_list = Quartz.CGWindowListCopyWindowInfo(options, Quartz.kCGNullWindowID)
            for window in window_list:
                if window['kCGWindowOwnerPID'] == pid:
                    bounds = window['kCGWindowBounds']
                    return (bounds['X'], bounds['Y'], bounds['Width'], bounds['Height'])
    return None

def translate_coordinates(x, y, app_name):
    scaling_factor = get_display_scaling_factor()
    primary_bounds = get_primary_display_bounds()
    window_bounds = get_window_bounds(app_name)
    screen_size = pyautogui.size()
    
    print(f"Raw coordinates: ({x}, {y})")
    print(f"Scaling factor: {scaling_factor}")
    print(f"Primary bounds: {primary_bounds}")
    print(f"Window bounds: {window_bounds}")
    print(f"Screen size: {screen_size}")
    
    if "chrome" in app_name.lower() or "firefox" in app_name.lower() or "safari" in app_name.lower():
        if window_bounds:
            # Adjust coordinates relative to window position and content area
            content_x = x - window_bounds[0]
            content_y = y - window_bounds[1]
            translated_x = int(content_x / scaling_factor) + int(window_bounds[0])
            translated_y = int(content_y / scaling_factor) + int(window_bounds[1])
        else:
            print("Warning: Unable to get window bounds for browser.")
            translated_x = int(x / scaling_factor)
            translated_y = int(y / scaling_factor)
    else:
        translated_x = int(x / scaling_factor)
        translated_y = int(y / scaling_factor)
    
    translated_x = max(0, min(translated_x, screen_size.width - 1))
    translated_y = max(0, min(translated_y, screen_size.height - 1))
    
    print(f"Translated coordinates: ({translated_x}, {translated_y})")
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
    
    app_name = get_active_window_info()
    print(f"Active application: {app_name}")
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
    
    translated_x, translated_y = translate_coordinates(center[0], center[1], app_name)
    translated_center = (translated_x, translated_y)
    
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
        print(f"Target click coordinates: ({x}, {y})")
        current_pos = pyautogui.position()
        print(f"Current mouse position: {current_pos}")
        pyautogui.moveTo(x, y, duration=1)
        time.sleep(0.5)  # Short pause to ensure the move is complete
        intermediate_pos = pyautogui.position()
        print(f"Intermediate mouse position: {intermediate_pos}")
        pyautogui.click()
        time.sleep(0.5)  # Short pause to ensure the click is complete
        final_pos = pyautogui.position()
        print(f"Final mouse position: {final_pos}")
        
        if final_pos != (x, y):
            print(f"Warning: Final position {final_pos} doesn't match target {(x, y)}")
        
        return True
    else:
        print("Image not found. Click action not performed.")
        return False

def detect_image_with_delay(template_path, confidence=0.8, debug=True, delay=0):
    if delay > 0:
        print(f"Waiting for {delay} seconds before starting detection...")
        time.sleep(delay)
    return detect_image(template_path, confidence, debug)

def click_image_with_delay(template_path, confidence=0.8, debug=True, delay=0):
    if delay > 0:
        print(f"Waiting for {delay} seconds before starting detection...")
        time.sleep(delay)
    return click_image(template_path, confidence, debug)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect and click on an image on the screen.")
    parser.add_argument("image_path", nargs="?", help="Path to the image file to detect")
    parser.add_argument("--confidence", type=float, default=0.8, help="Confidence threshold for image detection (0.0 to 1.0)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--click", action="store_true", help="Click on the detected image")
    parser.add_argument("--delay", type=int, default=0, help="Delay in seconds before starting detection")
    
    args = parser.parse_args()
    
    print("Advanced Chrome Debug Image Detection Script")
    print("---------------------------------------------")
    
    if args.image_path:
        if args.click:
            success = click_image_with_delay(args.image_path, confidence=args.confidence, debug=args.debug, delay=args.delay)
            print(f"Click operation {'successful' if success else 'failed'}.")
        else:
            result = detect_image_with_delay(args.image_path, confidence=args.confidence, debug=args.debug, delay=args.delay)
            if result:
                print(f"Image detected at: {result}")
            else:
                print("Image not detected.")
    else:
        parser.print_help()