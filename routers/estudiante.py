from fastapi import Query, Depends, HTTPException, Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import  Session, selectinload
from config.database import SessionLocal
from models.models import Estudiante, Carrera, Materia
from schemas.estudiante_schema import EstudianteBase, EstudianteCreate
from middleware.jwt_bearer import JWTBearer
from typing import List

estudiante_router = APIRouter()

templates = Jinja2Templates(directory="templates") 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get a template con formulario de estudiante
@estudiante_router.get("/estudiantes/", tags=['estudiantes'], response_class=HTMLResponse, dependencies=[Depends(JWTBearer())])
async def obtener_formulario(request: Request,  db: Session = Depends(get_db)):
    materias = obtener_materias(db)
    return templates.TemplateResponse("estudiante_form.html", {"request": request, "carreras": carreras, "materias": materias})

def obtener_carreras(db: SessionLocal) -> List[str]:
    carreras = db.query(Carrera).all()
    return [carrera.nombre for carrera in carreras]

def obtener_materias(db: SessionLocal) -> List[str]:
    materias = db.query(Materia).all()
    return [materia.nombre for materia in materias]

# Endpoint de creación de estudiante
@estudiante_router.post("/estudiantes/", tags=['estudiantes'], status_code=201, dependencies=[Depends(JWTBearer())])
async def crear_estudiante(estudiante_data: EstudianteCreate, db: Session = Depends(get_db)):
    # Verificamos si el correo ya existe en la base de datos
    estudiante_existente = db.query(Estudiante).filter_by(correo=estudiante_data.correo).first()
    if estudiante_existente:
        raise HTTPException(status_code=400, detail="La cuenta de correo ya fue utilizada")

    # Buscamos las carreras y materias por su nombre
    carreras = db.query(Carrera).filter(Carrera.nombre.in_(estudiante_data.carreras)).all()
    materias = db.query(Materia).filter(Materia.nombre.in_(estudiante_data.materias)).all()

    # Verificamos si todas las carreras y materias están en la base de datos
    if len(carreras) != len(estudiante_data.carreras) or len(materias) != len(estudiante_data.materias):
        raise HTTPException(status_code=400, detail="No se encontraron todas las carreras o materias en la base de datos")

    # Creamos el estudiante con las carreras y materias encontradas
    nuevo_estudiante = Estudiante(
        nombre_completo=estudiante_data.nombre_completo,
        correo=estudiante_data.correo,
        direccion=estudiante_data.direccion,
        telefono=estudiante_data.telefono,
        edad=estudiante_data.edad,
        carreras=carreras,
        materias=materias
    )
    db.add(nuevo_estudiante)
    db.commit()
    db.refresh(nuevo_estudiante)

    return {"mensaje": "¡Estudiante creado con éxito!", "id": nuevo_estudiante.id}

# Get a resultados, páginados y ordenados por ID de estudiante
@estudiante_router.get("/resultados/", tags=["resultados"], response_model=List[EstudianteBase], dependencies=[Depends(JWTBearer())])
async def obtener_resultados(page: int = Query(1), db: Session = Depends(get_db)):
    page_size = 10
    start = (page - 1) * page_size
    
    # Realizamos la consulta para obtener estudiantes con sus carreras y materias asociadas
    resultados = (
        db.query(Estudiante)
        .options(selectinload(Estudiante.carreras).selectinload(Carrera.materias))
        .order_by(Estudiante.id)
        .offset(start)
        .limit(page_size)
        .all()
    )
    
    return resultados

# Get por ID a estudiante
@estudiante_router.get("/resultados/{registro_id}", tags=["estudiantes"], response_model=EstudianteBase, dependencies=[Depends(JWTBearer())])
async def obtener_registro_por_id(registro_id: int, db: Session = Depends(get_db)):
    # Busca en la BBDD el primer estudiante que coincida ID con el valor de registro_id
    registro = db.query(Estudiante).filter(Estudiante.id == registro_id).first()
    if registro:
        return registro
    else:
        raise HTTPException(status_code=404, detail="Registro no encontrado")