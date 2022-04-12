# Exercise 4 Template
import os
# Do not modify the file name or function header

# Return the size of the file and words ending in 's'
def get_file_info(filename):
	# Your code here
	
	if type(filename) is not str:						#verficamos que filename no sea una cadena
		raise TypeError ("filename no es una cadena o es nulo")
	
	size = 0								#definimos size como un entero
	wordlist = []								#definimos un array para almacenar las palabras

	try:									#si no se produce error:
	
		with open(filename, "r") as fp:						#abrimos el archivo.txt como 'fp'
		
			linea = fp.readline()						#linea toma el valor de un string de la linea que contenia el fichero
		
			size = len(linea)						#le damos a size el valor de cuantos caracteres hay
			print (size)							
			
			m = linea.split()						#le damos a m el valor de un array de strings con cada una de las palabras que formaba linea.
			
			i = 0								#le damos a i el valor 0
			
			while i < len(m):						#mientras que i es menor que la longitud de m (el numero de palabras que contiene la frase) hacer:
			
				if m[i][len(m[i])-1] == 's':					#si la letra del final de la palabra es 's', hacer
					wordlist.append(m[i])						#añadimos la palabra al array
				i=i+1								#aumentamos el valor de i por uno (saltamos a la siguiente palabra)
				
		return (size, wordlist)								#devolvemos size y wordlist
	except IOError:								#si se produce un fallo hacer:
		print("el fichero no existe")						#mostramos por salida estandar "el fichero no existe"
	finally:								#finalmente
		fp.close()								#cerrar el fichero.
