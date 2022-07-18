import json

entrada_datos = input("")
entrada_jugadores = input("")

lista = []
diccionario = json.loads(entrada_datos)
count = 0

for i in entrada_jugadores:
    for x,y  in diccionario.items():
        if i == x:
            lista.append(i)
            count += y

print(count)
print(*lista)


dsd3h46