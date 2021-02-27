import socket
import sys
import os
from os import path

TCP_IP = '0.0.0.0'
TCP_PORT = int(sys.argv[1])
BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

while True:
    conn, addr = s.accept()
    need_to_close = False
    while not need_to_close:
        conn.settimeout(1)
        try:
            data = conn.recv(BUFFER_SIZE)
            conn.settimeout(None)
        except socket.timeout:  # timeout exception
            need_to_close = True
            conn.close()
            break
        except ConnectionResetError:  # client close the socket after "keep-alive"
            need_to_close = True
            conn.close()
            break
        except ConnectionAbortedError:
            need_to_close = True
            conn.close()
            break

        data = data.decode("utf-8")  # decode the data to string
        print(data, end = "")
        dataPart = data.split("\r\n\r\n")
        need_to_close = True

        for i in range(len(dataPart)):
            if dataPart[i] == '':
                break
            dataArray = dataPart[i].split("\n")  # line
            file_name = dataArray[0].split()[1]  # first line, file name

            if file_name == "/":  # index.html
                file_name = "/index.html"
            elif file_name == "/redirect":  # redirect
                conn.send(b"HTTP/1.1 301 Moved Permanently\r\nConnection: close\r\nLocation: /result.html\r\n\r\n")
                need_to_close = True
                break
            file_path = os.path.join(sys.path[0], "files" + file_name)
            is_keep_alive = False
            for line in dataArray:  # find Connection:
                if "Connection:" in line:
                    is_keep_alive = line.split()[1] == "keep-alive"  # 0 for close, 1 for keep-alive
                    break  # the inner for loop
            need_to_close = not is_keep_alive
            if not path.exists(file_path):  # check if file exist
                conn.send(b"HTTP/1.1 404 Not Found\r\nConnection: close\r\n\r\n")
                need_to_close = True
                break
            file_size = os.path.getsize(file_path)
            str_to_send = "HTTP/1.1 200 OK\r\n"  # create the header string
            if is_keep_alive:
                temp = "Connection: keep-alive\r\n"
            else:
                temp = "Connection: close\r\n"
            str_to_send += temp
            temp = "Content-Length: "
            str_to_send += temp
            temp = str(file_size)
            str_to_send += temp
            temp = "\r\n\r\n"
            str_to_send += temp
            try:
                with open(file_path, "rb") as f:  # read bytes from the file
                    bytes_read = f.read(file_size)
            except PermissionError:  # couldnt open the file
                conn.send(b"HTTP/1.1 404 Not Found\r\nConnection: close\r\n\r\n")
                need_to_close = True
                break
            except FileNotFoundError:  # file not found
                conn.send(b"HTTP/1.1 404 Not Found\r\nConnection: close\r\n\r\n")
                need_to_close = True
                break
            conn.send(bytes(str_to_send, "utf-8") + bytes_read)  # send bytes to client
            if not is_keep_alive:  # if needed to close
                need_to_close = True
                break
        if need_to_close:
            conn.close()
            break
