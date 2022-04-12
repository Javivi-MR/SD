import argparse
import random
import socket

def main(host, port, n):
    # ...
	ADDR = (host,port)
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 	#Creamos socket
	belowcount = 0											# creamos un contador llamado belowcount
	for i in range(0,n):									# bucle desde el 0 hasta n (siendo n el numero de puntos que deseamos)
		x = random.uniform(0,1)								# x = a un numero random entre 0 y 1
		y = random.uniform(0,1)								# y = a un numero random entre 0 y 1	
	
		punto = str((x,y))									# pasamos punto al formato que se nos pide
		buffer = punto.encode("utf-8")						
	
		s.sendto(buffer, ADDR)								# mandamos al servidor el punto

		buffer, ADDR = s.recvfrom(1024)						# recibimos mensaje del servidor
		
		if (buffer.decode("utf-8") == "below"):				# si el mensaje recibido es igual a "below"
			belowcount = belowcount + 1							#incrementamos en 1 el contador belowcount

	pi = 4 * (belowcount/n)									# la varible pi sera igua a 4 * (belowcount/n)

	print (pi)												# mostramos la aproximación de pi

	buffer = "exit".encode("utf-8")							
	s.sendto(buffer, ADDR)									# mandamos al servidor "exit"

	s.close()												# cerramos el socket

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=1024, help="remote port")
    parser.add_argument('--host', default='localhost', help="remote hostname")
    parser.add_argument('--number', default=100000, help="number of random points to be generated")
    args = parser.parse_args()

    main(args.host, args.port, args.number)
