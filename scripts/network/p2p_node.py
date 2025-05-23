import socket
import threading

class Node:
    def __init__(self, host="127.0.0.1", port=5000):
        self.host = host
        self.port = port
        self.peers = []

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen()
        print(f"🌐 Nodo escuchando en {self.host}:{self.port}")
        while True:
            conn, addr = server.accept()
            print(f"🔗 Conexión establecida con {addr}")
            threading.Thread(target=self.handle_client, args=(conn,)).start()

    def handle_client(self, conn):
        while True:
            try:
                data = conn.recv(4096)
                if not data:
                    break
                print(f"📩 Recibido: {data.decode()}")
            except:
                break
        conn.close()

    def connect_to_peer(self, peer_host, peer_port):
        peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peer.connect((peer_host, peer_port))
        self.peers.append(peer)
        print(f"🔗 Conectado a nodo {peer_host}:{peer_port}")
        return peer

    def send_to_peers(self, message):
        for peer in self.peers:
            try:
                peer.sendall(message.encode())
            except:
                self.peers.remove(peer)
