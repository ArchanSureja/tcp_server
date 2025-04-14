import socket 
import threading 
import queue
import time 
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
                task(args)
                self.task_queue.task_done()
            except Exception as e:
                 print("ERROR in thread ",e)
           
    def submit(self,task,args):
         self.task_queue.put((task,args))
    
    def shutdown(self):
         self.shutdown_flag.set()
          
def send_response(socket_fd):
        _ = socket_fd.recv(1024)
        # delay for simulating actual behaviour  
        time.sleep(10) 
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 12\r\n\r\nHello World!\r\n"
        socket_fd.send(response.encode('utf-8'))
        socket_fd.close()

def main():
    thread_pool = ThreadPool(2)
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1',7070))
        s.listen()
        while True: 
            socket_fd ,_=s.accept() 
            print("client connected")
            thread_pool.submit(send_response,socket_fd)


if __name__ == "__main__":
    main()
