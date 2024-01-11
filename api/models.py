from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from pydantic import BaseModel


class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)

    usuarios = relationship("Usuario", back_populates="empresa", cascade="all, delete-orphan", single_parent=True)
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    id_fk_empresa = Column(Integer, ForeignKey("empresas.id"))
    nombre = Column(String)
    email = Column(String)


    empresa = relationship("Empresa", back_populates="usuarios")



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

