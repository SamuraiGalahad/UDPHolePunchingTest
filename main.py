from config import LOCAL_PORT, SERVER_PORT, SERVER_IP
import random
import socket
import threading
import time

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("0.0.0.0", LOCAL_PORT))

code = "TESTCODE"

client.sendto(code.encode(), (SERVER_IP, SERVER_PORT))

peers = set()


def receive_messages():
    while True:
        data, addr = client.recvfrom(1024)
        message = data.decode()
        print(message)
        if ":" in message:
            peer_addr = (message.split(":")[0], int(message.split(":")[1]))
            peers.add(peer_addr)

            for _ in range(5):
                client.sendto(b"Punch", peer_addr)

            print(f"{peer_addr}")


threading.Thread(target=receive_messages, daemon=True).start()
msg = random.randint(1, 10)
while True:
    if msg:
        for peer in peers:
            client.sendto(str(msg).encode(), peer)
            time.sleep(0.5)
