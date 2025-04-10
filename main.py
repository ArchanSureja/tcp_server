import socket 
import threading 

def send_response(socket_fd):
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 12\r\n\r\nHello World!\r\n"
        socket_fd.send(response.encode('utf-8'))
        socket_fd.close()
def main():
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1',7070))
        s.listen()
        while True : 
            socket_fd ,_=s.accept() 
            print("client connected")
            _ = socket_fd.recv(1024) 
            t=threading.Thread(target=send_response,args=(socket_fd,))
            t.start()
if __name__ == "__main__":
    main()
