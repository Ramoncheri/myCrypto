from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, SelectField, DateTimeField
from wtforms.validators import DataRequired, EqualTo, ValidationError


def valida_posibilidad_compra(form, field):
    if field.data ==form.Moneda_from.data:
        raise ValidationError("No es posible realizar ningún intercambio entre monedas iguales")
    elif field.data != "BTC" and form.Moneda_from.data == "EUR": 
        raise ValidationError("No es posible intercambiar EUR, por {} directamente. Sólo puede adquirir {}, con otras criptomonedas.".format(field.data,field.data ))
    elif field.data == "EUR" and form.Moneda_from.data != "BTC":
        raise ValidationError("No es posible cambiar {} por EUR, directamente. Sólo es posible intercambiar BTC por EUR. Si desea EUR, por favor, intercambie  antes sus {} a BTC y vuelva a intentarlo.".format(form.Moneda_from.data, form.Moneda_from.data))



criptos = ("","EUR", "BTC", "ETH", "XRP", "LTC", "BCH", "BNB", "USDT", "EOS", "BSV", "XLM", "ADA", "TRX")

class CompraForm(FlaskForm):
    criptoFrom= SelectField(u'From ', choices= [(cripto) for cripto in criptos], validators=[EqualTo('criptoTo', message="No puede ser igual a la moneda comprada")])
    criptoTo= SelectField(u'To ', choices=[(cripto) for cripto in criptos], validators=[valida_posibilidad_compra])
    cantidadFrom= FloatField('Cantidad', validators=[DataRequired(message='Campo requerido')])
    calcular= SubmitField('Calcular')

    cancelar= SubmitField('Cancelar')
    comprar= SubmitField('Comprar')


    #cantidadTo= FloatField('Cantidad')
    #fechaHora= DateTimeField('fecha')
    #cotizacion= FloatField('Cotización')

    
      


    