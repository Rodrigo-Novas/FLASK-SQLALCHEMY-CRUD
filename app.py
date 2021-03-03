from flask import Flask, url_for, session, request, render_template
from flask_migrate import Migrate
from werkzeug.utils import redirect
from werkzeug.exceptions import abort

from forms import PersonaForm
from database import db
from models import Persona

import psycopg2 as psy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#Configuracion de la bd
USER_DB = "postgres"
PASS_DB = "jose jose" #modificar en deploy
URL_DB = "localhost"
NAME_DB = "sap_flask"
FULL_URL_DB = f"postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}" #CONECTION STRING

app.config["SQLALCHEMY_DATABASE_URI"] = FULL_URL_DB
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#Inicializacion del objeto db de sqlalchemy
db.init_app(app)


migrate = Migrate()
migrate.init_app(app, db) #para iniciarla ejecuto flask db init, nos crea la carpeta de migrations 
#tambien usamos el comando flask db migrate para migrar a la base de datos la clase que creamos  
#Posteriormente usamos flask db update, seria como un mCon.commit lo que hace es guardar los datos en la db    
#si hacemos algun cambio                      
#Usamos flask stamp head esto es para saber si tenemos algun problema es necesario ejecutarlo siempre al principio, nos actualiza
#despues usamos flask db upgrade

#configuracion de flask-wtf
app.config["SECRET_KEY"] = "asdasdasd" #se configura una secret key





#despues de crear la tabla persona vamos a crear las rutas
#si colocamos estas app.route seguidas le decimos que se puede usar cualquier ruta de estas
@app.route("/")
@app.route("/index")
@app.route("/index.html")
def inicio():
    #listado de personas
    personas = Persona.query.order_by("id") #esto nos devuelve todas las persnas que hayan y ademas nos ordena por id, se puede usar query.all() pero no orde
    total_personas = Persona.query.count() #nos envia el numero total de personas
    app.logger.debug(f"Listado de personas: {personas}")
    app.logger.debug(f"Total de personas: {total_personas}")
    return render_template("index.html", personas = personas, total_personas = total_personas)


@app.route("/ver/<int:id>")
def verId(id):
        persona= Persona.query.get_or_404(id)#en el caso de que no lo encuentre lanza el error 404
        #app.logger.debug(f"Ver persona: {persona}")
        return render_template("detalle.html", persona= persona)
    
@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    persona = Persona()
    personaForm = PersonaForm(obj=persona)#le indico que el formulario va a utilizar la clase persona
   #Agarrar los datos del form y enviarlos a la bdd
    if request.method == "POST":
        if personaForm.validate_on_submit(): #lo que hace es validar que el formulario sea valido
            personaForm.populate_obj(persona) #completa el objeto de tipo modelo
            #insertamos nuevo registro
            db.session.add(persona)
            db.session.commit()
            return redirect(url_for("inicio"))
    return render_template("agregar.html", forma = personaForm) 


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    persona = Persona.query.get_or_404(id)
    personaForm = PersonaForm(obj= persona)
    if request.method == "POST":
        if personaForm.validate_on_submit():
            personaForm.populate_obj(persona)
            db.session.commit()
            return redirect(url_for("inicio"))
    return render_template("editar.html", forma = personaForm)


@app.route("/eliminar/<int:id>", methods=["GET"])
def eliminar(id):
    persona = Persona.query.get_or_404(id)
    db.session.delete(persona)
    db.session.commit()
    return redirect(url_for("inicio"))
