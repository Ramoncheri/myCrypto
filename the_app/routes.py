from the_app import app
from flask import render_template
import sqlite3





@app.route('/')
def index():
    conn= sqlite3.connect(app.config['BBDD'])
    c= conn.cursor()

    query= "SELECT Moneda_comprada, Cant_adquirida, Cantidad FROM resumen;"
    operaciones= c.execute(query).fetchall()

    conn.close()
    

    return render_template('inicio.html', titulo= 'My Crypto', operaciones= operaciones)