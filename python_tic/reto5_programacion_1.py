def grupos(list_get):
    list_save = []

    for i in list_get:
        if i not in list_save:
            list_save.append(i)
    
    return list_save

def necesito_del_grupo(list_index,list_get,value):
    list_save = []

    for a in list_index:
        value_get = list_get[a]
        if value_get == value:
            list_save.append(a)
    
    return list_save

def sirven_a_marta(list_maria,list_marta):
    list_save = []
    for i in  list_maria:
        if i not in list_marta:
            list_save.append(i)

    return list_save

def cuantas_cambian(list_marta, list_maria):
    count_marta = 0
    count_maria = 0

    for i in list_marta:
        if i not in list_maria:
            count_marta += 1
    
    for i in list_maria:
        if i not in list_marta:
            count_maria += 1

    return (count_maria if count_marta > count_maria else count_marta)
