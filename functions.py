def maxf(min,max):
    return (min if min > max else max)

def max_tree(arg1,arg2,arg3):
    return (arg1 if arg1 > arg2 else arg2 if arg2 > arg3 else arg3 )

def is_vocal(character):
    lista = ["a","e","i","o","u"]
    return character.lower() in lista

def sum(list_numbers):
    count = 0
    for i in list_numbers:
        count += i
    return count

def mult(list_numbers):
    count = 1
    for i in list_numbers:
        count *= i
    return count

def inversa(text):
    letras = str()
    for i in range(len(text)):
        letras += text[(len(text)-1)-i]
    return letras

def is_palondromo(text):
    return inversa(text) == text

def superposicion(lista1,lista2):
    for i in lista1:
        if i in lista2:
            return True
    return False

def generar_n_caracteres(number,texto):
    return texto*number

def procedimiento(lista):
    string = str()
    for i in lista:
        string += ("*"*i + "\n")
    return string


def repeat_letras(texto):
    texto = texto.lower().replace(",","").replace("." ,"").split()
    lista = {}
    for i in texto:
        if i not in lista:
            lista[i] = texto.count(i)
    return lista


def Multiplicar(number1,number2):
    iniciar = min(number1,number2)
    result = 0

    for i in range(iniciar):
        result += max(number1,number2)

    return result

def GetExampleNumber(text):
    count = 0
    list_numbers = []

    for i in text:
        if i.isdigit():
            #if i not in list_numbers:
            list_numbers.append(i)
            count += int(i)

    print("Digitos Extraidos: ",*list_numbers)

    list_numbers.sort()

    print("Digitos ordenados: ",*list_numbers)

    print("Suma de Digitos:", count)


def PruebaExtra(number):
    lista = []
    count = 0
    for i in range(1,number):
        if i%3 == 0 or i%5 == 0:
            lista.append(i)
            count += i
    print(count)


def PruebaExtra2(*arg):
    texto = str()
    for i in arg:
        texto += str(i)

    no_numbers = str()
    for i in range(0,10):
        i = str(i)
        if i not in texto:
            no_numbers += i
  
    print(no_numbers)

def OrdenarMaMe(texto):
    texto = texto.split(" ")
    lista = []

    for i in texto:
       lista.append(int(i))

    print(f'{max(lista)} {min(lista)}')

def make_negative( number):
    return number if number < 0 else (number-(number*2))

def getVolumeOfCubiod(length, width, height):
    result = (length * width * height) 
    return result

def string_to_number(s):
    print(int(s))


def define_suit(card):
    DECK = ['2S','3S','4S','5S','6S','7S','8S','9S','10S','JS','QS','KS','AS',
            '2D','3D','4D','5D','6D','7D','8D','9D','10D','JD','QD','KD','AD',
            '2H','3H','4H','5H','6H','7H','8H','9H','10H','JH','QH','KH','AH',
            '2C','3C','4C','5C','6C','7C','8C','9C','10C','JC','QC','KC','AC']

    SUITE = {
        "C": "clubs",
        "D": "diamonds",
        "H": "hearts",
        "S": "spades"
        }

    print(SUITE[card[-1]])


def fibo(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1

    return fibo(n-1) + fibo(n-2)


def race(v1, v2, g):
    if v1 >= v2:
        return None
    time = (v2-v1)
    time = g*3600/time

    hours = int(time/3600)
    minutes = int((time%3600) / 60)
    seconds = int(time % 60)

    return [hours,minutes,seconds]
    

def cuadrado(number):
    text = str()
    pared = number-2

    for i in range(number):
        text += "*"  

    text+="\n"

    for i in range(pared):
        text+=("*")
        text+=(" ")*(number-2)
        text+=("*")
        text+="\n"

    for i in range(number):
        text += "*"
    text+="\n"

    return text

def cuadradosimp(number):
    text = str()
    pared = number-2

    for i in range(pared):
        text+="*"

        for a in range(pared):
            text+=" "

        text+="*"
        
        text +="\n"
    return text

def fake_bin(x):
    cadena = str()
    for i in x:
        if int(i) < 5:
            cadena += "0"
        else:
            cadena += "1"
    return cadena


def numbernegative(str):
    try:
        value = int(str)
        if value < 0:
            return False
            
        if len(str) >= 4 and len(str) <= 6:
            return True
        else:
            return False
    except Exception as exception:
        return False

def main():
   print(numbernegative("#")) 
           
main()