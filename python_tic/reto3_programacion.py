#Ingreso de datos - Upper convierte el texto en mayuscula y separa por coma.
letras_entrada = input().upper().split(",")

#Lista Vacia, donde almacena las letras sin repetir.
guardar_letras_sin_repetir = []
guardar_contador_letras = []

#indice deel comienzo de la lista.
letra_comprobacion = letras_entrada[0]

#contador de letras repetidas
contador = 0

#Comienzo de for
for i in range(0,len(letras_entrada)):
    mostrar_letra = letras_entrada[i] #Muestra la letra dependiendo el indice obtenido por el for

    if letra_comprobacion != mostrar_letra:
        guardar_contador_letras.append([letra_comprobacion,contador])
        guardar_letras_sin_repetir.append(letra_comprobacion)   

        contador = 0
        letra_comprobacion = mostrar_letra

    if letra_comprobacion == mostrar_letra:
       contador += 1
#fin contador

#Comprueba si termina el for y el contador tienen algun valor guardado , lo guarda en lista.
if contador != 0:
    guardar_contador_letras.append(contador)
    guardar_letras_sin_repetir.append(letra_comprobacion)

print(*guardar_letras_sin_repetir)
print(*guardar_contador_letras)