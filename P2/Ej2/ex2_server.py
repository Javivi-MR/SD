import argparse
import socket
import os
import time


def main(host, port):
    # ...
	s_escuchar = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	# Creamos socket
	s_escuchar.bind((host, port))									# asignamos ip e puerto
	
	s_escuchar.listen() #Esperando al cliente
	
	s_del_cliente, addr_cliente = s_escuchar.accept() #Cliente nuevo

	buffer = s_del_cliente.recv(512)		# Recibimos el contenido del fichero
	
	datos = buffer.decode("utf-8")			# los movemos a datos
	
	datos = datos.split()					# los dividimos en una lista de palabras, ej ("hola que tal -> ["hola" , "que" , "tal"])
	

	letrasAcount = 0						# Contador de letra a en palabras
	palabras = []							# Lista para palabras con la a

	for i in range (len(datos)):				#bucle para movernos de palabra en palabra
		for j in range (len(datos[i])):				# Buecle para overnos de letra en letra (de la palabra seleccionada en el bucle superior)		
			if(datos[i][j] == 'a'):					# Si la letra es 'a'
				letrasAcount = letrasAcount + 1			#aumentamos en uno la variable letrasAcount
		
		if(letrasAcount > 0):						# Si la variable letrasAcount es > que 0, significa que esa palabra contiende al menos 1 a
			palabras.append(datos[i])				# Metemos en la lista esa palabra
			letrasAcount = 0						# Reseteamos el contador a 0
			
	buffer = str(len(palabras)).encode("utf-8")		# Enviamos el nÃºmero de palabras con a como string
	s_del_cliente.send(buffer)
	
	time.sleep(0.05)								# Paramos el sistema para enviar a parte la lista como string

	buffer = str(palabras).encode("utf-8")			# Enviamos la lista de palabras con a
	s_del_cliente.send(buffer)



	s_escuchar.close()								# Cerramos los sockets
	s_del_cliente.close()							# Cerramos los sockets
	

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=1024, help="listening port")
    parser.add_argument('--host', default='localhost', help="hostname")
    args = parser.parse_args()

    main(args.host, args.port)
