from image_detection_service import ImageDetectionService
import pyautogui

def run_demo():
    print("Image Detection Service Demo")
    print("-----------------------------")
    
    service = ImageDetectionService()
    
    # Click Share button
    image_path = "/Users/nicholasmuir/PythonProjects/test-pyautogui/share.png"
    print(f"\nTest Case: Click image with delay '{image_path}'")
    success = service.click_image_with_delay(image_path, confidence=0.8, debug=True, delay=3)
    if success:
        print("Click operation successful after delay")
    else:
        print("Click operation failed after delay")
    
    # Select entire screen
    image_path = "/Users/nicholasmuir/PythonProjects/test-pyautogui/entire_screen1.png"
    print(f"\nTest Case: Click image with delay '{image_path}'")
    success = service.click_image_with_delay(image_path, confidence=0.8, debug=True, delay=3)
    if success:
        print("Click operation successful after delay")
    else:
        print("Click operation failed after delay")
    
    # Click on screen preview
    image_path = "/Users/nicholasmuir/PythonProjects/test-pyautogui/entire_screen_preview.png"
    print(f"\nTest Case: Click image with delay '{image_path}'")
    success = service.click_image_with_delay(image_path, confidence=0.8, debug=True, delay=3)
    if success:
        print("Click operation successful after delay")
    else:
        print("Click operation failed after delay")

    # Click on share button
    image_path = "/Users/nicholasmuir/PythonProjects/test-pyautogui/share_button.png"
    print(f"\nTest Case: Click image with delay '{image_path}'")
    success = service.click_image_with_delay(image_path, confidence=0.8, debug=True, delay=3)
    if success:
        print("Click operation successful after delay")
    else:
        print("Click operation failed after delay")


if __name__ == "__main__":
    run_demo()