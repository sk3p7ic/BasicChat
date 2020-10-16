"""
BasicChat-Server
"""
import socket, threading
import bc.message

class Client:
  def __init__(self, client_socket, client_id, client_ip, client_name):
    self.client_socket = client_socket
    self.client_id = client_id
    self.client_ip = client_ip
    self.client_name = client_name

  def startClient(self):
    print(f"Hello from {self.client_name}")
    # Create message to send user ID to client
    m = bc.message.Message(0, bc.message.MsgTypes.MSG_CHID,
                           str(self.client_id).zfill(4))
    self.client_socket.send(m.makeHeader()) # Send the header to client
    self.client_socket.send(m.getMsg()) # Send the user ID to client

  def getClientInfoAsDict(self):
    return {"id": self.client_id, "ip": self.client_ip, "name":self.client_name}

class Server:
  clients = [] # Stores the clients

  def __init__(self, port):
    self.port = port # The port the server will listen on
    self.next_id = 1 #  Start at 1 because server has ID 0
  
  def startListener(self):
    print("CREATING NEW LISTENER...") # Create the listener socket object
    self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the listener
    self.listener.bind((socket.gethostname(), self.port))
    # Start listening
    self.listener.listen(10)
    print(f"LISTENING ON PORT {self.port}")
    while True:
      (client, address) = self.listener.accept()
      print(f"CONNECTION FROM {address} STARTED.")
      header = client.recv(50).decode().split('\n')
      if header[1].split(' ')[1] != bc.message.MsgTypes.MSG_HEAD.name:
        print("ERROR: INCORRECT HEADER")
        print(header)
        print(header[1].split(' ')[1])
        client.close()
      else:
        name = client.recv(int(header[2].split(' ')[1])).decode()
        self.onClientConnect(client, address, name)
  
  def onClientConnect(self, client, address, name):
    client = Client(client, self.next_id, address, name)
    self.clients.append(threading._start_new_thread(client.startClient, ()))
    self.next_id += 1

def start():
  server = Server(1337)
  server.startListener()

start()