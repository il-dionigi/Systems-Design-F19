import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('172.20.10.2', 8080))
output = 'I am CLIENT'
client.sendall(output.encode('utf-8'))
from_server = client.recv(4096)
client.close()
print(from_server.decode('utf-8'))
