from the_app import app
from the_app import api
from flask import render_template, request, redirect, url_for
import sqlite3
from the_app.forms import CompraForm
from the_app.functions import calc_fecha, select



@app.route('/')
def index():
    
    d=select()
    if len(d)==1:
        return render_template('sin_movimientos.html')
    else: 
        return render_template('inicio.html', ops= d)     
   

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
    #boton_calc_presionado= False
    form= CompraForm(request.form)  

    if request.method=='GET':
    
        return render_template('formul_compra.html', form= form)

    else:
        
        if request.values.get('calcular'):
            
            if form.validate():
        
                cantidadTo= api.convert(request.values.get('criptoFrom'), request.values.get('cantidadFrom'), request.values.get('criptoTo'))
                cotiz= cantidadTo/float(request.values.get('cantidadFrom'))
                fecha= calc_fecha()
                #boton_calc_presionado= True
                return render_template('formul_compra.html', form= form, cotiz= cotiz, cantidadTo= cantidadTo, fecha=fecha)
                
            else:
                return render_template('formul_compra.html', form= form)

            

        elif request.values.get('cancelar'):
        
            return redirect(url_for("operar"))

        else:
            #if boton_calc_presionado== True:
            conn=sqlite3.connect(app.config['BBDD'])
            c= conn.cursor()
            query= "INSERT INTO resumen(fecha, de_cripto, volumen, a_cripto, cotizacion, importe) values (?,?,?,?,?,?);"
            datos= (request.values.get('fecha'), request.values.get('criptoFrom'), request.values.get('cantidadFrom'), request.values.get('criptoTo'), request.values.get('cotiz'), request.values.get('cantidadTo'))
            
            try:
                c.execute(query, datos)
                conn.commit()
            except Exception as e:
                print('MOD/DEL- Error de acceso a la base de datos: {}'.format(e))
                return 'Error de acceso a la base de datos'
            conn.close()
            #boton_calc_presionado= False
            return redirect(url_for('index'))
            #else:
                #return redirect(url_for("operar"))
        
            

@app.route('/status')
def status():
    d= select()

    suma_total_act= 0
    for fila in d.items():
        if fila[0] != 'EUR':
            suma_total_act += fila[1]['volumen']*fila[1]['importe']
    

    return render_template('status.html', ops= d, suma_total_act= suma_total_act)




