import threading
import socket

host = '127.0.0.1' # localhost
port = 55555 # server port

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message: str):
  '''Sends encoded messages to all connected clients'''
  for client in clients:
    client.send(message)


def handle(client: socket.socket):
  '''Handles messages from client'''
  while True:
    try:
      # Broadcasts the message
      message = client.recv(1024)
      broadcast(message)
    except:
      # Remove the client
      index = clients.index(client)
      clients.remove(client)
      client.close()
      nickname = nicknames[index]
      nicknames.remove(nickname)
      broadcast(f'{nickname} left the chat!'.encode('ascii'))
      break


def receive():
  while True:
    # Accept Connection
    client, address = server.accept()
    print(f'Connected with {str(address)}')
    
    # Request And Store Nickname
    client.send('NICK'.encode('ascii'))
    nickname = client.recv(1024).decode('ascii')
    nicknames.append(nickname)
    clients.append(client)

    print(f'Nickname of the client is {nickname}')
    broadcast(f'{nickname} joined the chat!'.encode('ascii'))
    client.send('Connected to the server!'.encode('ascii'))

    thread = threading.Thread(target=handle, args=(client,))
    thread.start()


if __name__ == "__main__":
  print('Server is listening...')
  receive()