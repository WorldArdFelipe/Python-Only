import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

"""
types = (
    0 = excel (Default)
    1 = csv
)
"""

def load_archive(name_archive,type = "excel",page_index = 0):
    if type == "csv":
        return pd.read_csv(name_archive)
    else:
        return pd.read_excel(name_archive,page_index)

#Get count dates na
def get_dates_na(date):
    return date.isna().sum()

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

def set_delete_duplicate(date):
    return date.drop_duplicates(keep='last', inplace= True)

#delete column is na values
def set_delete_column_is_na(data):
    return data.dropna()

#change value is na to value x
def set_value_is_na(data,value = 0):
    return data.fillna(value,inplace = True)


def show_info_dates_extra1(data):
    p_q =  get_dates_first_cuartil(data)
    t_q =  get_dates_three_cuartil(data)
    i_q =  get_dates_intercuartil(data)
    m =  get_dates_median(data)
    v_mn =  get_dates_min(data)
    v_mx =  get_dates_max(data)

    print("Primer Cuartil : {} \nTercer Cuartil : {} \nInter Cuartil : {}\nMediana : {}\nMinima : {}\nMaxima : {}".format(p_q,t_q,i_q,m,v_mn,v_mx))

# show box outliners of value atipicos
def show_box_outliers(data):
    plt.boxplot(data,vert=False)
    plt.show()







