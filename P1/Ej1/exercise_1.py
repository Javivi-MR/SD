# Exercise 1 Template

# Do not modify the file name or function header

# Return the sum of those parameters that contain an even number
def accum(x, y, z):
	# Your code here
	sum = 0
	if type(x) is not int:
		raise TypeError("x no es entero") #Verificamos que x es un entero
	if type(y) is not int:
		raise TypeError("y no es entero") #Verificamos que y es un entero
	if type(z) is not int:
		raise TypeError("z no es entero") #Verificamos que z es un entero

	if x%2 == 0:				  #si x es divisible entre 2 (es par) hacer:
    		sum=x+sum			  #hacemos sum=x+sum
	if y%2 == 0:				  #si y es divisible entre 2 (es par) hacer:
    		sum=y+sum			  #hacemos sum=y+sum
	if z%2 == 0:				  #si z es divisible entre 2 (es par) hacer:
    		sum=z+sum			  #hacemos sum=y+sum
	# ...

	return sum				  # devolvemos sum que sera la suma de los numeros que hayan sido pares


 

	


