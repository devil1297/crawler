import re
def getMonth(mm):
    month = {
        'JAN': "01",
        'FEB': "02",
        'MAR': "03",
        'APR': "04",
        'MAY': "05",
        'JUN': "06",
        'JUL': "07",
        'AUG': "08",
        'SEP': "09",
        'OCT': "10",
        'NOV': "11",
        'DEC': "12",
    }
    return month.get(mm)
def string2Date(date):
    part = date.split('-')
    dd = part[1]
    mm = getMonth(part[0].upper())
    yyyy = '20' + part[2]

    return yyyy+'-'+mm+'-'+dd

def checkTM(titleCheck):
    f = open("TM.txt", "r")
    for tmWord in f:
        if titleCheck.find(tmWord.upper()) != -1:
            return 0
    return 1

def get_type_product(title):
    titleCheck = title.upper()
    status=1
    type = "??"
    if checkTM(titleCheck) != 1:
       status = -1
    elif titleCheck.find("ALL OVER") != -1:
        type ="ALL OVER"
    elif titleCheck.find("LONG SLEEVE") != -1:
        type = "LONG SLEEVE"
    elif titleCheck.find("HOODIE") != -1:
        type = "HOODIE"
    elif titleCheck.find("SWEATSHIRT") != -1:
        type = "SWEATSHIRT"
    elif titleCheck.find("SHIRT") != -1:
        type = "T-SHIRT"
    elif titleCheck.find("MUG") != -1:
        type = "MUG"
    elif titleCheck.find("POSTER") != -1:
        type = "POSTER"
    else:
        status = -1
    return [status, type]

def getSoldProductEbay(stringInput):
    m = re.search('of views. (.+?) sold', stringInput)
    if m:
        found = m.group(1)
        return int(found.replace(',', ''))
    else:
        return 0

def getDayProductEbay(stringInput):
    m = re.search('(.+?) days on eBay', stringInput)
    if m:
        found = m.group(1)
        return int(found.replace(',', ''))
    else:
        return 0

def getViewProductEbay(stringInput):
   return int(stringInput.replace(',',''))