import argparse
import socket
import math

def f(x):
	return math.sqrt(1 - math.pow(x, 2)) 					# devuelve raiz(1-x^2)

def main(host, port):
    # ...
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 	# Creamos socket
	s.bind((host, port))									# asignamos ip e puerto

	bufferi ="rndm".encode("utf-8")							# inicializamos bufferi con basura
	
	while (bufferi.decode("utf-8") != "exit"):				# Mientras que bifferi no sea "exit" hacer:

		bufferi, addr_c = s.recvfrom(1024)						# Recibimos datos del cliente (punto o exit) || si es un punto tiene la siguiente forma '(x,y)', ejemplo '(0.56,0.36)'
		
		if (bufferi.decode("utf-8") != 'exit'):					# si lo recibido no es exit hacemos: 

			punto = bufferi.decode("utf-8").split(",")			# creamos una lista tal que: si el punto es '(x,y)' -> ['(x','y)']
					
			punto[0] = punto[0].replace("(","")					# eliminamos el caracter '(' obteniendo en la primera posicion de la lista 'x'	
			punto[1] = punto[1].replace(")","")					# eliminamos el caracter ')' obteniendo en la primera posicion de la lista 'y'
							
			x = float(punto[0])									# le asignamos a la variable x el valor de la primera posicion de la lista convirtiendolo en flotante
			y = float(punto[1])									# le asignamos a la variable y el valor de la segunda posicion de la lista convirtiendola en flotante
					
			if (x > 1 or x < 0) or (y > 1 or y < 0):			# si el punto esta fuera de rango (x o y menor que 0 o mayor que 1) hacer:
				buffero = "error"									#mandamos al cliente "error"
				s.sendto(buffero.encode("utf-8"), addr_c)
			else:												# si el punto esta dentro de rango
				if y<f(x):											# si y es menor que lo que devuelve la funcion f al pasarle x
					buffero = "below"									#mandamos al cliente "below"
					s.sendto(buffero.encode("utf-8"), addr_c)
				else:												# si y es mayor que lo que devuelve la funcion f al pasarle x
					buffero = "above"									#mandamos al cliente "above"
					s.sendto(buffero.encode("utf-8"), addr_c)
	
	s.close()												# cerramos el socket
	

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=1024, help="listening port")
    parser.add_argument('--host', default='localhost', help="hostname")
    args = parser.parse_args()

    main(args.host, args.port)
