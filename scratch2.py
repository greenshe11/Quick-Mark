import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

def match_template(target, template, template_size):
    #mult = template.shape[0]/template_size[0]
    #print(template_size)
    #template_size = [int(x*mult) for x in template.shape[:2]]
    #print("SOZE")
    #print(template_size)
    template = cv2.resize(template, template_size)
    # Convert both images to grayscale
    main_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # Perform template matching
    result = cv2.matchTemplate(main_gray, template_gray, cv2.TM_CCOEFF_NORMED)

    # Find the maximum correlation value
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(max_val)
    # Get the coordinates of the top-left corner of the matched region
    top_left = max_loc

    # Get the coordinates of the bottom-right corner of the matched region
    bottom_right = (top_left[0] + template_gray.shape[1], top_left[1] + template_gray.shape[0])
    #return max_val
    # Draw a rectangle around the matched region on the main image
    #cv2.rectangle(main_image, top_left, bottom_right, (0, 255, 0), 2)
    #plt.imshow(main_image)
    #plt.show()
    return max_val
# Load the template and target images
# Directory containing the images
directory =r"C:\Users\USER\Downloads\kibin_main_images"

# List all files in the directory
files = os.listdir(directory)

# Filter only image files (assuming images have extensions like .png, .jpg, .jpeg, etc.)
image_files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

# Create full paths for each image file
image_paths = [os.path.join(directory, file) for file in image_files]
values = []
# Print the list of image paths
for template_path in image_paths:
    
    target_path = r"C:\Users\USER\Downloads\kibin_sample\5.png"
    template_image = cv2.imread(template_path)
    main_image = cv2.imread(target_path)
    gray = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)
    print(template_path)
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Canny edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours in the edged image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area and aspect ratio
    min_area = 100  # Minimum area of a contour
    min_aspect_ratio = 0.5  # Minimum aspect ratio of a contour
    bounding_boxes = []
    for contour in contours:
        # Compute the bounding box of the contour
        x, y, w, h = cv2.boundingRect(contour)
        
        area = cv2.contourArea(contour)
        aspect_ratio = w / h
        bounding_boxes.append((x, y, w, h))
    
    
   
    biggest_box = max(bounding_boxes, key=lambda box: box[2] * box[3])
    x, y, w, h = biggest_box
    #cv2.rectangle(main_image, top_left, bottom_right, (0, 255, 0), 2)
    #x, y, template_width, template_height = best_match_location
    #bottom_right = (x + template_width, y + template_height)
    #cv2.rectangle(main_image, (x, y), (x+w,y+h), (0, 255, 0), 2)
    #plt.imshow(main_image)
    #plt.show()
    #Filter contours based on area and aspect ratio
    val = match_template(main_image, template_image, (w,h))
    values.append(val)
path = image_paths[values.index(max(values))]
#cv2.rectangle(main_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
main_name = path.split('\\')[-1]
template_name = template_path.split('\\')[-1]
print(main_name)

#get target, get each template