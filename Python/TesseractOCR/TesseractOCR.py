from PIL import Image
import pytesseract as pyT
import numpy as np
import argparse
import os
import glob

pyT.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR-4.0\\tesseract'
#
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True,
#                help="C:\\Users\\Dave.Wood\\Pictures\\OCR_TESTING")
#
#ap.add_argument("-p", "--preprocess", type=str, default="thresh",
#                help="thresh")
#
#args = vars(ap.parse_args())
#
#image=cv2.imread(args["image"])
#gray=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#if(args["preprocess"] == "thresh"):
#    gray = cv2.threshold(gray, 0, 255,
#                         cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
#elif(args["preprocess"] == "blur"):
#    gray = cv2.medianBlur(gray, 3)
#    
#filename = "{}.png".format(os.getpid())

# Loads image list
image_list = list(map(Image.open, glob.glob('C:\\Users\\Dave.Wood\\Pictures\\OCR_TESTING\\*.jpg')))

# converts image to array
image = image_list[3]

#subscript an array
img = Image.fromarray(np.array(image), 'RGB').convert('LA')
output_list = list()
slice_size = 150
for x in range(1, int(img.size[0]/slice_size)):
    print(str(x*slice_size))
    cropped_image = [((x-1)*slice_size):(x*slice_size), :]
    # convert back to image object which is also grayscale
    imag = Image.fromarray(cropped_image, 'RGB').convert('LA')
#    output_list.append(pyT.image_to_string(imag))
    print(pyT.image_to_string(imag))

# disp
image.show()


