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

def actualizar_usuario(db: Session, usuario_id: int, usuario: models.UsuarioBase):
    db_usuario = db.query(models.UsuarioBase).get(usuario_id)
    for key, value in usuario.dict().items():
        setattr(db_usuario, key, value)
    db.commit()
    return db_usuario

def eliminar_usuario(db: Session, usuario_id: int):
    usuario = db.query(models.UsuarioBase).get(usuario_id)
    db.delete(usuario)
    db.commit()
    return {"message": "Usuario eliminado"}

def obtener_usuarios_por_empresa(db: Session, empresa_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id_fk_empresa == empresa_id).all()

