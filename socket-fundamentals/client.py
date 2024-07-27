import socket

HOST = '192.168.1.68'
PORT = 9090

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

client.send("Hello World!".encode('utf-8'))
print(client.recv(1024).decode('utf-8'))