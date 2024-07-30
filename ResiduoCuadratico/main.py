from datetime import datetime

# Pide al usuario que ingrese su fecha de nacimiento
fecha_nacimiento = input("Ingrese su fecha de nacimiento en formato dd/mm/yyyy: ")

# Convierte la entrada del usuario en un objeto datetime
fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%d/%m/%Y')

# Obtiene la fecha actual
fecha_actual = datetime.now()

# Calcula la cantidad de días transcurridos entre ambas fechas
dias_transcurridos = (fecha_actual - fecha_nacimiento).days

# Imprime la cantidad de días transcurridos
print("Han pasado {} días desde tu fecha de nacimiento hasta hoy.".format(dias_transcurridos))
# Convierte el dato dias transcurridos en entero para poderle sacar el modulo
asignado = int(dias_transcurridos) % 3

print("El ejercicio que te toca realizar con su numero de dias que serian", (dias_transcurridos),
      " seria el siguiente: ")
# se menciona al usuario que algoritmo programara conforme a sus dias desde nacimiento hasta ahora

if asignado == 0:
    print("Ha sido asignado el 'buscaminas' como algoritmo para realizar en la practica 1")
elif asignado == 1:
    print("Ha sido asignado el 'Gato Dummy' como algoritmo para realizar en la practica 1")
elif asignado == 2:
    print("Ha sido asignado 'Memoria' como algoritmo para realizar en la practica 1")