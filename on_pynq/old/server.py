import socket

BUFFER_SIZE = 1024 * 4 # 4KB
host = '0.0.0.0'  # 對server端為主機位置
port = 5002

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