import pandas as pd

NAME_ARCHIVE = "prueba_tecnica.xlsx"
INDEX_SHEET = 1
LISTA_COUNTRY = []

def load_archive():
  return pd.read_excel(NAME_ARCHIVE,sheet_name=INDEX_SHEET)

def count_data_na(data):
  data = data.isna().sum()
  return data

def clean_data(data):
  #data = data.fillna(0) # rellena vacios o na a 0
  data =  data.dropna() # elimina columna completa con elemento 0
  return data

def weeknum(data):  
  fecha = data["Fecha de creacion"]
  fecha = pd.to_datetime(fecha)
  fecha.astype('int64').dtypes
  return  fecha.dt.week

def weekday(data):  
  fecha = data["Fecha de creacion"]
  fecha = pd.to_datetime(fecha)
  day = pd.DatetimeIndex(fecha).day
  month = pd.DatetimeIndex(fecha).month
  result = (day - fecha.dt.dayofweek).apply(str)
  test = fecha.dt.month.apply(str) + "-" + result + "-" +fecha.dt.year.apply(str)
  return pd.to_datetime(test)
    
dates = load_archive()
dates = dates.drop(0) #Elimina columna 0 (titulos extras) - only datos
dates.rename(columns = {"País →":"Fecha de creacion"},inplace=True) #Remplaza titulo
count_dates = count_data_na(dates) #contador de elementos vacios
dates = clean_data(dates)

#Agrega nuevas tablas -Info extra
dates["Semana"] = weeknum(dates) 
dates["Fecha inicio semana"] = weekday(dates)


#Crea nuevo dataframe con nuevos valores
dates_filtre =  pd.DataFrame(data={
    'Fecha_Semana' : dates["Fecha inicio semana"],
    'Fuerza_Ventas_Argentina' : dates["Argentina"],
    'Fuerza_Ventas_Brasil' : dates["Brasil"],
    'Fuerza_Ventas_Chile' : dates["Chile"],
    'Fuerza_Ventas_Peru' : dates["Peru"],
    'Fuerza_Ventas_Total' : 0,
})

#Agrupa por columa fecha_semana - aplica sum a varios repetidos 
dates_filtre = dates_filtre.groupby(by = [dates_filtre['Fecha_Semana']]).agg(
    {
        "Fuerza_Ventas_Argentina" : "sum",
        "Fuerza_Ventas_Brasil" : "sum",
        "Fuerza_Ventas_Chile" : "sum",
        "Fuerza_Ventas_Peru" : "sum",
    }
).reset_index()


#Convierte type objet a int
dates_filtre = dates_filtre.astype(
  {"Fuerza_Ventas_Argentina":"int",
  "Fuerza_Ventas_Brasil":"int",
  "Fuerza_Ventas_Chile":"int",
  "Fuerza_Ventas_Peru":"int"}
)

dates_filtre["Fuerza_Ventas_Total"] = dates_filtre.sum(axis=1, numeric_only=True)
#dates_filtre.Fuerza_Ventas_Argentina

#print("Elementos vacios encontrados : \n{} ".format(count_dates))
#dates_filtre.dtypes //saber types de elementos
#dates_filtre.head(20)

dates_filtre.head(30)