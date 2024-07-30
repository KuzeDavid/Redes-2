import datetime

# Obtiene la fecha de nacimiento del usuario
fecha_nacimiento_str = input("Ingresa tu fecha de nacimiento (en formato dd/mm/aaaa): ")

# Convierte la cadena de fecha en un objeto datetime
fecha_nacimiento = datetime.datetime.strptime(fecha_nacimiento_str, "%d/%m/%Y")


#fecha_actual = datetime.datetime.now()
destinofinal= datetime.datetime.strptime("08/03/2023","%d/%m/%Y")
# Calcula la cantidad de días vividos hasta la fecha en la que se elegio el ejercicio
dias_vividos = (destinofinal - fecha_nacimiento).days

# Imprime el resultado
print("Has vivido", dias_vividos, "días.")
ejercicio= dias_vividos % 3
print("Ejercicio: ",ejercicio)



'''
# Function to return gcd of a and b
def gcd(a, b):
    if (a == 0):
        return b;
    return gcd(b % a, a);


# Print generators of n
def printGenerators(n):
    # 1 is always a generator
    print("1", end=" ");

    for i in range(2, n):

        # A number x is generator
        # of GCD is 1
        if (gcd(i, n) == 1):
            print(i, end=" ");


# Driver Code
n = 10;
printGenerators(n);
'''