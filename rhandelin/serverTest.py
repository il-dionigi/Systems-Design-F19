import socket
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serv.bind(('192.168.43.55', 8080))
serv.listen(5)
while True:
	conn, addr = serv.accept()
	from_client = ''
	while True:
		data = conn.recv(4096)
		if not data: break
		from_client += data.decode('utf-8')
		print(from_client)
		output = 'I am SERVER'
		conn.send(output.encode('utf-8'))
	conn.close()
	print('client disconnected')