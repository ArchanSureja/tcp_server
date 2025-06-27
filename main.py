import socket 
import threading 
import queue
import time 
import json 
import mimetypes

class ThreadPool():
    def __init__(self,num_of_threads):
          self.task_queue = queue.Queue()
          self.threads = []
          self.num_threads = num_of_threads 
          self.shutdown_flag = threading.Event()
          for _ in range(self.num_threads):
               t = threading.Thread(target=self.worker)
               t.start()
               self.threads.append(t)

    def worker(self):
         while not self.shutdown_flag.is_set():
            try:
                task,args = self.task_queue.get()
                task(*args)
                self.task_queue.task_done()
            except Exception as e:
                 print("ERROR in thread ",e)
           
    def submit(self,task,*args):
         self.task_queue.put((task,args))
    
    def shutdown(self):
         self.shutdown_flag.set()

def load_routes(config_file="routes.json"):
    with open(config_file) as f:
        return json.load(f)

def send_response(socket_fd,routes):
        path = socket_fd.recv(1024).decode().split(" ")[1]
        print(f"Received request for path: {path}")
        print(f"Routes: {routes[path] if path in routes else 'Not Found'}")

        if path == "/favicon.ico":
            socket_fd.close()
            return 
        if path in routes:
            try:
                with open(routes[path],"rb") as f:
                    data = f.read()

                mime_type , _ = mimetypes.guess_type(routes[path])
        

                if mime_type is None:
                    mime_type = 'application/octet-stream'

                header = (
                    f"HTTP/1.1 200 OK\r\n"
                    f"Content-Type: {mime_type}\r\n"
                    f"Content-Length: {len(data)}\r\n"
                    f"\r\n"
                )
                socket_fd.send(header.encode('utf-8'))
                socket_fd.send(data)
            except FileNotFoundError as e:
                print(f"File not found: {e}")
                error = (
                    "HTTP/1.1 404 Not Found\r\n"
                    "Content-Type: text/plain\r\n"
                    "Content-Length: 14\r\n"
                    "\r\n"
                    "File Not Found"
                )
                socket_fd.send(error.encode('utf-8'))
            finally:
                print("Closing socket")
                socket_fd.close()
                print("Socket closed")
        else:
            error = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/plain\r\n"
                "Content-Length: 14\r\n"
                "\r\n"
                "File Not Found"
            )
            socket_fd.send(error.encode('utf-8'))
            socket_fd.close()
            print("Socket closed")

def main():
    thread_pool = ThreadPool(5)
    routes = load_routes()
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1',7070))
        s.listen()
        while True: 
            socket_fd ,_= s.accept() 
            print("client connected")
            thread_pool.submit(send_response,socket_fd,routes)


if __name__ == "__main__":
    main()
