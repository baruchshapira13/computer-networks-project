import socket
import threading

host = "127.0.0.1"
port = 12345


def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print(data.decode())
        except:
            break


def start_client():
    username = input("enter username: ")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    sock.send(username.encode())

    thread = threading.Thread(
        target=receive_messages, args=(sock,), daemon=True
    )
    thread.start()

    print("connected to server")
    print("message format: @user:message")

    while True:
        msg = input()
        if msg == "exit":
            break
        sock.send(msg.encode())

    sock.close()


if __name__ == "__main__":
    start_client()
