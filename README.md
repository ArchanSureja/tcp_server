# Simple Multithreaded HTTP Server in Python 🧵🌐

This is a basic multithreaded HTTP server written in Python using sockets and a custom thread pool. It listens on port `7070` and responds with a simple "Hello World!" message to every incoming request.

---

## 📂 Project Structure

- **`ThreadPool` class**  
  A simple thread pool implementation using Python’s `threading` and `queue` modules.

- **`send_response(socket_fd)`**  
  Handles each client request: receives data, simulates a delay, and sends a fixed HTTP response.

- **`main()` function**  
  Starts the server, listens for connections, and assigns each one to the thread pool.

---

## 🚀 How It Works

1. The server listens on `127.0.0.1:7070`.
2. When a client connects, it prints `"client connected"`.
3. The connection is passed to the thread pool for processing.
4. Each thread:
   - Reads the request.
   - Uses Routes to determine file path
   - Sends back a file data with appropriate MIME TYPE response.
   - Closes the connection.

---

## 🛠️ Requirements

- Python 3.x  
  No external libraries are required — only built-in modules (`socket`, `threading`, `queue`, `time`).

---

## 📦 Running the Server

```bash
python main.py
