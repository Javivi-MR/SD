import socket

# HOST = 'localhost'
HOST = '127.0.0.1'
PORT = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))

print("Waiting for messages...")
# addr_c -> (host_c, port_c)
# buffer, (host_c, port_c) = s.recvfrom(1024)
buffer, addr_c = s.recvfrom(512)

print("Received message: '" + buffer.decode("utf-8") + "'")
print("From the client in the address: " + str(addr_c))


s_cliente.send("Hola, cliente, soy el servidor".encode("utf-8"))

s.close()
