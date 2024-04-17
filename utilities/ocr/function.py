import cv2 as cv
import numpy as np
import os
#from utilities.ocr.model import TensorFlowModel
on_android = False
try:
    print("RUN")
    on_android = True
    from android.storage import primary_external_storage_path
    storage = primary_external_storage_path()+'/'
    # Import TFLite interpreter from tflite_runtime package if it's available.
    from tflite_runtime.interpreter import Interpreter
    #from tflite_runtime.interpreter import load_delegate
    
except ImportError:
    print("IMORT EROR")
    on_android = False
    # If not, fallback to use the TFLite interpreter from the full TF package.
    import tensorflow as tf
    Interpreter = tf.lite.Interpreter
    load_delegate = tf.lite.experimental.load_delegate
    storage = ''
#print("GETTING INTERPRESTER")
model_path = os.path.abspath('utilities/ocr/converted_model.tflite')
interpreter = Interpreter(model_path=model_path)
#print("ALLOCATING")
interpreter.allocate_tensors()
#print("STOPPING HERE")
#images = [cv.imread(file) for file in glob.glob("test\*.jpg")]

def Predict(image,count=0):
    if on_android:
        image = cv.rotate(image, cv.ROTATE_90_COUNTERCLOCKWISE)
        image = cv.flip(image, 1)
        #image = cv.flip(image,0)
        image = cv.rotate(image, cv.ROTATE_90_COUNTERCLOCKWISE)
        image = cv.rotate(image, cv.ROTATE_90_COUNTERCLOCKWISE)
    dict_word = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H',8:'I',9:'J',10:'K',11:'L',12:'M',13:'N',14:'O',15:'P',16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V',22:'W',23:'X', 24:'Y',25:'Z'}
    labelNames = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    labelNames = [l for l in labelNames]
    #gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.medianBlur(image, 5)
    ret, gray = cv.threshold(gray, 30, 255, cv.THRESH_BINARY)
    #gray = cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 2)
    #gray = np.pad(gray, ((9,9), (9, 9), (0, 0)), mode='constant', constant_values=0)
    #padding = 20
    #gray = cv.copyMakeBorder(gray, padding, padding, padding, padding, cv.BORDER_CONSTANT, value = 0)
    #element = cv.getStructuringElement(cv.MORPH_RECT, (7, 7))
    #gray = cv.morphologyEx(gray, cv.MORPH_GRADIENT, element)
    
    #gray = gray / 255.  # downsampling
    gray = 255 - gray
    #print(np.unique(gray))
    gray = cv.resize(gray, (32, 32))  # resizing
    #cv.imwrite(storage + f'{count}-filtered.png',gray)
    #cv.imwrite(storage + f'{count}-filtered.png',gray) if on_android else True
    # Reshape the image
    gray = gray / 255.0
    gray = np.reshape(gray, (1, 32, 32,1)).astype(np.float32)
    #x = np.array(np.random.random_sample((1, 28, 28)), np.float32)
    
    
    # Prepare input tensor for the model
    input_details = interpreter.get_input_details()
    interpreter.set_tensor(input_details[0]['index'], gray)
    path = storage + f'{count}.png'
    cv.imwrite(path,image) if on_android else True
    
    # Run inference
    interpreter.invoke()

    # Get the output tensor
    output_details = interpreter.get_output_details()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    sorted_indices = np.argsort(output_data)
    #print("DATA",sorted(output_data[0]))
    #print(sorted_indices)
    top_three_indices = np.array(list(labelNames))[sorted_indices]
    #print(sorted_indices)
    #print(top_three_indices)

    # Get the predicted class
    predicted_class = labelNames[np.argmax(output_data)]
    #print(len(top_three_indices[0]))
    #print(len(sorted(output_data[0])))
    #print({x:y for x,y in zip(top_three_indices[0], sorted(output_data[0]))})
    return predicted_class, {x:y for x,y in zip(top_three_indices[0], sorted(output_data[0]))}
