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
    return db.query(models.Usuario).get(usuario_id)



def eliminar_usuario(db: Session, usuario_id: int):
    usuario = db.query(models.Usuario).get(usuario_id)
    db.delete(usuario)
    db.commit()
    return {"message": "Usuario eliminado"}

def obtener_usuarios_por_empresa(db: Session, empresa_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id_fk_empresa == empresa_id).all()

