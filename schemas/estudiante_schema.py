from pydantic import BaseModel, constr, EmailStr, validator
from typing import List
import re

class MateriaBase(BaseModel):
    nombre: constr(min_length=3, max_length=50)
    carrera_id: int
    estudiante_id: int

    def __repr__(self):
        return f"Materia(nombre={self.nombre})"


class CarreraBase(BaseModel):
    nombre: constr(min_length=3, max_length=50)

    def __repr__(self):
        return f"Carrera(nombre={self.nombre})"

class EstudianteBase(BaseModel):
    nombre_completo: constr(min_length=3, max_length=100)
    correo: EmailStr
    direccion: constr(min_length=5, max_length=100)
    telefono: constr(min_length=7, max_length=20) 
    edad: int
    carreras: List[CarreraBase] = []
    materias: List[MateriaBase] = []

    @validator('edad')
    def validate_edad(cls, v):
        if v < 18:
            raise ValueError('La edad debe ser mayor o igual a 18')
        return v
    
    @validator('telefono')
    def validate_telefono(cls, v):
        if not re.match(r'^\+?[0-9\s]+$', v):
            raise ValueError('Número de teléfono inválido')
        return v
    
class EstudianteCreate(EstudianteBase):
    carreras: List[str] = []
    materias: List[str] = []
    pass


class CarreraCreate(CarreraBase):
    pass

class MateriaCreate(MateriaBase):
    pass

class Estudiante(EstudianteBase):
    id: int
    carreras: List[CarreraBase] = []
    materias: List[MateriaBase] = []

    class Config:
        orm_mode = True

class Carrera(CarreraBase):
    id: int
    estudiantes: List[EstudianteBase] = []
    materias: List[MateriaBase] = []

    class Config:
        orm_mode = True

class Materia(MateriaBase):
    id: int
    carrera: CarreraBase
    estudiante: EstudianteBase

    class Config:
        orm_mode = True