from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Usuario(db.Model):
    __tablename__ = "Usuarios"
    ID_Usuario = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(100))
    Correo = db.Column(db.String(100))


class Propuesta(db.Model):
    __tablename__ = "Propuestas"
    ID_Propuesta = db.Column(db.Integer, primary_key=True)
    ID_Usuario = db.Column(db.Integer, db.ForeignKey("Usuarios.ID_Usuario"))
    Nombre_proyecto = db.Column(db.String(200), unique=True)
    Descripcion_problema = db.Column(db.Text)
    Solucion_propuesta = db.Column(db.Text)
    Area_impacto = db.Column(db.Integer)
    Descripcion_general = db.Column(db.Text)
    Fecha_envio = db.Column(db.String)

    usuario = db.relationship("Usuario")


class Pregunta(db.Model):
    __tablename__ = "Preguntas"
    ID_Pregunta = db.Column(db.Integer, primary_key=True)
    Texto_pregunta = db.Column(db.Text, nullable=False)
    Puntaje_maximo = db.Column(db.Integer, nullable=False)


class Evaluacion(db.Model):
    __tablename__ = "Evaluaciones"
    ID_Evaluacion = db.Column(db.Integer, primary_key=True)
    ID_Propuesta = db.Column(db.Integer, db.ForeignKey("Propuestas.ID_Propuesta"))
    Puntaje_total = db.Column(db.Integer)
    Fecha_evaluacion = db.Column(db.String)

    propuesta = db.relationship("Propuesta", backref="evaluacion")


class EvaluacionRespuesta(db.Model):
    __tablename__ = "Evaluacion_Respuestas"
    ID_Evaluacion = db.Column(db.Integer, db.ForeignKey("Evaluaciones.ID_Evaluacion"), primary_key=True)
    ID_Pregunta = db.Column(db.Integer, db.ForeignKey("Preguntas.ID_Pregunta"), primary_key=True)
    Puntaje_obtenido = db.Column(db.Integer)

    evaluacion = db.relationship("Evaluacion", backref="respuestas")
    pregunta = db.relationship("Pregunta")
