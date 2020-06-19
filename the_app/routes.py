from the_app import app
from flask import render_template, request
import sqlite3


@app.route('/')
def index():
    conn= sqlite3.connect(app.config['BBDD'])
    c= conn.cursor()

    query= "SELECT id, criptomoneda, volumen, importe, operacion FROM resumen;"
    operaciones= c.execute(query).fetchall()
    
    conn.close()
    
    d={}
    k=d.keys()
    for fila in operaciones:
        if (fila[1]) in k:
            if fila[4]=='Compra':
                d[fila[1]]['volumen'] += float(fila[2])
                d[fila[1]]['importe'] += float(fila[3])
            else:
                d[fila[1]]['volumen'] -= float(fila[2])
                d[fila[1]]['importe'] -= float(fila[3])
        else:
            d[fila[1]]= {'volumen': float(fila[2]), 'importe': float(fila[3])}
            
    
    return render_template('inicio.html', ops= d)


@app.route('/detalle', methods=["GET", "POST"])

def detalle_ops():
    if request.method== 'GET':
        cryptoM= request.values['id']
        conn=sqlite3.connect(app.config['BBDD'])
        c= conn.cursor()
        
        query= "SELECT fecha, hora, operacion, volumen, cotizacion, importe, criptomoneda FROM resumen WHERE criptomoneda=?"
        op_crypto= c.execute(query, (cryptoM,)).fetchall()
        
        conn.close()
    

    
    return render_template('detalle.html', titulo= 'My Crypto', op_crypto= op_crypto)




