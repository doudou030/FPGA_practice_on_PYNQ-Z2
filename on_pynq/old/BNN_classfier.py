from pynq import bnn

hw_classifier = bnn.LfcClassifier(bnn.NETWORK_LFCW1A1,"mnist",bnn.RUNTIME_HW)
sw_classifier = bnn.LfcClassifier(bnn.NETWORK_LFCW1A1,"mnist",bnn.RUNTIME_SW)

import cv2
from PIL import Image as PIL_Image
from PIL import ImageEnhance
from PIL import ImageOps

orig_img_path = ('image.jpg')

img = PIL_Image.open(orig_img_path).convert("L")     
                   
#Image enhancement                
contr = ImageEnhance.Contrast(img)
img = contr.enhance(3)                                                    # The enhancement values (contrast and brightness) 
bright = ImageEnhance.Brightness(img)                                     # depends on backgroud, external lights etc
img = bright.enhance(4.0)          

#img = img.rotate(180)                                                     # Rotate the image (depending on camera orientation)
#Adding a border for future cropping
img = ImageOps.expand(img,border=80,fill='white')


from PIL import Image as PIL_Image
import numpy as np
import math
from scipy import misc

#Find bounding box  
inverted = ImageOps.invert(img)  
box = inverted.getbbox()  
img_new = img.crop(box)  
width, height = img_new.size  
ratio = min((28./height), (28./width))  
background = PIL_Image.new('RGB', (28,28), (255,255,255))  
if(height == width):  
    img_new = img_new.resize((28,28))  
elif(height>width):  
    img_new = img_new.resize((int(width*ratio),28))  
    background.paste(img_new, (int((28-img_new.size[0])/2),int((28-img_new.size[1])/2)))  
else:  
    img_new = img_new.resize((28, int(height*ratio)))  
    background.paste(img_new, (int((28-img_new.size[0])/2),int((28-img_new.size[1])/2)))  
  
background  
img_data=np.asarray(background)  
img_data = img_data[:,:,0]  
misc.imsave('img_webcam_mnist.png', img_data) 


from array import *
from PIL import Image as PIL_Image
from PIL import ImageOps
img_load = PIL_Image.open('img_webcam_mnist.png').convert("L")  
# Convert to BNN input format  
# The image is resized to comply with the MNIST standard. The image is resized at 28x28 pixels and the colors inverted.   
  
#Resize the image and invert it (white on black)  
smallimg = ImageOps.invert(img_load)  
smallimg = smallimg.rotate(0)  
  
data_image = array('B')  
  
pixel = smallimg.load()  
for x in range(0,28):  
    for y in range(0,28):  
        if(pixel[y,x] == 255):  
            data_image.append(255)  
        else:  
            data_image.append(1)  
          
# Setting up the header of the MNIST format file - Required as the hardware is designed for MNIST dataset         
hexval = "{0:#0{1}x}".format(1,6)  
header = array('B')  
header.extend([0,0,8,1,0,0])  
header.append(int('0x'+hexval[2:][:2],16))  
header.append(int('0x'+hexval[2:][2:],16))  
header.extend([0,0,0,28,0,0,0,28])  
header[3] = 3 # Changing MSB for image data (0x00000803)  
data_image = header + data_image  
output_file = open('img_webcam_mnist_processed.jpg', 'wb')  
data_image.tofile(output_file)  
output_file.close()   


print("\n\n")
class_out = hw_classifier.classify_mnist("img_webcam_mnist_processed.jpg")
print("Hardware Classifier")
print("Class number: {0}".format(class_out))
print("Class name: {0}".format(hw_classifier.class_name(class_out)))
print("\n\n")

class_out=sw_classifier.classify_mnist("img_webcam_mnist_processed.jpg")
print("Software Classifier:")
print("Class number: {0}".format(class_out))
print("Class name: {0}".format(hw_classifier.class_name(class_out)))




