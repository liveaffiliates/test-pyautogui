import pyautogui
import time

def verify_coordinates():
    print("Screen size:", pyautogui.size())
    print("Current mouse position:", pyautogui.position())
    
    input("Move your mouse to the extension icon and press Enter...")
    icon_pos = pyautogui.position()
    print("Extension icon position:", icon_pos)
    
    input("Press Enter to move the mouse to (100, 100)...")
    pyautogui.moveTo(100, 100, duration=2)
    time.sleep(1)
    print("Mouse position after move:", pyautogui.position())
    
    input("Press Enter to move the mouse to the previously recorded icon position...")
    pyautogui.moveTo(icon_pos.x, icon_pos.y, duration=2)
    time.sleep(1)
    print("Final mouse position:", pyautogui.position())

if __name__ == "__main__":
    print("Coordinate Verification Script")
    print("------------------------------")
    verify_coordinates()
    print("Verification complete.")