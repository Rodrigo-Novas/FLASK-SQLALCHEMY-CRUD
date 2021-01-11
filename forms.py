
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#flask form se importa desde wtf, le colocamos los campos que va a tener nuestro form
class PersonaForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired()]) #esto es para hacer formularios
    apellido = StringField("Apellido") #esto es para hacer formularios
    email = StringField("Email", validators=[DataRequired()]) #esto es para hacer formularios
    enviar = SubmitField("Enviar")