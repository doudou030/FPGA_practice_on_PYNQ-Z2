import socket

def scklisten():
    
    BUFFER_SIZE = 1024 * 4 # 4KB
    host = '0.0.0.0'  # 對server端為主機位置
    port = 5003

    address = (host, port)

    socket01 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # AF_INET:默認IPv4, SOCK_STREAM:TCP

    socket01.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    socket01.bind(address)  # 讓這個socket要綁到位址(ip/port)
    socket01.listen(5)  # listen(backlog)
    print(f"[*] Listening as {host}:{port}")

    # backlog:操作系統可以掛起的最大連接數量。該值至少為1，大部分應用程序設為5就可以了
    print('Socket Startup')

    conn, addr = socket01.accept()  # 接受遠程計算機的連接請求，建立起與客戶機之間的通信連接
    # 返回（conn,address)
    # conn是新的套接字對象，可以用來接收和發送數據。address是連接客戶端的地址
    print('Connected by', addr)

    ##################################################
    # 開始接收
    print('begin write image file "image.jpg"')
    imgFile = open('image.jpg', 'wb')  # 開始寫入圖片檔
    while True:
        imgData = conn.recv(BUFFER_SIZE)  # 接收遠端主機傳來的數據
        if not imgData:
            break  # 讀完檔案結束迴圈
        imgFile.write(imgData)
    imgFile.close()
    print('image save')
    ##################################################

    conn.close()  # 關閉
    socket01.close()
    print('server close')




from pynq import bnn
import cv2
from PIL import Image as PIL_Image
from PIL import ImageEnhance
from PIL import ImageOps
import numpy as np
import math
from scipy import misc
from array import *


def BNNclass():
    

    hw_classifier = bnn.LfcClassifier(bnn.NETWORK_LFCW1A1,"mnist",bnn.RUNTIME_HW)
    sw_classifier = bnn.LfcClassifier(bnn.NETWORK_LFCW1A1,"mnist",bnn.RUNTIME_SW)

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
    


while 1:
        scklisten()
        BNNclass()
     