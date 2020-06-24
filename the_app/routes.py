from the_app import app
from the_app import api
from flask import render_template, request
import sqlite3



@app.route('/')
def index():
    #price= api.convert()

    conn= sqlite3.connect(app.config['BBDD'])
    c= conn.cursor()

    query= "SELECT id, de_cripto, volumen,importe, operacion FROM resumen;"
    operaciones= c.execute(query).fetchall()
    
    conn.close()

    if operaciones:
    
        d={}
        k=d.keys()
        for fila in operaciones:
            if (fila[1]) in k:
                if fila[4]=='Compra':
                    d[fila[1]]['volumen'] += (fila[2])
                    
                else:
                    d[fila[1]]['volumen'] -= (fila[2])
                    
            else:
                d[fila[1]]= {'volumen': (fila[2])} 
            
        
        
        for symbol in k:
            symbol_from=symbol
            price= api.convert(symbol_from)
            d[symbol_from]['importe']= price
        
        return render_template('inicio.html', ops= d)

    else: 
        return render_template('sin_movimientos.html')


@app.route('/detalle', methods=["GET"])

def detalle_ops():
    if request.method== 'GET':
        cryptoM= request.values['id']
        conn=sqlite3.connect(app.config['BBDD'])
        c= conn.cursor()
        
        query= "SELECT fecha, hora, operacion, volumen, cotizacion, importe, de_cripto FROM resumen WHERE de_cripto=?"
        op_crypto= c.execute(query, (cryptoM,)).fetchall()
        
        conn.close()
    

    
    return render_template('detalle.html', titulo= 'My Crypto', op_crypto= op_crypto, cryptoM=cryptoM)


@app.route('/operar', methods=["GET", "POST"])
def operar():

    #form= CompraForm(request.form)  

    if request.method=='GET':
        return render_template('formul_compra.html', form=form)
    else:
        return 'es un post confirmando la compra'


@app.route('/status')
def status():
    conn= sqlite3.connect(app.config['BBDD'])
    c= conn.cursor()

    query= "SELECT id, de_cripto, volumen, importe, operacion, cotizacion FROM resumen;"
    operaciones= c.execute(query).fetchall()
    
    conn.close()
    
    if operaciones:
    
        d={}
        k=d.keys()
        for fila in operaciones:
            if (fila[1]) in k:
                if fila[4]=='Compra':
                    d[fila[1]]['volumen'] += (fila[2])
                    d[fila[1]]['importe'] += (fila[3])
                else:
                    d[fila[1]]['volumen'] -= (fila[2])
                    d[fila[1]]['importe'] -= (fila[3])
            else:
                d[fila[1]]= {'volumen': (fila[2]), 'importe':(fila[3]), 'cotizacion': (fila[5])}

        for symbol in k:
            symbol_from=symbol
            price= api.convert(symbol_from)
            d[symbol_from]['cot_actual']= price
    
    suma_total= 0
    suma_total_act= 0
    for fila in d.items():
        suma_total += fila[1]['importe']
        suma_total_act += fila[1]['volumen']*fila[1]['cot_actual']
    

    return render_template('status.html', ops= d, suma_total= suma_total, suma_total_act= suma_total_act)




