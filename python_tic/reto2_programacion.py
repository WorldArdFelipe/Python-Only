pedro_letras = input("")
nestor_letras = input("")
jurado_letras = input("")

puntos_pedro = 0
puntos_nestor = 0
salida = ""

for letra_jurado in jurado_letras:

    if pedro_letras.count(letra_jurado) > 0:
        puntos_pedro +=1
    
    if nestor_letras.count(letra_jurado) > 0:
        puntos_nestor += 1
    
    if(puntos_pedro > puntos_nestor):
        salida += "J"
    elif(puntos_nestor > puntos_pedro):
        salida += "k"
    else:
        salida += "L"

print(salida)