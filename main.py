from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()

# Tabla intermedia para la relación muchos a muchos
alumno_asignatura = Table('alumno_asignatura', Base.metadata,
    Column('alumno_id', Integer, ForeignKey('alumnos.id'), primary_key=True),
    Column('asignatura_id', Integer, ForeignKey('asignaturas.id'), primary_key=True)
)

class Alumno(Base):
    __tablename__ = 'alumnos'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    asignaturas = relationship('Asignatura', secondary=alumno_asignatura, back_populates='alumnos')

class Asignatura(Base):
    __tablename__ = 'asignaturas'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    alumnos = relationship('Alumno', secondary=alumno_asignatura, back_populates='asignaturas')

# Configuración de la base de datos
engine = create_engine('sqlite:///school.db')
Base.metadata.create_all(engine)

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()

# Ejemplo de inserción de datos
# Crear alumnos
alumno1 = Alumno(nombre='Fred Crespo')
alumno2 = Alumno(nombre='Jenkins Guevara')

# Crear asignaturas
asignatura1 = Asignatura(nombre='Contruccion Software')
asignatura2 = Asignatura(nombre='Base De Datos')
asignatura3 = Asignatura(nombre='Analisis Y Requerimiento de Software')

# Relacionar alumnos con asignaturas
alumno1.asignaturas = [asignatura1, asignatura2]
alumno2.asignaturas = [asignatura2, asignatura3]

# Agregar a la sesión
session.add(alumno1)
session.add(alumno2)
session.add(asignatura1)
session.add(asignatura2)
session.add(asignatura3)

# Confirmar transacción
session.commit()

# Consultar datos
for alumno in session.query(Alumno).all():
    print(f'Alumno: {alumno.nombre}')
    for asignatura in alumno.asignaturas:
        print(f'  Asignatura: {asignatura.nombre}')