from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from pydantic import BaseModel

# modelos SQLAlchemy
class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    id_fk_empresa = Column(Integer, ForeignKey("empresas.id"))
    nombre = Column(String)
    email = Column(String)

    empresa = relationship("Empresa")



class EmpresaBase(BaseModel):
    nombre: str

    class Config:
        orm_mode = True

class UsuarioBase(BaseModel):
    id_fk_empresa: int
    nombre: str
    email: str

    class Config:
        orm_mode = True

