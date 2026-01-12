import socket
import threading

host = "127.0.0.1"
port = 12345

clients = {}
lock = threading.Lock()


def handle_client(client_socket):
    username = ""
    try:
        username = client_socket.recv(1024).decode().strip()

        with lock:
            clients[username] = client_socket
            print(username + " connected")

        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            message = data.decode().strip()

            if message.startswith("@") and ":" in message:
                target, text = message.split(":", 1)
                target = target.replace("@", "").strip()
                text = text.strip()

                with lock:
                    if target in clients:
                        clients[target].send(
                            ("from " + username + ": " + text).encode()
                        )
                    else:
                        client_socket.send(
                            ("error: user not connected").encode()
                        )

    except:
        pass

    finally:
        with lock:
            if username in clients:
                del clients[username]

        client_socket.close()
        print(username + " disconnected")


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print("server listening on " + host + ":" + str(port))

    while True:
        client_socket, addr = server_socket.accept()
        thread = threading.Thread(
            target=handle_client, args=(client_socket,)
        )
        thread.start()


if __name__ == "__main__":
    start_server()
