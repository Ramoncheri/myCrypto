from the_app import app
from the_app import api
from flask import render_template, request, redirect, url_for
import sqlite3
from the_app.forms import CompraForm
from the_app.functions import calc_fecha, select



@app.route('/')
def index():

    d=select()
    if d:
        return render_template('inicio.html', ops= d)

    else: 
        return render_template('sin_movimientos.html')


@app.route('/detalle')

def detalle_ops():
    
    cryptoM= request.values['id']
    conn=sqlite3.connect(app.config['BBDD'])
    c= conn.cursor()
    
    query= "SELECT fecha, volumen, cotizacion, importe, a_cripto, de_cripto FROM resumen WHERE a_cripto=? or de_cripto=?"
    datos=((cryptoM), (cryptoM))
    op_crypto= c.execute(query,datos).fetchall()
    
    conn.close()
    

    
    return render_template('detalle.html', op_crypto= op_crypto, cryptoM=cryptoM)


@app.route('/operar', methods=["GET", "POST"])
def operar():

    form= CompraForm(request.form)  

    if request.method=='GET':
    
        return render_template('formul_compra.html', form= form)

    else:
        
        if request.values.get('calcular'):

            if form.validate():
        
                cantidadTo= api.convert(request.values.get('criptoFrom'), request.values.get('cantidadFrom'), request.values.get('criptoTo'))
                cotiz= cantidadTo/float(request.values.get('cantidadFrom'))
                fecha= calc_fecha()
                return render_template('formul_compra.html', form= form, cotiz= cotiz, cantidadTo= cantidadTo, fecha=fecha)

            else:
                return render_template('formul_compra.html', form= form)

        elif request.values.get('cancelar'):
        
            return redirect(url_for("operar"))

        else:

            conn=sqlite3.connect(app.config['BBDD'])
            c= conn.cursor()
            query= "INSERT INTO resumen(fecha, de_cripto, volumen, a_cripto, cotizacion, importe) values (?,?,?,?,?,?);"
            datos= (request.values.get('fecha'), request.values.get('criptoFrom'), request.values.get('cantidadFrom'), request.values.get('criptoTo'), request.values.get('cotiz'), request.values.get('cantidadTo'))
            c.execute(query, datos)

            conn.commit()
            conn.close()

            return redirect(url_for('index'))
        





@app.route('/status')
def status():
    conn= sqlite3.connect(app.config['BBDD'])
    c= conn.cursor()

    query= "SELECT id, de_cripto, volumen, importe, a_cripto FROM resumen;"
    operaciones= c.execute(query).fetchall()
    
    conn.close()
    
    if operaciones:
    
        d={}
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
            d[symbol_from]['importe']= cotiz
    

    suma_total_act= 0
    for fila in d.items():
        if fila[0] != 'EUR':
            suma_total_act += fila[1]['volumen']*fila[1]['importe']
    

    return render_template('status.html', ops= d, suma_total_act= suma_total_act)




