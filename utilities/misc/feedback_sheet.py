from utilities.omr_eval.capture_sheet import CaptureSheet
import os
import cv2
import numpy as np
try:
    #import dill as pickle
    import pickle
except Exception as e:
    import pickle
import random
# Directory containing PNG files

def presave_all():
    """Saves all bbox data and image template for each type of test. Takes up to 4 mins to process.
    Returns:
        FeedBackChoices object: object containing bbox + template image paths as properties 
        and method for retrieval. See: FeedBackChoices
    """
    main = PRESAVE_FEEDBACK(1,20,'idtf')[0]
    presave_tf = PRESAVE_FEEDBACK(1,300,'tf')[0]
    main.tf, main.tf_img_paths = presave_tf.tf, presave_tf.tf_img_paths
    presave_mc = PRESAVE_FEEDBACK(1,175,'mc')[0]
    main.mc, main.mc_img_paths = presave_mc.mc, presave_mc.mc_img_paths
    write_presaved_feedback(main)
    return main
    


class Circle:
    """?"""
    def __init__(self, *args):
        self.xywh = args



class FeedBackChoices:
    """DONT TOUCH"""
    def __init__(self):
        self.mc = []
        self.mc_img_paths = []
        #self.mc_choices_by_num = []
        self.tf = []
        self.tf_img_paths = []
        #self.tf_choices_by_num = []
        self.idtf = []
        self.idtf_img_paths = []

    def get_mc_by_count(self, count):
        return self.mc[count-1]
    def get_tf_by_count(self, count):
        return self.tf[count-1]
    def get_idtf_by_count(self,count):
        return self.idtf[count-1]
    

def write_presaved_feedback(data):
    """Writes presaved data. Dont use this as this will overwrite internal presaved propeties.
    Instead refer to function: presave_all()"""
    # Writing to a pickle file
    with open('assets/feedback.pkl', 'wb') as f:
        pickle.dump(data, f)


def read_presaved_feedback():
    """Reads presaved FeedBackChoices object"""
    # Reading from a pickle file
    with open('assets/feedback.pkl', 'rb') as f:
        data = pickle.load(f)
    return data

def convert_bbox_high_to_low(bbox_high_res, high_res_dims, low_res_dims):
    """
    Utility Function for internal processes.
    Convert bounding boxes from high resolution to low resolution maintaining aspect ratio.
    
    Args:
        bbox_high_res (tuple): Bounding box coordinates in (x, y, width, height) format 
                               in the high-resolution image.
        high_res_dims (tuple): Dimensions of the high-resolution image (width, height).
        low_res_dims (tuple): Dimensions of the low-resolution image (width, height).
        
    Returns:
        tuple: Bounding box coordinates in (x, y, width, height) format in the low-resolution image.
    """
    # Unpack dimensions
    high_res_width, high_res_height = high_res_dims
    low_res_width, low_res_height = low_res_dims
    
    # Unpack bounding box coordinates
    x_high, y_high, w_high, h_high = bbox_high_res
    
    # Calculate scaling factors
    scale_w = low_res_width / high_res_width
    scale_h = low_res_height / high_res_height
    
    # Scale bounding box coordinates to low-resolution image
    x_low = int(x_high * scale_w)
    y_low = int(y_high * scale_h)
    w_low = int(w_high * scale_w)
    h_low = int(h_high * scale_h)
    
    return x_low, y_low, w_low, h_low

def PRESAVE_FEEDBACK(start,finish,test_type,fbc_obj=None):
    """DONT USE. Refer to presave_all() function for writing.

    Args:
        start (_type_): _description_
        finish (_type_): _description_
        test_type (string): mc or tf
    """
    errors = 0
    fbc = FeedBackChoices() if fbc_obj is None else fbc_obj
    for count in range(start,finish+1):

        #print("presave iteration ",count)

        filepath = f'assets/{test_type}_img/{count}.png'
        
        cs=CaptureSheet(count,count,count,filepath, 1,on_android=False,show_plots=True)
        cs.get_boxes()
        
        cs.get_bubbles(redo=True, mod_value=3, for_feedback=True)
        image = cs.boxes.crops[0]
        
        cv2.imwrite(f'assets/feedback/{test_type}_img/{count}.png',image)
        cs.get_choices()
        #if cs.bubbles[0].test_type !='MULTIPLE CHOICE':
         #   errors += 1
        choices_by_num = cs.bubbles[0].choices_by_num_dict

        if test_type == 'mc':
            fbc.mc_img_paths.append(f'assets/feedback/{test_type}_img/{count}.png')
            fbc.mc.append(choices_by_num)
        elif test_type == 'tf':
            fbc.tf_img_paths.append(f'assets/feedback/{test_type}_img/{count}.png')
            fbc.tf.append(choices_by_num)
        elif test_type =='idtf':
            fbc.idtf_img_paths.append(f'assets/feedback/{test_type}_img/{count}.png')
            fbc.idtf.append(choices_by_num)
        #num_dict = {}
        #result = []
        #for index in range(1,count+1):
        #for choices in choices_by_num[index]:
            
            #choice = choices_by_num[index]
            ##print(choices_by_num)
            #
            #for bubble_pos in range(4 if test_type == 'mc' else 2):
           #     result.append(Circle(*choice[bubble_pos].xywh))
          #  num_dict[index] = result
         #   result=[]
        #cs.bubbles[0].choices_by_num = num_dict
    return fbc,errors



    
def feedback(answer_array, correct_array, test_type, item_count, save_filepath='img.png',for_preservation=False):
    """old code. DONT USE. Use  feedback_quick() instead.\nCaution: writes something."""
    folder_ref = {'TRUE OR FALSE': 'tf_img',
              'MULTIPLE CHOICE': 'mc_img',
              'IDENTIFICATION': 'idtf_img'}
    file_ref = f'{item_count}.png'
    multiplier_ref = {'TRUE OR FALSE': 2,
                      'MULTIPLE CHOICE':4,
                      'IDENTIFICATION': 1}
    overall_ref = f'assets/{folder_ref[test_type]}/{file_ref}'
    cs = CaptureSheet(item_count,item_count,item_count,overall_ref,1,on_android=False,show_plots=True)
    cs.get_boxes()
    
    #cs.get_bubbles()
    
    cs.get_bubbles(redo=True,mod_value=13)
    image = cs.boxes.crops[0]
    for x in cs.bubbles[0].rectangles:
        x,y,w,h = x
        
        x2, y2 = x + w, y + h
        #cv2.rectangle(image, (x, y), (x2, y2), [50,200,200], cv2.FILLED)
    cv2.imwrite('img.png',image)
    cs.get_choices()
    choices_by_num = cs.bubbles[0].choices_by_num
    if for_preservation:
        fbc = FeedBackChoices()
        if test_type == 'MULTIPLE CHOICE':
            fbc.mc_img_paths.append(f'assets/feedback/{test_type}_img/{item_count}.png')
            fbc.mc.append(choices_by_num)
        elif test_type == 'TRUE OR FALSE':
            fbc.tf_img_paths.append(f'assets/feedback/{test_type}_img/{item_count}.png')
            fbc.tf.append(choices_by_num)
        #print(fbc.mc)

    
    image =  np.repeat(image[:, :, np.newaxis], 3, axis=2)
    index_char = [
        ['A','T'],
        ['B', 'F'],
        ['C'],
        ['D']
    ]
    #print("COLORING PAPERS")
    #print(answer_array)
    #print(correct_array)
    #print(answer_array)
    

    for answer, correct, index in zip(answer_array, correct_array, range(1,len(answer_array)+1)):
        #for choices in choices_by_num[index]:
        
        choice = choices_by_num[index]
        ##print(choices_by_num)
        
        for bubble_pos in range(multiplier_ref[test_type]):
            x,y,w,h = choice[bubble_pos]
            x2, y2 = x + w, y + h
            
            #print("GETTING ")
            #print(bubble_pos)
            #print(answer)
            #print(index_char)
            #print(correct_array)
            ##print(answer, index_char[bubble_pos], correct_array[bubble_pos])
            for correct_list in correct: # correct single is a bubbble # caorrect can have cor
                if  correct_list in index_char[bubble_pos]: # yellow, listed as correct list
                    ##print(correct_list)
                    cv2.rectangle(image, (x, y), (x2, y2), [0,150,150], 5)

            if answer in index_char[bubble_pos]:
                #print(True)
                cv2.rectangle(image, (x, y), (x2, y2), [00,00,00], cv2.FILLED)
                if answer in correct:
        
                    cv2.rectangle(image, (x, y), (x2, y2), [00,200,00], 5)
                else:
                    #print(False)
                    cv2.rectangle(image, (x, y), (x2, y2), [00,000,200],5)
            # mark possible correct yellow
            
                # green = correct answer
    cv2.imwrite(save_filepath,image)
 
def add_text_on_bbox(x,y,w,h, image, text, text_color=None):
    if text_color == None:
        text_color = (0,0,0)

    # Calculate the center coordinates of the bounding box
    center_x = x + w // 2
    center_y = y + h // 2

    # Create an image canvas
    #image = cv2.imread("your_image.jpg")  # Load your image here

    # Define the text and font settings
    text = text
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 3
    font_thickness = 5

    # Get the size of the text
    text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]

    # Calculate the position to place the text to make it centered
    text_x = int(center_x - text_size[0] // 2)
    text_y = int(center_y + text_size[1] // 2)

    # Draw the text on the image
    cv2.putText(image, text, (text_x, text_y), font, font_scale, text_color, font_thickness)
    return image

def feedback_quick(answer_array, 
                   correct_array, 
                   test_type, 
                   item_count, 
                   save_filepath='img.png',
                   fbc=None,
                   idtf_eval_array = None):
    folder_ref = {'TRUE OR FALSE': 'tf_img',
              'MULTIPLE CHOICE': 'mc_img',
              'IDENTIFICATION': 'idtf_img'}
    file_ref = f'{item_count}.png'
    multiplier_ref = {'TRUE OR FALSE': 2,
                      'MULTIPLE CHOICE':4,
                      'IDENTIFICATION': 15}
    #overall_ref = f'assets/{folder_ref[test_type]}/{file_ref}'
    #print("LOADING PRESAVED")
    fbc = read_presaved_feedback() if fbc is None else fbc
    #print("LOADING PRESAVED DONE")
    
    index_char = [
        ['A','T'],
        ['B', 'F'],
        ['C'],
        ['D']
    ]
    image = cv2.imread(f'assets/feedback/{folder_ref[test_type]}/{file_ref}',cv2.IMREAD_GRAYSCALE)
    #image =  np.repeat(image[:, :, np.newaxis], 3, axis=2)
    #gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #threshold_value = 200
    #max_value = 255
    #_, gray_image = cv2.threshold(gray_image, threshold_value, max_value,  type=cv2.THRESH_BINARY)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    #print("COLORING PAPERS")
    content = fbc.mc if test_type=='MULTIPLE CHOICE' else fbc.tf
    content = None
    if test_type=="MULTIPLE CHOICE":
        content = fbc.mc
    elif test_type =='TRUE OR FALSE':
        content = fbc.tf
    else:
        content = fbc.idtf
    #print(fbc.idtf)
    #print(fbc.idtf.keys())
    choices_by_num = content[item_count-1]
    #print((choices_by_num))
    
    

    
    #answer_array = answer_array[sorted_indices]
    for answer, correct, index in zip(answer_array, correct_array, range(1,len(answer_array)+1)):
        #for choices in choices_by_num[index]:
        #print(len(choices_by_num))
        #print(np.array(choices_by_num).shape)
        choice = choices_by_num[index]
        ##print(choices_by_num)
        choice= np.array(choice)
        print(choice)
        sorted_indices = np.argsort(choice[:,1])
        choice = choice[sorted_indices]
        previous = (0,0,0)
        for bubble_pos in range(multiplier_ref[test_type]):
            x,y,w,h = choice[bubble_pos]
            ##print(x,y,w,h)
            #print(image.shape)
            #x,y,w,h = convert_bbox_high_to_low(choice[bubble_pos],[int(s*1) for s in image.shape[:2]],image.shape[:2])
            x2, y2 = x + w, y + h
            print("IDTF ARRAY",idtf_eval_array)
            print(answer_array)
            print(correct_array)
            
            if test_type == 'IDENTIFICATION':
            
                try:
                    text = correct[bubble_pos]
                except IndexError as e:
                    print(e)
                    text = ' '
                try:
                    is_correct = idtf_eval_array[index]
                except IndexError as e:
                    print(e)
                    is_correct = previous
                print("ISCORRECT",is_correct)
                print(idtf_eval_array)
                if is_correct == 1:
                    text_color = (0,0,0)
                    previous = 1
                else:
                    text_color = (0,00,00)
                    previous =0
                image = add_text_on_bbox(x=x,
                                        y=y,
                                        w=w,
                                        h=h,
                                        image=image,
                                        text=text,
                                        text_color=text_color)
            ##print(answer, index_char[bubble_pos], correct_array[bubble_pos])
            # yellow, listed as correct list
                    ##print(correct_list)
               #     pass
                    
                        
            if test_type == 'IDENTIFICATION': # skip what follows when is identiificaton
                continue
            for correct_list in correct: # correct single is a bubbble # caorrect can have cor
                if  correct_list in index_char[bubble_pos]:
                    cv2.rectangle(image, (x, y), (x2, y2), [00,200,0], 10)
            if answer in index_char[bubble_pos]:
                ##print(True)
                cv2.rectangle(image, (x, y), (x2, y2), [00,00,00], cv2.FILLED)
                if answer in correct:
                    cv2.rectangle(image, (x, y), (x2, y2), [00,200,0], 10)
                else:
                    ##print(False)
                    cv2.rectangle(image, (x, y), (x2, y2), [00,000,200],10)
                    pass
            
            # mark possible correct yellow
        
            
                # green = correct answer
    # Specify the border size

    padding_size = 15

    # Define the border size
    border_size = 10

    # Define the color for the border (e.g., black)
    border_color = (0, 0, 0)  # Black color in BGR format

    # Add a border to the image by painting over the pixels
    image_with_border = np.copy(image)
    image_with_border[:border_size, :, :] = border_color  # Top border
    image_with_border[-border_size:, :, :] = border_color  # Bottom border
    image_with_border[:, :border_size, :] = border_color  # Left border
    image_with_border[:, -border_size:, :] = border_color  # Right border

    # Pad the image with black color
    image = np.pad(image_with_border, ((padding_size, padding_size), (padding_size, padding_size), (0, 0)), mode='constant', constant_values=255)

    cv2.imwrite(save_filepath,image)
    save_filepath2 = save_filepath[:-4] + '-flipped.png'
    cv2.imwrite(save_filepath2, cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE))

    return True

        
    #print("DONE FEEDBACK GENERATION")
 