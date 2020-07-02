from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, SelectField, DateTimeField
from wtforms.validators import DataRequired, ValidationError
from the_app.functions import select


def compra_errors(form, field):
    if field.data ==form.criptoFrom.data:
        raise ValidationError("No es posible operar entre el mismo tipo de moneda")
    elif field.data != "BTC" and form.criptoFrom.data == "EUR": 
        raise ValidationError("Solo son posibles las operaciones de cambio de EUR con BTC")
    elif field.data == "EUR" and form.criptoFrom.data != "BTC":
        raise ValidationError("Solo son posibles las operaciones de cambio de EUR con BTC")

def valid_cantidadFrom(form, field):
    ops= select()
    for operacion, data in ops.items():
        if operacion != 'EUR' and form.criptoFrom.data == operacion:
            if field.data > data['volumen']:
                raise ValidationError('Saldo insuficiente')


def criptosFrom():
    d= select()
    criptosFrom= d.keys()
    return criptosFrom



criptosFrom= criptosFrom()
criptosTo = ("","EUR", "BTC", "ETH", "XRP", "LTC", "BCH", "BNB", "USDT", "EOS", "BSV", "XLM", "ADA", "TRX")

class CompraForm(FlaskForm):
    criptoFrom= SelectField('From', choices= [(cripto, cripto) for cripto in criptosFrom])
    criptoTo= SelectField('To', choices=[(cripto, cripto) for cripto in criptosTo], validators=[compra_errors])
    cantidadFrom= FloatField('Cantidad', validators=[DataRequired( message='Campo requerido'), valid_cantidadFrom])
    calcular= SubmitField('Calcular')

    cancelar= SubmitField('Cancelar')
    comprar= SubmitField('Comprar')


    #cantidadTo= FloatField('Cantidad')
    #fechaHora= DateTimeField('fecha')
    #cotizacion= FloatField('Cotización')

    
      


    