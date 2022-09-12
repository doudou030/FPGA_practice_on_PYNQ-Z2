from asyncio.windows_events import NULL
from tkinter import *
from tkinter.filedialog import asksaveasfilename as saveAs


import PIL
from PIL import  ImageDraw, ImageGrab
import socket
import os
import tqdm
import random

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024 * 4 # 4KB
cv = NULL
draw = NULL

def activate_paint(e):
    global lastx, lasty
    cv.bind('<B1-Motion>', paint)
    lastx, lasty = e.x, e.y

def paint(event):
    global lastx, lasty
    x, y = event.x, event.y
    cv.create_line((lastx, lasty, x, y), width=8, fill='black', smooth=True, splinesteps=12)
    lastx, lasty = x, y

def reset_button():
    cv.delete('all')
    draw.rectangle((0, 0, 500, 500), fill="white")
    question_x = random.randint(0,5)
    question_y = random.randint(0,4)
    answer = question_x + question_y
    question = ('{} + {} = ?'.format(question_x,question_y))
    cv.create_text(250,30,text=question, font=('Arial', 40))
    
def exit_button():
    exit()

def upload():
    filename = "image.jpg"
    #抓圖
    x1 = win.winfo_rootx() + cv.winfo_rootx()
    y1 = win.winfo_rooty() + cv.winfo_rooty()
    x2 = x1 + cv.winfo_width()
    y2 = y1 + cv.winfo_height()
    ImageGrab.grab().crop((x1, y1, x2, y2)).save(filename)
    filesize = os.path.getsize(filename)
    
    host = "192.168.2.99" # pynq的eth0的ip位置
    port = 5003
    address = (host, port)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"[+] Connecting to {host}:{port}")
    s.connect(address)
    print("[+] Connected.")
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    #######傳輸開始#######
    img = open(filename,"rb")
    while True:
        imgDATA = img.read(BUFFER_SIZE)
        if not imgDATA:
            break
        s.sendall(imgDATA)
        progress.update(len(imgDATA))
        
    img.close()
    print("[+] img closed.")
    #######傳輸結束#######
    s.close()
    print("[+] Socket closed.")



    

# GUI介面
win = Tk()
win.title("手寫辨識小遊戲")
win.resizable(0,0) 
lastx, lasty = None, None

cv = Canvas(win, width=500, height=500, bg='white')
cv.pack

white = (255,255,255)
image1 = PIL.Image.new('RGB', (500, 500), white)
draw = ImageDraw.Draw(image1)

cv.pack(expand=YES, fill=BOTH)
cv.bind('<Button-1>', activate_paint)

# button setup
uploadBB = Button(text="Upload", command=upload)
uploadBB.place(relx=.5, rely=.975, anchor="center")
uploadBB.pack

reset=Button(text='Reset',command=reset_button)
reset.pack(side=LEFT)

_exit=Button(text='Exit',command=exit_button)
_exit.pack(side=RIGHT)

## text
while(True):
    question_x = random.randint(0,5)
    question_y = random.randint(0,5)
    answer = question_x + question_y
    if(answer < 10): 
        break 


question = ('{} + {} = ?'.format(question_x,question_y))
cv.create_text(250,30,text=question, font=('Arial', 40))

win.mainloop()