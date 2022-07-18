def FunctionReto1():
    precio_huevos = int(input("Digite el precio de los huevos: "))
    
    precio_leche = int((precio_huevos*2) + 4)
    precio_cafe =  int((precio_leche + precio_huevos) / 5)

    categoria = ""
    if precio_cafe > 0 and precio_cafe <= 20:
        categoria = "uno"
    elif precio_cafe >= 21 and precio_cafe <= 30:
        categoria = "dos"
    elif precio_cafe >= 31 and precio_cafe <= 50:
        categoria = "tres"
    elif precio_cafe > 50:
        categoria = "cuatro"

    print("{} {} {}\n{}".format(precio_huevos,precio_leche,precio_cafe,categoria))

FunctionReto1()
