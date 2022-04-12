# Exercise 2 Template

# Do not modify the file name or function header

# Adds e to mylist and returns the resulting list
def list_add(mylist, e):
	# Your code here
	if type(e) is not int:
		raise TypeError("el numero a añadir es nulo")	#Evitamos que el dato 'e' sea nulo
	
	mylist.append(e)					#Añadimos e a la lista
	

	return mylist						#devolvemos la lista actualizada

# Removes the first occurrence of e in mylist and returns the resulting list 
def list_del(mylist, e):
	# Your code here
	if type(e) is not int:
		raise TypeError("el numero a añadir es nulo")  	#Evitamos que el dato 'e' sea nulo

	if not mylist:
		print("Error: la lista esta vacia")		#Evitamos que la lista este vacia
		quit()

	mylist.remove(e)					#eliminamos de la lista el dato 'e'

	return mylist						#devolvemos la lista actualizada

# Adds the tuple t (value, key) to mydict and returns the resulting dictionary
def dict_add(mydict, t):
	# Your code here


	if type(t) is not tuple:
		raise TypeError("el numero a añadir es nulo o no es una tupla")	#Evitamos que el dato 't' no sea una tupla

	if not len(t)==2:
		print("Error: la tupla no es de dos elementos")		#Evitamos que la lista este vacia
		quit()

	mydict[t[0]] = t[1]					#añadimos la tupla al diccionario

	return mydict						#devolvemos el diccionario actualizado

	
