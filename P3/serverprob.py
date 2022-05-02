
from bottle import run, request, response, get, post, put, delete
import json


with open("database.json","r") as f: #Nos conectamos con el json en modo lectura
	database = json.load(f)     #Leemos el JSON y lo convertimos en un diccionario

############################################### CLASES #####################################################


class Sala:
	def __init__ (self, roomId_, capacity_, resources_):
		self.roomId = roomId_
		self.capacity = capacity_
		self.resources = resources_

class Reserva:
	def __init__(self, bookingId_, roomId_, dni_, date_, startTime_, endTime_):
		self.bookingId = bookingId_
		self.roomId = roomId_
		self.date = date_
		self.startTime = startTime_
		self.endTime = endTime_
		self.DNI = dni_

class Usuarios:
	def __init__(self, dni_, userName_, password_):
		self.DNI = dni_
		self.userName = userName_
		self.password = password_

############################################# FUNCIONES #######################################################

#--------------------------------------------------------------------------------------------------------

def comprobarUs(userName_,password_):
	for i in range (0,len(database["Usuario"])):
		if database['Usuario'][i]['userName'] == userName_ and database['Usuario'][i]['password'] == password_:
			print("¡usuario correcto!")
			return True
	return False			

#--------------------------------------------------------------------------------------------------------

def add_to_json_sala(data):
	with open("database.json", "r+") as f:
		file_data = dict(json.load(f))
		file_data["Sala"].append(data)
		f.seek(0)
		json.dump(file_data,f,indent=4)

#--------------------------------------------------------------------------------------------------------

def consultarSala (roomId):
	data = [roomId]		
	for i in range (0,len(database["Sala"])):
		dic = database["Sala"][i]
		if (dic["roomId"] == roomId):
			data.append(dic["capacity"])
			data.append(dic["resources"])
	return data


#--------------------------------------------------------------------------------------------------------

def existesala(data):
	return True
	# suponemos que el usuario sabe las salas que existen
#--------------------------------------------------------------------------------------------------------

def nuevares(data): #[DNI,roomId,date,startTime,duration]
	bookingId = len(database["Reserva"]) + 1 
	roomId = data[1]
	DNI = data[0]
	date = data[2]
	startTime = data[3]
	duration = 	data[4]
	
	y = {"bookingId":bookingId, "roomId":roomId, "DNI":DNI, "date":date, "startTime":startTime, "duration":duration}
	data.append(bookingId)
	
	database["Reserva"].append(y)

	return y

#--------------------------------------------------------------------------------------------------------
	
def add_to_json_resv(y):
	with open("database.json", "r+") as f:
		file_data = dict(json.load(f))
		file_data["Reserva"].append(y)
		f.seek(0)
		json.dump(file_data,f,indent=4)


#--------------------------------------------------------------------------------------------------------

def listarReserva(DNI):
	data = []
	
	for i in range (0,len(database["Reserva"])):
		res = []
		if(DNI == database["Reserva"][i]["DNI"]):
			res.append(database["Reserva"][i]["bookingId"])
			res.append(database["Reserva"][i]["roomId"])
			res.append(database["Reserva"][i]["date"])
			res.append(database["Reserva"][i]["startTime"])
			res.append(database["Reserva"][i]["duration"])
			data.append(res)
			
	return data


#--------------------------------------------------------------------------------------------------------

def eliminarReserva (bookingId):
	
	flag=1

	#Eliminamos la reserva (si existe) de la base de datos
	for i in range (0,len(database["Reserva"])):
		if (database["Reserva"][i]["bookingId"] == bookingId):
			del database["Reserva"][i]
			flag = 0
			break

	#Sobreescribimos el fichero 
	if (flag == 0):
		with open("database.json", "w") as f:
			file_data = database
			f.seek(0)
			json.dump(file_data,f,indent=4)
	
	return flag


################################################## COMUNICACION ####################################################
		
#--------------------------------------# OPCION 1 #------------------------------------------------#
@post('/addRoom')
def addRoom():

	data = request.json

	username = data[0]
	password = data[1]
	
	roomId = data[2]
	capacity = data[3]
	resources = data[4]

	flag = comprobarUs(username,password)
	if(flag):

		y = {"roomId":roomId, "capacity":capacity, "resources":resources}
		database["Sala"].append(y)
		add_to_json_sala(y)

		return json.dumps({"estado": "0", "datos": [roomId, capacity, resources]})
	else:
		info = "¡Usuario Incorrecto!"
		return json.dumps({"estado": "1", "datos": info})

#--------------------------------------# OPCION 2 #------------------------------------------------#

@get('/showInformationRoom/')
@get('/showInformationRoom/<roomId>')
def showinfo(roomId=0):

	data = request.json

	username = data[0]
	password = data[1]

	flag = comprobarUs(username,password)
	if(flag):

		roomId = int(data[2])

		info = consultarSala(roomId)

		return json.dumps({"estado": "0", "datos": info})
	else:
		info = "¡Usuario Incorrecto!"
		return json.dumps({"estado": "1", "datos": info})

#--------------------------------------# OPCION 3 #------------------------------------------------#
@post('/addBooking')
def addbooking():


	data = request.json
		


	username = data[0]
	password = data[1]
	flag1 = comprobarUs(username,password)

	if(flag1):

		flag2 = existesala(data) #consulta si la reserva para esa sala se encuentra disponible (devuelve true si lo esta y false si no)
			
		if(flag2):
			dataux = [data[2],data[3],data[4],data[5],data[6]]
			y = nuevares(dataux) #[DNI,roomId,date,startTime,duration]
			add_to_json_resv(y)
			return json.dumps({"estado": "0", "datos":dataux})

	else:
		return json.dumps({"estado": "1", "datos": "Usuario erroneo"})
		

#--------------------------------------# OPCION 4 #------------------------------------------------#

@get('/showBookings/')
@get('/showBookings/<DNI>')
def showbookings(DNI):

	data = request.json

	username = data[0]
	password = data[1]

	res = comprobarUs(username,password)
	if(res):
		DNI = data[2]

		info = listarReserva(DNI)

		return json.dumps({"estado": "0", "datos": info})
	else:
		return json.dumps({"estado": "1", "datos": "Usuario no valido"})

#--------------------------------------# OPCION 5 #------------------------------------------------#

@delete('/deleteBooking/')
@delete('/deleteBooking/<bookingId>')
def deletebooking(bookingId):
	data = request.json

	username = data[0]
	password = data[1]

	flag = comprobarUs(username,password)
	if(flag):
		bookingId = data[2]
		flag2 = eliminarReserva(bookingId)

		if(flag2 == 0):
			return json.dumps({"estado": "0", "datos": "Reserva eliminada con exito"})
		else:
			return json.dumps({"estado": "1", "datos": "No se ha encontrado el Id de reserva"})
	else:
		return json.dumps({"estado": "1", "datos": "Usuario no valido"})


#-----------------------------------# Fin comunicación #---------------------------------------------#

def main():
    run(host='localhost', port=8080, debug=True)

# Llama a main()
if __name__ == '__main__':
	main()
