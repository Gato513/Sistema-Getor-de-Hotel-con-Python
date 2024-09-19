from sqlalchemy import create_engine, Column, String, String, Boolean, Integer, func

from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class Estadia(Base):
    __tablename__ = 'estadias'
    id_estadia = Column(Integer, primary_key=True)
    numero_habitacion = Column(String(20))
    tipo_habitacion = Column(String(20))
    costo = Column(Integer)
    dias_estadia = Column(Integer)
    descuento = Column(Integer)
    sub_total = Column(Integer)
    total = Column(Integer)
    forma_de_pago = Column(String(10))
    state = Column(String(10))
    is_employee = Column(String(10))

class Habitacion(Base):
    __tablename__ = 'habitaciones'
    id_habitacion = Column(Integer, primary_key=True)
    tipo = Column(String(20))
    costo = Column(Integer)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    salt = Column(String(64), nullable=False)
    role = Column(String(5), nullable=False, default="user")
    is_first_time =  Column(Boolean, nullable=False, default=True)

def start_connection():
    engine = create_engine(
        "mysql+pymysql://root@localhost/hotel_db"
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def restart_session(current_session):
    current_session.close()
    new_session = start_connection()
    return new_session

def close_session(session):
    session.close()

#! Octener la suma de ingresos totales por tipo de abitacion:
def habitaciones_de_empleados(tipo_habitacion):
    session = start_connection()

    total, dias_estadia = session.query( 
            func.sum(Estadia.total), 
            func.sum(Estadia.dias_estadia)
        ).filter( Estadia.state == 'finalizado', Estadia.tipo_habitacion == tipo_habitacion).first()

    session.close()
    return (dias_estadia if dias_estadia else 0, total if total else 0)

def get_tipo_abitacion():
    session = start_connection()
    #! Recuperar tipos de abitacion y almacenarlo como lista de tuplas. 
    resultado = session.query(Habitacion.tipo).all()

    tipos_habitacion = []

    for tipo in resultado:
        tipos_habitacion.append(tipo[0]) 
        #* Agregar el primer elemento de cada tupla (el valor de 'tipo') a la lista. otra forma de aplicar el for [tipo[0] for tipo in resultado]

    session.close()
    
    return tipos_habitacion

def empleados_ospedados():
    session = start_connection()

    cantidad_empleados = session.query( 
            func.count(Estadia.is_employee)
        ).filter( Estadia.state == 'En_curso', Estadia.is_employee == "si").first()
    session.close()
    return cantidad_empleados[0];

def habitaciones_de_empleados():
    session = start_connection()
    estadias_de_empleados = session.query(Estadia).filter(Estadia.is_employee == "si").all()
    session.close()
    return estadias_de_empleados
