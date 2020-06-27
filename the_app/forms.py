from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, SelectField, DateTimeField
from wtforms.validators import DataRequired, EqualTo

class CompraForm(FlaskForm):
    criptoFrom= SelectField(u'From ', choices= [(''), ('EUR'), ('BTC'), ('ETH'), ('LTC')], validators=[EqualTo('criptoTo', message="No puede ser igual a la moneda comprada")])
    criptoTo= SelectField(u'To ', choices=[(''), ('EUR'), ('BTC'), ('ETH'), ('LTC')])
    cantidadFrom= FloatField('Cantidad', validators=[DataRequired(message='Campo requerido')])
    submitField= SubmitField('Calcular')
    #cantidadTo= FloatField('Cantidad')
    #fechaHora= DateTimeField('fecha')
    #cotizacion= FloatField('Cotización')

    
    