import pyautogui
import cv2
import numpy as np

def debug_image_detection(image_path):
    print("Screen size:", pyautogui.size())
    
    input(f"Move your mouse to the {image_path} icon and press Enter...")
    manual_pos = pyautogui.position()
    print("Manually selected position:", manual_pos)
    
    print(f"Searching for image: {image_path}")
    try:
        # Capture the entire screen
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        # Load the template image
        template = cv2.imread(image_path, cv2.IMREAD_COLOR)
        
        # Perform template matching
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        top_left = max_loc
        h, w = template.shape[:2]
        bottom_right = (top_left[0] + w, top_left[1] + h)
        center = (top_left[0] + w//2, top_left[1] + h//2)
        
        print(f"Image detected at: {center}")
        
        # Draw rectangle and center point on the screenshot
        cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)
        cv2.circle(screenshot, center, 5, (0, 0, 255), -1)
        cv2.circle(screenshot, (manual_pos.x, manual_pos.y), 5, (255, 0, 0), -1)
        
        # Save the debug image
        debug_image_path = "debug_detection.png"
        cv2.imwrite(debug_image_path, screenshot)
        print(f"Debug image saved as {debug_image_path}")
        
        print("\nComparing with manual position:")
        print(f"X difference: {center[0] - manual_pos.x}")
        print(f"Y difference: {center[1] - manual_pos.y}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    image_path = "extension.png"
    print("Coordinate Translation Debug Script")
    print("-----------------------------------")
    debug_image_detection(image_path)
    print("Debug complete. Please check the debug_detection.png image.")