import threading
import socket

# Initial user setup, prompting for a nickname and potentially a password for admin users
nickname = input('Choose a nickname: ')
if nickname == 'admin':
  password = input('Enter password for admin: ')

# Flag to control the stopping of threads
stop_thread = False

# Establishing a connection to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

# def receive():
#   """Handles receiving messages from the server."""
#   while True:
#     global stop_thread
#     if stop_thread:
#       break
#     try:
#       message = client.recv(1024).decode('ascii')
#       # If 'NICK' Send Nickname
#       if message == 'NICK':
#         client.send(nickname.encode('ascii'))
#         next_message = client.recv(1024).decode('ascii')
#         if next_message == 'PASS':
#           client.send(password.encode('ascii'))
#           if client.recv(1024).decode('ascii') == 'REFUSE':
#             print('Connection was refused. Wrong password!')
#             stop_thread = True
#         elif next_message == 'BAN':
#           print('Connection refused because of ban')
#           client.close()
#           stop_thread = True
#       else:
#         print(message)
#     except:
#       # Close Connection When Error
#       print('An error occured!')
#       client.close()
#       break

def receive():
  """Handles receiving messages from the server."""
  global stop_thread
  while not stop_thread:
    try:
      message = client.recv(1024).decode('ascii')
      if message == 'NICK':
        client.send(nickname.encode('ascii'))
        handle_admin_verification()
      else:
        print(message)
    except Exception as e:
      print('An error occurred:', e)
      client.close()
      break

def handle_admin_verification():
  """Handles additional verification steps if the user is recognized as an admin by the server."""
  next_message = client.recv(1024).decode('ascii')
  if next_message == 'PASS':
    client.send(password.encode('ascii'))
    if client.recv(1024).decode('ascii') == 'REFUSE':
      print('Connection was refused. Wrong password!')
      global stop_thread
      stop_thread = True
  elif next_message == 'BAN':
    print('Connection refused because of ban')
    client.close()
    stop_thread = True


# Sending Messages To Server
# def write():
#   while True:
#     if stop_thread:
#       break
#     message = f'{nickname}: {input("")}'
#     if message[len(nickname)+2:].startswith('/'):
#       if nickname == 'admin':
#         if message[len(nickname)+2:].startswith('/kick'):
#           client.send(f'KICK {message[len(nickname)+2+6:]}'.encode('ascii'))
#         elif message[len(nickname)+2:].startswith('/ban'):
#           client.send(f'BAN {message[len(nickname)+2+5:]}'.encode('ascii'))
#       else:
#         print('Commands can only be executed by the admin!')
#     else:
#       client.send(message.encode('ascii'))


def write():
  """Handles sending messages to the server."""
  while not stop_thread:
    message = f'{nickname}: {input("")}'
    if message[len(nickname)+2:].startswith('/'):
      handle_admin_commands(message)
    else:
      client.send(message.encode('ascii'))


def handle_admin_commands(message):
  """Processes commands intended for admin users like kick and ban."""
  if nickname == 'admin':
    command, _, argument = message[len(nickname)+2:].partition(' ')
    if command == '/kick':
      client.send(f'KICK {argument}'.encode('ascii'))
    elif command == '/ban':
      client.send(f'BAN {argument}'.encode('ascii'))
  else:
    print('Commands can only be executed by the admin!')


if __name__ == "__main__":
  receive_thread = threading.Thread(target=receive)
  receive_thread.start()

  write_thread = threading.Thread(target=write)
  write_thread.start()