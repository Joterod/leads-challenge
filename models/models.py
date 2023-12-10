from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from config.database import Base

# Tabla de relación muchos-a-muchos entre Estudiante y Carrera
estudiante_carrera_association = Table('estudiante_carrera_association', Base.metadata,
    Column('estudiante_id', ForeignKey('estudiantes.id'), primary_key=True),
    Column('carrera_id', ForeignKey('carreras.id'), primary_key=True)
)

# Tabla de relación muchos-a-muchos entre Estudiante y Materias
estudiante_materia_association = Table('estudiante_materia_association', Base.metadata,
    Column('estudiante_id', ForeignKey('estudiantes.id'), primary_key=True),
    Column('materia_id', ForeignKey('materias.id'), primary_key=True)
)

class Estudiante(Base):
    """ Modelo de Estudiante para la base de datos PostgreSQL"""
    
    __tablename__ = 'estudiantes'

    id = Column(Integer, primary_key=True)
    nombre_completo = Column(String, nullable=False)
    correo = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    edad = Column(Integer, nullable=False)
    carreras = relationship(
        'Carrera', secondary=estudiante_carrera_association, back_populates='estudiantes'
    )
    materias = relationship('Materia', secondary=estudiante_materia_association, back_populates='estudiante')

class Carrera(Base):
    __tablename__ = 'carreras'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    estudiantes = relationship(
        'Estudiante', secondary=estudiante_carrera_association, back_populates='carreras' 
    )
    # Relación uno-a-muchos con Materia
    materias = relationship('Materia', back_populates='carrera')

class Materia(Base):
    __tablename__ = 'materias'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    carrera_id = Column(Integer, ForeignKey('carreras.id'))
    # Relación muchos-a-uno con Carrera
    carrera = relationship('Carrera', back_populates='materias')
    estudiante_id = Column(Integer, ForeignKey('estudiantes.id'))
    # Relación muchos-a-uno con Estudiante
    estudiante = relationship('Estudiante', back_populates='materias')
