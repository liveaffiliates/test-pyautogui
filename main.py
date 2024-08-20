import pyautogui
from pyautogui import ImageNotFoundException

def example_using_pyautogui():
    """
    Example method using pyautogui to move the mouse and click.
    """
    # Move the mouse to the position (100, 100)
    pyautogui.moveTo(100, 100, duration=1)
    # Take a screenshot and save it as test.png
    screenshot = pyautogui.screenshot()
    screenshot.save('test.png')

def example_locate_on_screen(image_path):
    """
    Example method using pyautogui to locate an image on the screen.
    """
    try:
        location = pyautogui.locateOnScreen(image_path)
        if location:
            print(f"Image found at: {location}")
        else:
            print("Image not found on the screen.")
    except ImageNotFoundException:
        print("Image not found on the screen.")

if __name__ == "__main__":
    example_using_pyautogui()
    example_locate_on_screen('test.png')  # Replace 'test.png' with the path to your image file
