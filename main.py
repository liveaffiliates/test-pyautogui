import pyautogui

def example_using_pyautogui():
    """
    Example method using pyautogui to move the mouse and click.
    """
    # Move the mouse to the position (100, 100)
    pyautogui.moveTo(100, 100, duration=1)
    # Click the mouse at the current position
    pyautogui.click()
    # Take a screenshot and save it as test.png
    screenshot = pyautogui.screenshot()
    screenshot.save('test.png')
    pyautogui.click()

# Example usage
if __name__ == "__main__":
    example_using_pyautogui()
