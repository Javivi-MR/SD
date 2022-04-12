import argparse
import socket
import numpy as np


def main(host, port):
    # ...
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	# Creamos socket
	s.bind((host, port))									# asignamos ip e puerto

	buffer, addr_c1 = s.recvfrom(1024)	# Recivimos nombre del player 1
	nombrej1 = buffer.decode("utf-8")
	
	buffer, addr_c1 = s.recvfrom(1024)	# Recivimos tablero del player 1
	tableroj1 = buffer.decode("utf-8")

	buffer, addr_c2 = s.recvfrom(1024)	# Recivimos nombre del player 2
	nombrej2 = buffer.decode("utf-8")
	
	buffer, addr_c2 = s.recvfrom(1024)  # Recivimos tablero del player 2
	tableroj2 = buffer.decode("utf-8")

	tableroj1 = np.matrix(tableroj1) 	# Convertimos a matriz el tablero del player 1
	tableroj2 = np.matrix(tableroj2)	# Convertimos a matriz el tablero del player 2
	
	# Habilitar prints para ver el tablero en forma matriz

	#print(tableroj1)
	#print(tableroj2)

	turno = 1  							# Contador para los turnos
	jugador = 1							# Contador para seleccionar el jugador
	flag = True							# Flag que nos indicara si el juego sigue (true) o termina (False)
	base = 65							# Numero base para restar en las funciones ord()
		
	while(flag):						# Mientras que el juego siga en curso
		t = "Turn " + str(turno)		# t = "Turn <id>" siendo id el numero de turno correspondiente (guardado en la variable turno)
		if(jugador%2 == 1):				# Seleccion del jugador || si se cumple el if (variable jugador es impar) el jugador que ataca es el 1
			s.sendto(t.encode("utf-8"), addr_c1)			# Enviamos al jugador 1 t ("turn <id>")
			buffer, addr_c1 = s.recvfrom(1024)				# Recibimos del jugador la coordenada que desea atacar
			coord = buffer.decode("utf-8")
			if(len(coord)==2):								# Procedemos a conseguir las coordenadas para nuestra matriz: si la longitud de coord es 2 el dato enviado será del tipo (A-J|1-9)
				x = int(coord[1]) - 1						# A x le asignamos el valor de la fila que será en este caso el valor numerico de la coordenada - 1, ej (A9 -> x = 9 - 1) 
			else:											# En este caso podria ser que la coord tuviese longitud 3, será del tipo (A-J|10)  
				x = 9										# En este caso tendremos que darle a x el valor 9, ej (A10 -> x = 10 - 1)

			if(coord[0] == 'A'):		# Ahora distinguiremos la columna seleccionada, para esto compararemos con todas las letras y daremos las siguientes asignaciones
				y = ord('A') - base		# si es A, y = 0. Notese que ord(A) devuelve 65 por lo que 65 - 65 = 0 
			if(coord[0] == 'B'):		
				y = ord('B') - base		# si es B, y = 1. Notese que ord(B) devuelve 66 por lo que 66 - 65 = 1
			if(coord[0] == 'C'):
				y = ord('C') - base		# si es C, y = 2. Notese que ord(C) devuelve 67 por lo que 67 - 65 = 2
			if(coord[0] == 'D'):
				y = ord('D') - base		# si es D, y = 3. Notese que ord(D) devuelve 68 por lo que 68 - 65 = 3
			if(coord[0] == 'E'):
				y = ord('E') - base		# si es E, y = 4. Notese que ord(E) devuelve 69 por lo que 69 - 65 = 4
			if(coord[0] == 'F'):
				y = ord('F') - base		# si es F, y = 5. Notese que ord(F) devuelve 70 por lo que 70 - 65 = 5
			if(coord[0] == 'G'):
				y = ord('G') - base		# si es G, y = 6. Notese que ord(F) devuelve 71 por lo que 71 - 65 = 6
			if(coord[0] == 'H'):
				y = ord('H') - base		# si es H, y = 7. Notese que ord(H) devuelve 72 por lo que 72 - 65 = 7
			if(coord[0] == 'I'):
				y = ord('I') - base		# si es I, y = 8. Notese que ord(I) devuelve 73 por lo que 73 - 65 = 8
			if(coord[0] == 'J'):
				y = ord('J') - base		# si es J, y = 9. Notese que ord(J) devuelve 74 por lo que 74 - 65 = 9
			
			
			if(tableroj2[x,y] == 1):	# vemos si la coordenada elegida cae en 1 o en 0. Si es 1 
				tableroj2[x,y] = 0		# volvemos 0 esa coordenada debido a que el ataque ha sido exitoso
				flag2 = False			# definimos la variable flag2 para la comprobación de si queda algun 1 en la matriz. false por defecto
				for i in range (10):					# Bucle para la comprobar si queda algun 1 en la matriz
					for j in range (10):				# ''	''	 ''      ''   ''   ''    ''  ''    ''  ''
						if(tableroj2[i,j] == 1):		# Si encontrasemos un 1 cambiamos el valor de flag2 a true
							flag2 = True				#
				if (flag2):										# En el caso de encontrar algun 1 (flag2 = True), hay que continuar la partida
					s.sendto("Hit".encode("utf-8"), addr_c1)		# Mandamos al player 1 "Hit"	
					turno = turno + 1								# incrementamos 1 el turno, y no cambiamos jugador para que juegue otra vez el mismo player (player 1)
				else:											# En el caso de no encontrar algun 1 (flag2 = False), hay que acabar la partida
					s.sendto("You win".encode("utf-8"), addr_c1)	# Mandamos al player que realizo el ataque (player 1) "you win" 
					s.sendto("You lost".encode("utf-8"), addr_c2)	# Mandamos al player que recibio el ataque (player 2) "you lost"
					flag = False									# variable Flag = False (el juego ha acabado)
			else:						# si la coordenada elegida cae en 0
				s.sendto("Fail".encode("utf-8"), addr_c1)		# Mandamos al jugador que hizo el ataque (player 1) "Fail"
				turno = turno + 1								# incrementamos 1 el turno
				jugador = jugador + 1							# incrementamos jugador para cambiar de jugador (siguiente turno le tocaria al player 2)

		else:										# Seleccion del jugador || al no cumplirse el if (variable jugador es par) el jugador que ataca es el 2
			s.sendto(t.encode("utf-8"), addr_c2)	# Enviamos al jugador 2 t ("turn <id>")
			buffer, addr_c2 = s.recvfrom(1024)		# Recibimos del jugador la coordenada que desea atacar
			coord = buffer.decode("utf-8")
			if(len(coord)==2):						# Procedemos a conseguir las coordenadas para nuestra matriz: si la longitud de coord es 2 el dato enviado será del tipo (A-J|1-9)
				x = int(coord[1]) - 1				# A x le asignamos el valor de la fila que será en este caso el valor numerico de la coordenada - 1, ej (A9 -> x = 9 - 1)
			else:									# En este caso podria ser que la coord tuviese longitud 3, será del tipo (A-J|10)
				x = 9								# En este caso tendremos que darle a x el valor 9, ej (A10 -> x = 10 - 1)

			if(coord[0] == 'A'):				# Ahora distinguiremos la columna seleccionada, para esto compararemos con todas las letras y daremos las siguientes asignaciones
				y = ord('A') - base				# si es A, y = 0. Notese que ord(A) devuelve 65 por lo que 65 - 65 = 0 
			if(coord[0] == 'B'):
				y = ord('B') - base				# si es B, y = 1. Notese que ord(B) devuelve 66 por lo que 66 - 65 = 1
			if(coord[0] == 'C'):
				y = ord('C') - base				# si es C, y = 2. Notese que ord(C) devuelve 67 por lo que 67 - 65 = 2
			if(coord[0] == 'D'):
				y = ord('D') - base				# si es D, y = 3. Notese que ord(D) devuelve 68 por lo que 68 - 65 = 3
			if(coord[0] == 'E'):
				y = ord('E') - base				# si es E, y = 4. Notese que ord(E) devuelve 69 por lo que 69 - 65 = 4
			if(coord[0] == 'F'):
				y = ord('F') - base				# si es F, y = 5. Notese que ord(F) devuelve 70 por lo que 70 - 65 = 5
			if(coord[0] == 'G'):
				y = ord('G') - base				# si es G, y = 6. Notese que ord(F) devuelve 71 por lo que 71 - 65 = 6
			if(coord[0] == 'H'):
				y = ord('H') - base				# si es H, y = 7. Notese que ord(H) devuelve 72 por lo que 72 - 65 = 7
			if(coord[0] == 'I'):
				y = ord('I') - base				# si es I, y = 8. Notese que ord(I) devuelve 73 por lo que 73 - 65 = 8
			if(coord[0] == 'J'):
				y = ord('J') - base				# si es J, y = 9. Notese que ord(J) devuelve 74 por lo que 74 - 65 = 9
				
			
			if(tableroj1[x,y] == 1):			# vemos si la coordenada elegida cae en 1 o en 0. Si es 1 
				tableroj1[x,y] = 0					# volvemos 0 esa coordenada debido a que el ataque ha sido exitoso
				flag2 = False						# definimos la variable flag2 para la comprobación de si queda algun 1 en la matriz. false por defecto
				for i in range (10):					# Bucle para la comprobar si queda algun 1 en la matriz
					for j in range (10):				# ''	''	 ''      ''   ''   ''    ''  ''    ''  ''
						if(tableroj1[i,j] == 1):		# Si encontrasemos un 1 cambiamos el valor de flag2 a true
							flag2 = True				#
				if (flag2):											# En el caso de encontrar algun 1 (flag2 = True), hay que continuar la partida
					s.sendto("Hit".encode("utf-8"), addr_c2)			# Mandamos al player 2 "Hit"
					turno = turno + 1									# Incrementamos 1 el turno, y no cambiamos jugador para que juegue otra vez el mismo player (player 2)
				else:												# En el caso de no encontrar algun 1 (flag2 = False), hay que acabar la partida
					s.sendto("You win".encode("utf-8"), addr_c2)		# Mandamos al player que realizo el ataque (player 2) "you win" 
					s.sendto("You lost".encode("utf-8"), addr_c1)		# Mandamos al player que recibio el ataque (player 1) "you lost"
					flag = False										# variable Flag = False (el juego ha acabado)
			else:								# si la coordenada elegida cae en 0
				s.sendto("Fail".encode("utf-8"), addr_c2)	# Mandamos al jugador que hizo el ataque (player 2) "Fail"
				turno = turno + 1							# incrementamos 1 el turno						
				jugador = jugador + 1						# incrementamos jugador para cambiar de jugador (siguiente turno le tocaria al player 1)

		
	# Habilitar prints para ver estado final de los tableros en forma matriz
	#print(tableroj1)
	#print(tableroj2)

	s.close()

	
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=1024, help="listening port")
    parser.add_argument('--host', default='localhost', help="hostname")
    args = parser.parse_args()

    main(args.host, args.port)
