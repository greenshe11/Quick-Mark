from utilities.omr_eval.capture_sheet import CaptureSheet
import cv2
import numpy as np

import matplotlib.pyplot as plt
cs = CaptureSheet(100,0,10,
                  img=r"C:\Users\USER\Downloads\423542016_781729933397725_4299235962542117415_n.jpg",
                  get_result_img=False,show_plots=False,
                  on_android=False,boxes_num=1)
cs.get_boxes()
cs.get_bubbles()
#cs.get_choices()
#cs.get_scores() 
def thicken_lines(image, kernel_size=(3, 3), iterations=3):
    # Define a kernel for dilation
    kernel = np.ones(kernel_size, np.uint8)
    
    # Perform dilation
    thickened_image = cv2.dilate(image, kernel, iterations=iterations)
    
    return thickened_image

def match_template(main, template):
    main = cv2.imread(main, cv2.IMREAD_GRAYSCALE)
    #main = cv2.cs.boxes.crops[0]
    main = cs.boxes.crops[0]
    try:
        template = cv2.imread(template, cv2.IMREAD_GRAYSCALE)
    except Exception as e:
        print(e)
        template = cv2.imread(template)
    
    main_gray = 255 - main
    #main_gray = thicken_lines(main_gray)
    _, main_gray = cv2.threshold(main_gray, 127, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # Define a 3x3 rectangular kernel
    main_gray = cv2.erode(main_gray, kernel, iterations=1)
    main_gray = cv2.Canny(main_gray, threshold1=100, threshold2=200)
    cv2.imwrite('res.png',main_gray)
    template_gray = template
    template_gray2 = np.ones_like(template)*255
    cv2.imwrite('template.png', template_gray2)
    # Perform template matching
    result = cv2.matchTemplate(main_gray, template_gray, cv2.TM_CCORR)
    result2=  cv2.matchTemplate(main_gray, template_gray2, cv2.TM_SQDIFF_NORMED)
    result = result
    #print(result)
    # Get the coordinates of the top 20 matches
    locs = np.flip(np.argsort(result.ravel()))# Indices of top 20 matches sorted by score
    
    #locs2 = np.argsort(result2.ravel())[::-1]# Indices of top 20 matches sorted by score
    # Get the size (width and height) of the template
    template_w, template_h = template_gray.shape[::-1]
    drawn_rectangles = []
    count = 0
    scores = []
    filled_rect = []
    # Draw rectangles around the top 20 matches
    for loc in locs:
        y, x = np.unravel_index(loc, result.shape)
        # Check for overlap with previously drawn rectangles
        overlap = False
        for rect in drawn_rectangles:
            if abs(x - rect[0]) < template_w and abs(y - rect[1]) < template_h:
                overlap = True
                break
        if not overlap:
            
            """if result[y,x] > 0.70:
                print(result[y,x])
                continue"""

            cv2.rectangle(main, (x, y), (x + template_w, y + template_h), (0, 255, 0), 2)
            drawn_rectangles.append((x, y))
            scores.append(result[y, x])
            count+=1
        if count>=400:
            break
    #print(np.mean(scores))
    #print(np.min(scores))
    #print(np.max(scores))
    #print(np.median(scores))
    # Draw a rectangle around the best match
    #cv2.rectangle(main_gray, (best_match_x, best_match_y), (best_match_x + best_match_w, best_match_y + best_match_h), (0, 255, 0), 2)
    plt.imshow(main)
    plt.show()

match_template(r"C:\Users\USER\Downloads\WIN_20240228_07_06_06_Pro.jpg",
               'bubble_template.png')
