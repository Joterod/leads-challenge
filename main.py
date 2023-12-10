from fastapi import FastAPI
from config.database import Base, engine, SessionLocal
from models.models import Carrera, Materia
from routers.user import user_router
from routers.estudiante import estudiante_router


app = FastAPI()
app.title = "Leads"
app.version = "0.1"

app.include_router(user_router)
app.include_router(estudiante_router)

@app.on_event("startup")
async def on_startup():
    Base.metadata.create_all(bind=engine)
    try:
        setup_initial_data()
    except Exception as e:
        print(e)

def setup_initial_data():
    db = SessionLocal()
    try:
        carreras_info = [
            {"nombre": "Ingeniería", "materias_especificas": ["Cálculo", "Física", "Programación"]},
            {"nombre": "Medicina", "materias_especificas": ["Anatomía", "Bioquímica", "Farmacología"]},
        ]
        carreras = []
        for info in carreras_info:
            carrera = Carrera(nombre=info["nombre"])
            carreras.append(carrera)
            db.add(carrera)

            for materia_especifica in info["materias_especificas"]:
                materia = Materia(nombre=f"{info['nombre']} - {materia_especifica}")
                carrera.materias.append(materia)
                db.add(materia)
    
        db.commit()
    except Exception as e:
        print(e)
    finally:
        db.close()
