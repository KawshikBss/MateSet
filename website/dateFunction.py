from datetime import datetime

def get_day(date):
    return int(date[:2])

def get_month(date):
    return int(date[3:5])

def get_year(date):
    return int(date[6:10])

def get_hour(date):
    return int(date[11:13])

def get_minute(date):
    return int(date[14:16])

def int_date(date):
    return [get_year(date), get_month(date), get_day(date), get_hour(date), get_minute(date)]

def is_recent(date):
    todaysDateList = int_date(datetime.today().strftime("%d/%m/%Y-%I:%M%p"))
    compDateList = int_date(date)
    todaysDate = datetime(todaysDateList[0], todaysDateList[1], todaysDateList[2], todaysDateList[3], todaysDateList[4])
    compDate = datetime(compDateList[0], compDateList[1], compDateList[2], compDateList[3], compDateList[4])
    dateDiff = str(todaysDate - compDate).split(' ')
    if not dateDiff[0][0] == '-':
        if ':' not in dateDiff[0]:
            if int(dateDiff[0]) > 1:
                return False
        else:
            timeDiff = dateDiff[-1]
            if int(timeDiff.split(':')[0]) > 5:
                return False
            else:
                return True
    return False