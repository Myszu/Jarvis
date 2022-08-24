from datetime import datetime

def time_alive(creation):
    delta = (datetime.now() - creation)

    case1 = [1,2,3,4]
    case2 = [5,6,7,8,9,0]

    years = int((delta.days)/365)
    months = int((delta.days)/30)-(years*12)
    days = int(delta.days)-(years*12*30)-months*30


    if int(str(years)[-1]) in case1:
        sYears = f'{years} lata '
    if int(str(years)[-1]) in case2:
        sYears = f'{years} lat '
    if years == 1:
        sYears = f'{years} rok '
    if years == 0:
        sYears = ''
        
    if int(str(months)[-1]) in case1:
        sMonths = f'{months} miesiace '
    if int(str(months)[-1]) in case2:
        sMonths = f'{months} miesiecy '
    if months == 1:
        sMonths = f'{months} miesiac '
    if months == 0:
        sMonths = ''
        
    if int(str(days)[-1]) in case1:
        sDays = f'{days} dni '
    if int(str(days)[-1]) in case2:
        sDays = f'{days} dni '
    if days == 1:
        sDays = f'{days} dzien '
    if days == 0:
        sDays = ''

    difference = f'{sYears}{sMonths}{sDays}'
    return difference


def do_sum(equ):
    values = equ.split('+')
    
    try:
        if equ.find('.')>=0:
            values = list(map(float, values))
        else:
            values = list(map(int, values))
        equation = f'To bedzie {sum(values)} 🧐'
    except ValueError:  
        equation = 'Obie wartosci musza byc liczbami. 😖'
        
    return equation


def do_sub(equ):
    values = equ.split('-')
    
    try:
        if equ.find('.')>=0:
            values = list(map(float, values))
        else:
            values = list(map(int, values))
        equation = f'To bedzie {(values[0]-values[1])} 🧐'
    except ValueError:  
        equation = 'Obie wartosci musza byc liczbami. 😖'
        
    return equation


def do_multi(equ):
    values = equ.split('*')
    
    try:
        if equ.find('.')>=0:
            values = list(map(float, values))
        else:
            values = list(map(int, values))
        equation = f'To bedzie {(values[0]*values[1])} 🧐'
    except ValueError:  
        equation = 'Obie wartosci musza byc liczbami. 😖'
        
    return equation


def do_div(equ):
    values = equ.split('/')
    
    try:
        if equ.find('.')>=0:
            values = list(map(float, values))
        else:
            values = list(map(int, values))
        equation = f'To bedzie {(values[0]/values[1])} 🧐'
    except ValueError:  
        equation = 'Obie wartosci musza byc liczbami. 😖'
        
    return equation


def do_mod(equ):
    values = equ.split('%')
    
    try:
        if equ.find('.')>=0:
            values = list(map(float, values))
        else:
            values = list(map(int, values))
        equation = f'To bedzie {(values[0]%values[1])} 🧐'
    except ValueError:  
        equation = 'Obie wartosci musza byc liczbami. 😖'
        
    return equation