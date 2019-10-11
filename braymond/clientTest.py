import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.43.248', 8081))
output = 'I am CLIENT'
client.sendall(output.encode('utf-8'))
from_server = client.recv(4096)
client.close()
print(from_server.decode('utf-8'))