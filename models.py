from app import db


class Persona(db.Model): #Hereda de db.Model
    id = db.Column(db.Integer, primary_key=True)#sql alchemy es como las clases de modelo de django
    nombre = db.Column(db.String(250))
    apellido = db.Column(db.String(250))
    email = db.Column(db.String(250))
    
    def __str__():
        return f"Id: {id}, Nombre: {nombre}, Apellido: {apellido}, Email: {email}"
