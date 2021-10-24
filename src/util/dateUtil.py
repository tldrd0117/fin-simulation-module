import datetime

def currentDate():
    today = datetime.datetime.today()
    return today.strftime("%Y%m%d")
