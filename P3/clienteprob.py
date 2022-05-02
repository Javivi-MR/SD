import json
from bottle import route, run, template, post, request, response, put
import requests

def main():

	server = "http://localhost:8080"
	userName = input("Introduzca un usuario: ")			# Para poder usar añadir usuario manualmente en el json o usar usuario "admin"
	password = input("Introduzca una contraseña: ")		# Para poder usar añadir contraseña manualmente en el json o usar contraseña "admin"
	DNI = input("Introduzca su DNI: ")					# añadimos el dni

	op=True

	while (op):	############################################### MENU DISPLAY #########################################################################################################################

		#Mostrar Menu
		
		opcion = int(input('Menu   \n1.Anadir Sala\n2.Mostrar informacion sala\n3.Aniadir reserva\n4.Listar reservas\n5.Eliminar reservas\n6.Exit\n\nEscoge una de las opciones escribiendo el numero correspondiente: '))# Seleccionar opcion

		########### 1. Añadir Sala ##################################################################################################################################################################
		if(opcion == 1):

			roomId = int(input("Escoge un numero de sala: "))
			capacity = int(input("Escoge la capacidad de la sala: "))
			resources = input("Escoge los recursos necesarios para la sala(Recursos disponibles: proyector, pizarra, rotuladores, altavoces, micrófono, puntero láser):\n").split(', ')

			sala_list = [userName,password,roomId,capacity,resources]
			
			response = requests.post(url=server + '/addRoom', json=sala_list)	#comunicacion con el servidor

			

			datos_sala = json.loads(response.text)
	
			if (datos_sala["estado"] == '0'):
			
				texto = '¡Sala creada!\n'
				sala_list = datos_sala['datos']

				separa_recursos = str(sala_list[2]).replace("[","")
				separa_recursos = separa_recursos.replace("]","")
				separa_recursos = separa_recursos.replace("'","")

				text= '\n\nSala creada\n' + 'Sala: ' +str(sala_list[0])+ '\nCapacidad: ' +str(sala_list[1])+ '\nRecursos: ' + separa_recursos + '\n\n'

				print (text)
			else:
				print (datos_sala["datos"])

		#########################################################################################################################################################################

		########### 2. Mostrar info de una sala ####################################################################################################################################
		
		elif(opcion == 2):

			roomId = int(input("Escoge un numero de sala: "))			
		
			data = [userName,password,roomId]

			response = requests.get(url=server + '/showInformationRoom/' + str(roomId), json=data)

			datos_sala = json.loads(response.text)
			if (datos_sala["estado"] == '0'):
				sala_list = datos_sala['datos']

				separa_recursos = str(sala_list[2]).replace("[","")
				separa_recursos = separa_recursos.replace("]","")
				separa_recursos = separa_recursos.replace("'","")

				text= '\n\nInformacion sobre la sala: \n' + 'Numero de Sala: ' +str(sala_list[0])+ '\nCapacidad: ' +str(sala_list[1])+ '\nRecursos: ' + separa_recursos + '\n\n'
		
				print (text)
			else:
				print (datos_sala["datos"])

		####################################################################################################################################################################
		
		####################### 3. Crear reserva ##############################################################################################################################

		elif(opcion == 3):

			roomId = int(input("Escoge una sala: "))			
			date = input("Escoge una fecha (Formato: dd/mm/aaaa): ")
			startTime = input("Escoge una hora de inicio(Formato: hh:mm): ")
			duration = int(input("Escoge la duracion de la reserva en minutos(Ejemplo: 60 (1 hora)): "))

			datos_list = [userName,password,DNI,roomId,date,startTime,duration]

			response = requests.post(url=server + '/addBooking', json=datos_list)

			datos_reserva = json.loads(response.text)

			if (datos_reserva["estado"] == '0'):
				reservcomp = datos_reserva["datos"] #[DNI,roomId,date,startTime,duration,bookingId]

				print("¡Reserva completada!\n")
			
				text = "Id de la reserva: " + str(reservcomp[5]) + "\nId de la sala: " + str(reservcomp[1]) + "\nDNI: " + str(reservcomp[0]) + "\nfecha: " + str(reservcomp[2]) + "\nhora de comienzo: " + str(reservcomp[3]) + "\nduracion: " + str(reservcomp[4]) + "\n"
				print(text)

			else:
				print(datos_reserva["datos"])
		####################################################################################################################################################################
			
		####################### 4. Listar reservas ###############################################################################################################################

		elif(opcion == 4):
			
			data = [userName,password,DNI]
            
			
			response = requests.get(url=server + '/showBookings/' + str(DNI), json=data)

			datos_reserva = json.loads(response.text)
		
			if (datos_reserva["estado"] == '0'):		

				reserva_list = datos_reserva['datos']
		        
				print ("Reservas del usuario con dni: " + DNI)

				for i in range (0,len(reserva_list)):
		            
					text= '\n\nInformacion sobre la reserva: \n' + 'ID reserva: ' + str(reserva_list[i][0]) + '\nSala: ' + str(reserva_list[i][1]) + '\nFecha: ' + str(reserva_list[i][2]) + '\nHora Inicio: ' + str(reserva_list[i][3]) + '\nDuracion: ' + str(reserva_list[i][4]) +'\n\n'
					print (text)

			else:
				print (datos_sala["datos"])

		#######################################################################################################################################################################
		
		########### 5. Eliminar reserva #######################################################################################################################################
		elif(opcion == 5):
			bookingId = int(input("Escoge el identificador de la reserva que desea eliminar: "))
			response = requests.delete(url=server + '/deleteBooking/' + str(bookingId), json=[userName,password,bookingId])

			datos_reserva = json.loads(response.text)


			print(datos_reserva['datos'])
		

		### 6. Exit ###########################################################################################################################################################
		elif(opcion == 6):

			print("Hasta la proxima :)")
			op=False

if __name__ == '__main__':
	main()
