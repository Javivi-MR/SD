import socket

# HOST = 'localhost'
REMOTE_HOST = '127.0.0.1'
REMOTE_PORT = 1024
REMOTE_ADDR = (REMOTE_HOST, REMOTE_PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Sending a message...")
buffer = "A message.".encode("utf-8")
s.sendto(buffer, REMOTE_ADDR)



s.close()
