import threading
import socket

# Choosing Nickname
nickname = input('Choose a nickname: ')

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

def receive():
  while True:
    try:
      message = client.recv(1024).decode('ascii')
      # If 'NICK' Send Nickname
      if message == 'NICK':
        client.send(nickname.encode('ascii'))
      else:
        print(message)
    except:
      # Close Connection When Error
      print('An error occured!')
      client.close()
      break


# Sending Messages To Server
def write():
  while True:
    message = f'{nickname}: {input("")}'
    client.send(message.encode('ascii'))


if __name__ == "__main__":
  receive_thread = threading.Thread(target=receive)
  receive_thread.start()

  write_thread = threading.Thread(target=write)
  write_thread.start()