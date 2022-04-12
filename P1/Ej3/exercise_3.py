# Exercise 3 Template

# Do not modify the file name or function header

# Retuns a list with the prime numbers in the [a, b] interval
def prime(a, b):
	# Your code here
	primes = []								#definimos un array

	if type(a) is not int:
		raise TypeError("el numero a no es un entero o es nulo")	#evitamos que a sea nulo o no entero
	
	if type(b) is not int:
		raise TypeError("el numero b no es un entero o es nulo")	#evitamos que a sea nulo o no entero

	for i in range (a, b+1):						#hacemos un bucle donde i tomara los valores desde a hasta b 
		t = 1								#t sera nuestra flag
		for r in range (2,i):						#hacemos un bucle donde r tomara los valores desde 2 hasta i-1
			if i % r == 0:						#buscamos si tiene algun divisor
				t = 0						#si lo tiene ponemos nuestra flag a 0
		if t == 1:							#al llegar aqui, fuera del bucle, si nuestra flag es 1 signidica que no encontro ningun divisor
			primes.append(i)					#asi que añadimos es numero
	# ...

	return primes								#returneamos el array
