import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import os

"""
types = (
    0 = excel (Default)
    1 = csv
)
"""

def load_archive(name_archive,type = "excel",page_index = "", header_get = 0):
    if type == "csv":
        return pd.read_csv(name_archive)
    else:
        if header_get == 0 :
            if len(page_index) > 0:
                return pd.read_excel(name_archive,sheet_name = page_index)
            else:
                return pd.read_excel(name_archive)
        else:
            return pd.read_excel(name_archive,sheet_name = page_index,header = header_get)

#Get count dates na
def get_dates_na(date):
    return date.isna().sum()

def get_value_counts(date):
    return date.value_counts()

def get_count_total_dates_na(date):
    return date.isna().sum().sum()

#Get data only values na
def get_only_dates_na(date):
    return date[date.isna().any(True)]

#Get info dates
def get_dates_info(date):
    return date.info()

#get count column and files (0,0)
def get_dates_shape(date):
    return date.shape

#get dates duplicated
def get_dates_duplicated(date):
    return date[date.duplicated()]

#get datesd duplocated_by_group
def get_dates_duplicated_group(date,group):
    return date[date.duplicated(subset=group,keep =False)]

#get unique values
def get_values_uniques(date):
    return date.unique()

def get_count_value_unique(date):
    return date.nunique()

#Get descript dates
def get_dates_descrip(date):
    return date.describe().T

#get porcent values na
def get_porcent_values_na(data):
    cell = np.product(get_dates_shape(data))
    total = get_dates_na(data).sum()

    return (total/cell) * 100

def get_dates_median(data):
    return data.median()

def get_dates_max(data):
    return data.max()

def get_dates_min(data):
    return data.min()

def get_dates_first_cuartil(data):
    return data.quantile(0.25)

def get_dates_three_cuartil(data):
    return data.quantile(0.75)

def get_dates_intercuartil(data):
    q_first = get_dates_first_cuartil(data)
    q_three = get_dates_three_cuartil(data)

    q_inter = q_three-q_first
    return q_inter

#convert types dates
def set_convert_dtypes(date,list):
    return date.astype(list)

#delete column especific
def set_delete_column(date,index):
    return date.drop(index)

#replace title column
def set_change_name_column(date,column):
    return date.rename(columns = column,inplace=True)

#detele files duplicate
def set_delete_duplicate(date):
    return date.drop_duplicates(keep='last', inplace= True)

#delete column is na values
def set_delete_column_is_na(data):
    return data.dropna()

#change value is na to value x
def set_value_is_na(data,value = 0):
    return data.fillna(value,inplace = True)


def change_value_duplicate(data,group,column,value,type = "last"):
    data.loc[data.duplicated(subset=group, keep=type), column] = value

def show_info_dates_extra1(data):
    p_q =  get_dates_first_cuartil(data)
    t_q =  get_dates_three_cuartil(data)
    i_q =  get_dates_intercuartil(data)
    m =  get_dates_median(data)
    v_mn =  get_dates_min(data)
    v_mx =  get_dates_max(data)

    print("Primer Cuartil : {} \nTercer Cuartil : {} \nInter Cuartil : {}\nMinima : {}\nMediana : {}\nMaxima : {}".format(p_q,t_q,i_q,v_mn,m,v_mx))

# show box outliners of value atipicos
def show_box_outliers(data):
    plt.boxplot(data,vert=False)
    plt.show()


def convert_month_to_number(data):
    month = {
        'ENERO' : 1,
        'FEBRERO' : 2,
        'MARZO' : 3,
        'ABRIL' : 4,
        'MAYO' : 5,
        'JUNIO' : 6,
        'JULIO' : 7,
        'AGOSTO' : 8,
        'SEPTIEMBRE' : 9, 
        'OCTUBRE' : 10,
        'NOVIEMBRE' : 11,
        'DICIEMBRE' : 12}
    
    return month[data]

def convert_month_to_eng_string(data):
    month = {
        'ENERO' : 'January',
        'FEBRERO' : 'February',
        'MARZO' : 'March',
        'ABRIL' : 'April',
        'MAYO' :  'May',
        'JUNIO' : 'June',
        'JULIO' : 'July',
        'AGOSTO' : 'August',
        'SEPTIEMBRE' : 'September', 
        'OCTUBRE' : 'October',
        'NOVIEMBRE' : 'November',
        'DICIEMBRE' : 'December'}
    
    if data in month.keys():
        return month[data]
    
    return data

def convert_month_to_number_eng(data):
    month = {
        'January' : 1,
        'February' : 2,
        'March' : 3,
        'April' : 4,
        'May' : 5,
        'June' : 6,
        'July' : 7,
        'August' : 8,
        'September' : 9, 
        'October' : 10,
        'November' : 11,
        'December' : 12}
    return month[data]

def convert_month_to_number_reverse(data):
    month = {
        "01":'January',
        "02":'February',
        "03":'March',
        "04":'April',
        "05":'May',
        "06":'June',
        "07":'July',
        "08":'August',
        "09":'September', 
        "10":'October',
        "11":'November',
        "12":'December'}
    return month[data]

def convert_month_to_number_reverse_number(data):
    month = {
        1:'January',
        2:'February',
        3:'March',
        4:'April',
        5:'May',
        6:'June',
        7:'July',
        8:'August',
        9:'September', 
        10:'October',
        11:'November',
        12:'December'}
    return month[data]

def convert_month_to_number_esp(data):
    month = {
        "Ene": 1,
        "Feb": 2,
        "Mar": 3,
        "Abr" :4,
        "May": 5,
        "Jun": 6,
        "Jul" :7,
        "Ago" :8,
        "Sep" :9,
        "Oct" :10,
        "Nov" :11,
        "Dic" :12,

        }
    return month[data]



def adstock(list,adstock_rate):
    adstock_list = []
    for i in range(len(list)):
        if i == 0: 
            adstock_list.append(list[i])
        else:
            adstock_list.append(list[i] + adstock_rate * adstock_list[i-1])            
    return adstock_list

def adbudg(list,rho=0,v=1,p=1,beta=1,alpha=0):
    rho = rho*p
    tk=  alpha+((beta*(np.power(list,v)) )/( (np.power(list,v)) + (np.power(rho,v)) ))
    return tk


def create_date_range(min_fecha,max_fecha,name_column_fecha):
    range_fecha = pd.date_range(start=min_fecha, end=max_fecha)
    data_estacionales = pd.DataFrame({name_column_fecha:range_fecha})
    return data_estacionales

def new_name_col_convert(data,name_columns):
    name_column_new = ""
    name_column_new += data[name_columns[0]]
    len_name_colum =  len(name_columns)
    if len_name_colum > 1:
        for i in range(1,len_name_colum):
            name_column_new += ("_"+data[name_columns[i]])

    return name_column_new.str.replace(" ","", regex=True)

def add_value_new_dataframe(data,data2,name_column_new,name_columna_comp,inversion_column,name_column_mes,mes,name_column_año = "",año=None):
    if len(name_column_año) <= 0:
        get_info = data2.loc[(data2[name_column_mes] == mes) & (data2[name_column_new] == name_columna_comp),inversion_column]
    else:
        get_info = data2.loc[(data2[name_column_mes] == mes) & (data2[name_column_año] == año) & (data2[name_column_new] == name_columna_comp),inversion_column]

    if (get_info).any().any():
        return get_info.values[0]
    
    if len(get_info) > 0:
        if get_info.values[0] == 0:
            return get_info.values[0]

    return np.nan

def data_processed(data_p,name_columns_export,mes_p,año_p,inversion_p,order_by = True):
    name_columns_p = "COLUMN_NEW"

    data_p["COLUMN_NEW"] = new_name_col_convert(data_p,name_columns_export)

    name_column_new = data_p[name_columns_p]
    name_column_new = name_column_new.drop_duplicates()
    if order_by:
        name_column_new = name_column_new.sort_values()

    if año_p.isnumeric():
        files_new = len(get_values_uniques(data_p[mes_p]))
    else:
        shape_dates_new = data_p[[año_p,mes_p]].drop_duplicates().reset_index()
        files_new = int(get_dates_shape(shape_dates_new)[0])

    columns_new = int(get_dates_shape(name_column_new)[0])

    matrix = np.zeros((files_new, columns_new))
    dates_filtre2_new = pd.DataFrame(matrix)
    dates_filtre2_new = dates_filtre2_new.set_axis(name_column_new, axis=1, inplace=False)
    dates_filtre2_new.insert(0,"AÑO",0)
    dates_filtre2_new.insert(1,mes_p,0)
    if año_p.isnumeric():
        dates_filtre2_new[mes_p] =  get_values_uniques(data_p[mes_p])
        dates_filtre2_new["AÑO"] =  año_p
    else:
        dates_filtre2_new[mes_p] =  shape_dates_new[mes_p]
        dates_filtre2_new["AÑO"] =  shape_dates_new[año_p]
    if año_p.isnumeric():
        for mes_for in dates_filtre2_new[mes_p].values:
            for name_columna_for in name_column_new.values:
                dates_filtre2_new.loc[dates_filtre2_new[mes_p] == mes_for,name_columna_for] = dates_filtre2_new.loc[dates_filtre2_new[mes_p] == mes_for,name_columna_for].apply(add_value_new_dataframe, args=[data_p,name_columns_p,name_columna_for,inversion_p,mes_p,mes_for])

    else:
        for año_for in get_values_uniques(dates_filtre2_new[año_p]):
            for mes_for in dates_filtre2_new[mes_p].values:
                for name_columna_for in name_column_new.values:
                    dates_filtre2_new.loc[(dates_filtre2_new[mes_p] == mes_for) & (dates_filtre2_new["AÑO"] == año_for),name_columna_for] =  dates_filtre2_new.loc[(dates_filtre2_new[mes_p] == mes_for) & (dates_filtre2_new["AÑO"] == año_for),name_columna_for].apply(add_value_new_dataframe, args=[data_p,name_columns_p,name_columna_for,inversion_p,mes_p,mes_for,año_p,año_for])

    dates_filtre2_new.columns = dates_filtre2_new.columns.str.replace("*","_", regex=True).str.replace(" ","", regex=True)

    return dates_filtre2_new


def export_archive_data(data_final,name_archive_export,name_archive_export_only,name_sheet_set,type_only,reset_index = True):
    if type_only:
        if os.path.isfile(f"{name_archive_export_only}.xlsx"):
            with pd.ExcelWriter(f"{name_archive_export_only}.xlsx",mode='a',if_sheet_exists="replace") as writer:
                data_final.to_excel(writer,sheet_name = name_sheet_set, index= reset_index)
        else:
            data_final.to_excel(f"{name_archive_export_only}.xlsx",sheet_name=name_sheet_set, index= reset_index)
    else:
        data_final.to_excel(f"{name_archive_export}.xlsx",sheet_name=name_sheet_set, index= reset_index)















