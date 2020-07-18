from datetime import date, datetime
from the_app import api
import sqlite3
from the_app import app
from flask import render_template

def calc_fecha():
    now=datetime.now()
    fecha= now.strftime("%Y-%m-%d %H:%M")
    
    return fecha


def select():
    try:
        conn= sqlite3.connect(app.config['BBDD'])
        c= conn.cursor()

        query= "SELECT id, de_cripto, volumen,importe, a_cripto FROM resumen;"


        operaciones= c.execute(query).fetchall()
        
        conn.close()
        
        d={}
        if operaciones== []:
            d= {'EUR': 0}
            return d

            
        else:
            
            k=d.keys()
            for fila in operaciones:
                if fila[4] not in k:
                    d[fila[4]]= {'volumen': (fila[3])}
                    if fila[1] not in k:
                        d[fila[1]]={'volumen': -(fila[2])}
                    else: 
                        d[fila[1]]['volumen'] -= fila[2]
                    
                else:
                    d[fila[4]]['volumen'] += (fila[3])
                    if fila[1] not in k:
                        d[fila[1]]={'volumen': -(fila[2])}
                    else: 
                        d[fila[1]]['volumen'] -= fila[2]
                        
            for symbol in k:
                symbol_from=symbol
                cotiz= api.convert(symbol_from)
                try:
                    float(cotiz)== cotiz
                    d[symbol_from]['importe']= cotiz

                except:
                    d= cotiz

            return d
    
    except Exception as e:
        print ('Error de acceso a la base de datos: {}'.format(e))
        return 'BBDD'

        
    