import cv2
import numpy as np

def find_and_click_button(template_path, screenshot_path):
    # Load images
    template = cv2.imread(template_path, 0)  # Template image of the button
    screenshot = cv2.imread(screenshot_path, 0)  # Screenshot to search in
    
    # Template matching
    res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # Adjust threshold according to your needs
    loc = np.where(res >= threshold)
    
    if np.any(loc[0]):  # If there's at least one match
        # Get the first match's top-left corner (multiple matches possible)
        top_left = list(zip(*loc[::-1]))[0]
        # Calculate the center of the button
        button_center = (top_left[0] + template.shape[1]//2, top_left[1] + template.shape[0]//2)
        
        # Simulate click at button_center (this part depends on how you simulate clicks)
        print(f"Clicking at: {button_center}")
        # click_button(button_center)  # Assuming you have a function to simulate the click
    else:
        print("Button not found.")

# Example usage
find_and_click_button("path/to/button_image.png", "path/to/screenshot.png")