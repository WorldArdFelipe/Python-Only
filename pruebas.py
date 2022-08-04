import pandas as pd
from matplotlib import pyplot as plt

datosCovid = pd.read_csv("lacteos_datos.csv")
print(datosCovid["vendedor"])

datosCovid["ventas"] = datosCovid["valor_unidad_producto"] * datosCovid["cantidad_vendida"]

prueba = pd.DataFrame({
    "nombre" : datosCovid["vendedor"],
    "productos" : datosCovid["producto"],
    "cantidad_ventas" : datosCovid["cantidad_vendida"],
    "fechas" : datosCovid["fecha"],
    "ventas": datosCovid["ventas"]
})

#prueba.set_index('nombre',inplace=True)



print(prueba.groupby(by=['nombre','productos'])["ventas"].sum().reset_index())

"""
plt.xlabel("hola")
plt.ylabel("hola")
plt.show()
"""