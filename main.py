import cv2
import pyautogui
from pyautogui import ImageNotFoundException
import pyscreeze
import numpy as np
import imutils
import os
from datetime import datetime

def save_debug_screenshot(image, boxes, filename, highlight_box=None):
    """Save a debug screenshot with bounding boxes and highlight the found image."""
    for box in boxes:
        cv2.rectangle(image, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), (0, 255, 0), 2)
    
    if highlight_box:
        cv2.rectangle(image, (highlight_box[0], highlight_box[1]), 
                      (highlight_box[0] + highlight_box[2], highlight_box[1] + highlight_box[3]), 
                      (0, 0, 255), 3)  # Red color for the found image
    
    cv2.imwrite(filename, image)

def capture_and_highlight_region(coords, size):
    """Capture the region around the found coordinates and highlight it."""
    x, y = coords
    width, height = size
    
    # Capture the full screen
    full_screenshot = pyautogui.screenshot()
    full_screenshot = cv2.cvtColor(np.array(full_screenshot), cv2.COLOR_RGB2BGR)
    
    # Define the region to capture (with some padding)
    padding = 50
    left = max(0, x - padding)
    top = max(0, y - padding)
    right = min(full_screenshot.shape[1], x + width + padding)
    bottom = min(full_screenshot.shape[0], y + height + padding)
    
    # Extract the region
    region = full_screenshot[top:bottom, left:right]
    
    # Draw a rectangle around the found image
    cv2.rectangle(region, (x - left, y - top), (x - left + width, y - top + height), (0, 0, 255), 2)
    
    # Save the highlighted region
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"found_region_{timestamp}.png"
    cv2.imwrite(filename, region)
    print(f"Region screenshot saved as {filename}")

def template_match_with_scaling(image, gs=True, confidence=0.8):
    """
    Locate an image and return a pyscreeze box surrounding it. 
    Template matching is done by default in grayscale (gs=True)
    Detect image if normalized correlation coefficient is > confidence (0.8 is default)
    """
    templateim = pyscreeze._load_cv2(image, grayscale=gs)
    (tH, tW) = templateim.shape[:2]
    screenim_color = pyautogui.screenshot()
    screenim_color = cv2.cvtColor(np.array(screenim_color), cv2.COLOR_RGB2BGR)
    
    if gs:
        screenim = cv2.cvtColor(screenim_color, cv2.COLOR_BGR2GRAY)
    else:
        screenim = screenim_color

    found = None
    scalingrange = np.linspace(0.25, 2, num=50)
    all_matches = []

    for scale in scalingrange:
        resizedtemplate = imutils.resize(templateim, width=int(templateim.shape[1] * scale))
        r = resizedtemplate.shape[1] / templateim.shape[1]
        result = cv2.matchTemplate(screenim, resizedtemplate, cv2.TM_CCOEFF_NORMED)
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
        
        if maxVal > confidence:
            all_matches.append((maxVal, maxLoc, r))
        
        if found is None or maxVal > found[0]:
            found = (maxVal, maxLoc, r)

    if found and found[0] > confidence:
        (_, maxLoc, r) = found
        box = pyscreeze.Box(int(maxLoc[0]), int(maxLoc[1]), int(tW*r), int(tH*r))
        
        # Save debug screenshot
        debug_image = screenim_color.copy()
        boxes = [box]
        for match in all_matches:
            if match[0] > confidence:
                (_, loc, r) = match
                boxes.append(pyscreeze.Box(int(loc[0]), int(loc[1]), int(tW*r), int(tH*r)))
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        debug_filename = f"debug_screenshot_{timestamp}.png"
        save_debug_screenshot(debug_image, boxes, debug_filename, highlight_box=box)
        print(f"Debug screenshot saved as {debug_filename}")
        
        return box
    else:
        return None

def locate_center_with_scaling(image, gs=True):
    print(f"Searching for image: {image}")
    loc = template_match_with_scaling(image, gs=gs)
    if loc:
        center = pyautogui.center(loc)
        print(f"Image found at center: {center}")
        
        # Capture and highlight the found region
        template = cv2.imread(image)
        capture_and_highlight_region(center, (template.shape[1], template.shape[0]))
        
        print(f"Screen size: {pyautogui.size()}")
        current_pos = pyautogui.position()
        print(f"Current mouse position before move: {current_pos}")
        
        # Calculate relative movement
        move_x = center.x - current_pos.x
        move_y = center.y - current_pos.y
        
        # Move the mouse relative to its current position
        pyautogui.moveRel(move_x, move_y, duration=3)
        final_pos = pyautogui.position()
        print(f"Final mouse position: {final_pos}")
        
        # Verify if we reached the target
        if final_pos != center:
            print(f"Warning: Final position {final_pos} doesn't match target {center}")
        
        return center
    else:
        print("Image not found")
        raise Exception("Image not found")

def example_locate_on_screen(image_path):
    """
    Example method using pyautogui to locate an image on the screen.
    """
    print(f"Looking for image: {image_path}")
    try:
        location = pyautogui.locateCenterOnScreen(image_path)
        if location:
            print(f"Image center found at: {location}")
            current_pos = pyautogui.position()
            print(f"Current mouse position before move: {current_pos}")
            
            # Calculate relative movement
            move_x = location.x - current_pos.x
            move_y = location.y - current_pos.y
            
            # Move the mouse relative to its current position
            pyautogui.moveRel(move_x, move_y, duration=3)
            final_pos = pyautogui.position()
            print(f"Mouse position after move: {final_pos}")
            
            pyautogui.click()
            print(f"Mouse position after click: {pyautogui.position()}")
        else:
            print("Image not found on the screen.")
    except ImageNotFoundException:
        print("Image not found on the screen.")

def example_using_pyautogui():
    """
    Example method using pyautogui to move the mouse and click.
    """
    # Take a screenshot and save it
    screenshot = pyautogui.screenshot()
    screenshot.save("full_screenshot.png")
    print("Full screenshot saved as full_screenshot.png")

if __name__ == "__main__":
    delay = 5
    print(f"Waiting {delay} seconds before starting the script.")
    pyautogui.sleep(delay)

    # Take a full screenshot
    example_using_pyautogui()

    # Ensure the image file exists
    image_path = "extension.png"
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found.")
    else:
        try:
            coords = locate_center_with_scaling(image_path)
            print(f"Clicking on the image at coordinates: {coords}")
            pyautogui.click()
            print(f"Mouse position after click: {pyautogui.position()}")
        except Exception as e:
            print(f"Error in locate_center_with_scaling: {str(e)}")

        print("\nTrying with pyautogui's built-in function:")
        example_locate_on_screen(image_path)

    print("Script execution completed.")