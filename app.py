from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, Usuario, Propuesta, Pregunta, Evaluacion, EvaluacionRespuesta
from datetime import datetime


app = Flask(__name__)
CORS(app)


# Configuración DB para Render
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# Crear tablas la primera vez
@app.before_first_request
def create_tables():
    db.create_all()


# ====================================
#               USUARIOS
# ====================================
@app.post("/usuarios")
def crear_usuario():
    data = request.json
    usuario = Usuario(
        Nombre=data["Nombre"],
        Correo=data["Correo"]
    )
    db.session.add(usuario)
    db.session.commit()
    return jsonify({"msg": "Usuario creado", "ID_Usuario": usuario.ID_Usuario})


@app.get("/usuarios")
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{
        "ID_Usuario": u.ID_Usuario,
        "Nombre": u.Nombre,
        "Correo": u.Correo
    } for u in usuarios])


# ====================================
#               PROPUESTAS
# ====================================
@app.post("/propuestas")
def crear_propuesta():
    data = request.json
    propuesta = Propuesta(
        ID_Usuario=data["ID_Usuario"],
        Nombre_proyecto=data["Nombre_proyecto"],
        Descripcion_problema=data["Descripcion_problema"],
        Solucion_propuesta=data["Solucion_propuesta"],
        Area_impacto=data["Area_impacto"],
        Descripcion_general=data["Descripcion_general"],
        Fecha_envio=datetime.now().strftime("%Y-%m-%d")
    )
    db.session.add(propuesta)
    db.session.commit()
    return jsonify({"msg": "Propuesta creada", "ID_Propuesta": propuesta.ID_Propuesta})


@app.get("/propuestas")
def listar_propuestas():
    propuestas = Propuesta.query.all()
    return jsonify([{
        "ID_Propuesta": p.ID_Propuesta,
        "Nombre_proyecto": p.Nombre_proyecto,
        "ID_Usuario": p.ID_Usuario,
        "Fecha_envio": p.Fecha_envio
    } for p in propuestas])


# ====================================
#               PREGUNTAS
# ====================================
@app.post("/preguntas")
def crear_pregunta():
    data = request.json
    pregunta = Pregunta(
        Texto_pregunta=data["Texto_pregunta"],
        Puntaje_maximo=data["Puntaje_maximo"]
    )
    db.session.add(pregunta)
    db.session.commit()
    return jsonify({"msg": "Pregunta creada", "ID_Pregunta": pregunta.ID_Pregunta})


@app.get("/preguntas")
def listar_preguntas():
    preguntas = Pregunta.query.all()
    return jsonify([{
        "ID_Pregunta": p.ID_Pregunta,
        "Texto_pregunta": p.Texto_pregunta,
        "Puntaje_maximo": p.Puntaje_maximo
    } for p in preguntas])


# ====================================
#               EVALUACIONES
# ====================================
@app.post("/evaluaciones")
def crear_evaluacion():
    data = request.json

    evaluacion = Evaluacion(
        ID_Propuesta=data["ID_Propuesta"],
        Puntaje_total=data["Puntaje_total"],
        Fecha_evaluacion=datetime.now().strftime("%Y-%m-%d")
    )
    db.session.add(evaluacion)
    db.session.commit()

    for r in data["Respuestas"]:
        respuesta = EvaluacionRespuesta(
            ID_Evaluacion=evaluacion.ID_Evaluacion,
            ID_Pregunta=r["ID_Pregunta"],
            Puntaje_obtenido=r["Puntaje_obtenido"]
        )
        db.session.add(respuesta)

    db.session.commit()

    return jsonify({"msg": "Evaluación creada", "ID_Evaluacion": evaluacion.ID_Evaluacion})


@app.get("/evaluaciones/<int:id_propuesta>")
def obtener_evaluacion(id_propuesta):
    evaluacion = Evaluacion.query.filter_by(ID_Propuesta=id_propuesta).first()

    if not evaluacion:
        return jsonify({"msg": "No hay evaluación"}), 404

    respuestas = [{
        "ID_Pregunta": r.ID_Pregunta,
        "Texto_pregunta": r.pregunta.Texto_pregunta,
        "Puntaje_obtenido": r.Puntaje_obtenido
    } for r in evaluacion.respuestas]

    return jsonify({
        "ID_Evaluacion": evaluacion.ID_Evaluacion,
        "Puntaje_total": evaluacion.Puntaje_total,
        "Fecha_evaluacion": evaluacion.Fecha_evaluacion,
        "Respuestas": respuestas
    })


if __name__ == "__main__":
    app.run(debug=True)
