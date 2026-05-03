import socket
import threading

TARGET_HOST = "108.128.216.176"   # the IP Python found (VPN off)
TARGET_PORT = 6543
LOCAL_HOST = "127.0.0.1"
LOCAL_PORT = 15432

def forward(src, dst):
    try:
        while True:
            data = src.recv(4096)
            if not data:
                break
            dst.sendall(data)
    except:
        pass
    finally:
        src.close()
        dst.close()

def handle(client):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((TARGET_HOST, TARGET_PORT))
        threading.Thread(target=forward, args=(client, server), daemon=True).start()
        threading.Thread(target=forward, args=(server, client), daemon=True).start()
    except Exception as e:
        print("Proxy error:", e)

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.bind((LOCAL_HOST, LOCAL_PORT))
listener.listen(5)
print(f"Proxy running → connect Power BI to {LOCAL_HOST}:{LOCAL_PORT}")
while True:
    client_socket, _ = listener.accept()
    threading.Thread(target=handle, args=(client_socket,), daemon=True).start()