from datetime import date, datetime

def calc_fecha():
    now=datetime.now()
    fecha= now.strftime("%Y-%m-%d %H:%M")
    
    return fecha
    