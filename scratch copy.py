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
def match_template(image_array, template_array, search_threshold, prob_threshold=0.7):
    main = image_array
    template = template_array
    main_gray = 255 - main
    
    template_gray = template
    # Perform template matching
    result = cv2.matchTemplate(main_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    
    #result2=  cv2.matchTemplate(main_gray, template_gray2, cv2.TM_CCOEFF_NORMED)
    #print(result)
    # Get the coordinates of the top 20 matches
    locs = np.argsort(result.ravel())[::-1]# Indices of top 20 matches sorted by score
    
    #locs2 = np.argsort(result2.ravel())[::-1]# Indices of top 20 matches sorted by score
    # Get the size (width and height) of the template
    template_w, template_h = template_gray.shape[::-1]

    drawn_rectangles = []
    count = 0
    scores = []
    # Draw rectangles around the top 20 matches
    print(search_threshold)
    for loc in locs:
        y, x = np.unravel_index(loc, result.shape)
        # Check for overlap with previously drawn rectangles
        overlap = False
        for rect in drawn_rectangles:
            if abs(x - rect[0]) < template_w and abs(y - rect[1]) < template_h:
                overlap = True
                break
        
        if not overlap:
            
            if result[y,x] > prob_threshold:
                #print(result[y,x])
                drawn_rectangles.append((x,y,template_w,template_h))
                print(result[y,x])
                continue

            #cv2.rectangle(main_gray, (x, y), (x + template_w, y + template_h), (0, 255, 0), 2)
            #drawn_rectangles.append((x, y))
            #scores.append(result[y, x])
            count+=1
        if count>=search_threshold:
            break
        return drawn_rectangles
    
    
#___________________
all_rect = []
main = cs.boxes.crops[0]
template = cv2.imread('bubble_template.png',cv2.IMREAD_GRAYSCALE)
template_filled = np.ones_like(template)*255
print(main.shape)
print(template.shape)
print(template_filled.shape)
rect_filled = match_template(main, template_filled, 400)
num_filled = len(rect_filled)
rect_bubbles = match_template(main, template, 400-num_filled)
all_rect += rect_filled
all_rect += rect_bubbles
print(all_rect)
for rect in all_rect:
    x,y,template_w,template_h = rect
    cv2.rectangle(main, (x, y), (x + template_w, y + template_h), (0, 255, 0), 5)
plt.imshow(main)
plt.show()