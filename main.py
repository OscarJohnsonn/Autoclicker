import pyautogui
import cv2
import numpy as np
import os

def take_screenshot(save_path):
    # Take a screenshot using pyautogui
    screenshot = pyautogui.screenshot()
    
    # Save the screenshot to the specified path
    screenshot.save(save_path)
    
    # Convert to OpenCV format
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return screenshot_cv

def find_button(screenshot, button_image_path):
    # Load the button image using OpenCV
    button_image = cv2.imread(button_image_path, cv2.IMREAD_COLOR)
    
    # Perform template matching to find the button
    result = cv2.matchTemplate(screenshot, button_image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    # Define a threshold to determine if the button is found
    threshold = 0.8
    if max_val >= threshold:
        button_height, button_width, _ = button_image.shape
        top_left = max_loc
        bottom_right = (top_left[0] + button_width, top_left[1] + button_height)
        
        # Draw rectangle around the matched region
        cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)
        
        # Debugging information
        print(f'Match found with max value: {max_val}')
        print(f'Top left corner: {top_left}')
        print(f'Bottom right corner: {bottom_right}')
        
        # Return the top-left corner and dimensions of the matched region
        return top_left, button_width, button_height
    else:
        print(f'No match found, max value: {max_val}')
        return None, None, None

def click_button(button_location, button_width, button_height):
    # Calculate the center of the button
    button_center_x = button_location[0] + button_width // 2
    button_center_y = button_location[1] + button_height // 2
    
    # Print the coordinates for debugging
    print(f'Clicking at: ({button_center_x}, {button_center_y})')
    
    # Move the mouse to the center of the button and click
    pyautogui.moveTo(button_center_x, button_center_y)
    pyautogui.click()

# Create the screenshot directory if it doesn't exist
if not os.path.exists('screenshot'):
    os.makedirs('screenshot')

# Get screen resolution
screen_width, screen_height = pyautogui.size()
print(f'Screen resolution: {screen_width}x{screen_height}')

# Define the path to your button image
button_image_path = 'image.png'

# Define the path to save the screenshot
screenshot_path = 'screenshot/screenshot.png'

# Take a screenshot of the screen and save it
screenshot = take_screenshot(screenshot_path)

# Find the button on the screen
button_location, button_width, button_height = find_button(screenshot, button_image_path)

# Save the annotated screenshot
annotated_screenshot_path = 'screenshot/annotated_screenshot.png'
cv2.imwrite(annotated_screenshot_path, screenshot)

if button_location:
    print(f'Button found at location: {button_location}')
    # Click the button
    click_button(button_location, button_width, button_height)
else:
    print('Button not found on the screen.')
