import pyautogui

def example_using_pyautogui():
    """
    Example method using pyautogui to move the mouse and click.
    """
    # Move the mouse to the position (100, 100)
    pyautogui.moveTo(100, 100, duration=1)
    # Click the mouse at the current position
    pyautogui.click()

# Example usage
if __name__ == "__main__":
    example_using_pyautogui()
