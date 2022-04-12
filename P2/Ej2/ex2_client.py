import argparse
import socket
import os


def main(host, port, filein, fileout):
    # ...
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 	# Creamos socket
	dir_remota = (host,port)
	s.connect(dir_remota)									# nos conectamos al servidor
	
	filei = open(filein, 'r') 								# Abrimos el fichero filein.txt en modo lectura

	datos = filei.read()									# Guardamos su contenido en datos

	filei.close()											# Cerramos el fichero filein.txt

	buffer = datos.encode("utf-8")							# Mandamos al servidor los datos
	s.send(buffer)	

	buffer = s.recv(512)									# Recibimos el numero de palabras con a
	numPalabras = int(buffer.decode("utf-8"))	

	buffer = s.recv(512)									# Recibimos una string en forma de lista de palabras con a
	palabras = buffer.decode("utf-8")


	palabras = palabras.replace("'","")						# Eliminamos caracteres conflictivos para dejar solo las palabras con espacios separandolas
	palabras = palabras.replace(",","")						# Eliminamos caracteres conflictivos para dejar solo las palabras con espacios separandolas
	palabras = palabras.replace("[","")						# Eliminamos caracteres conflictivos para dejar solo las palabras con espacios separandolas
	palabras = palabras.replace("]","")						# Eliminamos caracteres conflictivos para dejar solo las palabras con espacios separandolas

	palabras = palabras.split()								# Recreamos la lista con las palabras con a

	# Activar prints para comprobar si el nÃºmero de palabras y la lista es la esperada			
	#print(numPalabras)									
	#print(palabras)

	fileo = open(fileout, 'w')								# Abrimos el fichero fileout.txt en modo escritura
	
	for i in range(len(palabras)):
		fileo.write(palabras[i] + "\n")						# Escribimos en el fichero una palabra en cada linea

	fileo.close()											# Cerramos el fichero fileout.txt

	s.close()												# Cerramos el socket

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=1024, help="remote port")
    parser.add_argument('--host', default='localhost', help="remote hostname")
    parser.add_argument('--filein', default='filein.txt', help="file to be read")
    parser.add_argument('--fileout', default='fileout.txt', help="file to be written")
    args = parser.parse_args()

    main(args.host, args.port, args.filein, args.fileout)
