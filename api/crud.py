from sqlalchemy.orm import Session
from api import models

def obtener_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Usuario).offset(skip).limit(limit).all()

def crear_usuario(db: Session, usuario: models.UsuarioBase):
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

def leer_usuario(db: Session, usuario_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()



def eliminar_usuario(db: Session, usuario_id: int):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if usuario:
        db.delete(usuario)
        db.commit()
        return usuario
    return None


def obtener_usuario_con_empresa(db: Session, usuario_id: int):
    return db.query(models.Usuario, models.Empresa).join(models.Usuario.empresa).filter(models.Usuario.id == usuario_id).first()

def obtener_empresas(db: Session):
    return db.query(models.Empresa).all()

def obtener_usuarios_por_empresa(db: Session, id_fk_empresa: int):
    return db.query(models.Usuario).filter(models.Usuario.id_fk_empresa == id_fk_empresa).all()